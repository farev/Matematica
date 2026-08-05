/* rup_check.c — forward DRUP proof checker, written from the definition.
 *
 * Checks that every clause line in a DRUP proof follows from the CNF plus
 * previously verified proof clauses by reverse unit propagation (RUP):
 * asserting the negation of the clause and running unit propagation to
 * exhaustion must yield a conflict.  'd' lines delete clauses.  The proof
 * is accepted iff an empty clause is verified.
 *
 * Usage: rup_check <cnf-file> <drup-file>
 * Exit 0 and prints "s VERIFIED" on success; exit 1 with a diagnostic
 * otherwise.  No code shared with any SAT solver.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

/* ---------- dynamic int buffer ---------- */
typedef struct { int *a; size_t n, cap; } vec;
static void vpush(vec *v, int x) {
    if (v->n == v->cap) { v->cap = v->cap ? 2*v->cap : 16; v->a = realloc(v->a, v->cap*sizeof(int)); if (!v->a) { fprintf(stderr,"oom\n"); exit(2);} }
    v->a[v->n++] = x;
}

/* literal encoding: lit>0 -> 2*lit, lit<0 -> 2*(-lit)+1 ; var(l)=l>>1, neg(l)=l^1 */
static inline int enc(int dimacs) { return dimacs > 0 ? 2*dimacs : 2*(-dimacs)+1; }

/* clause database: flat arena of (len, deleted, lits...) records */
typedef struct { int len; int deleted; int lits[]; } clause;
static clause **cls; static size_t ncls, capcls;
static void addcls_ptr(clause *c) {
    if (ncls == capcls) { capcls = capcls ? 2*capcls : 1024; cls = realloc(cls, capcls*sizeof(clause*)); if(!cls){fprintf(stderr,"oom\n");exit(2);} }
    cls[ncls++] = c;
}

/* watches: per literal, list of clause indices */
static vec *watch;           /* size 2*(nvars+1) */
static int nvars;

/* assignment: 0 unassigned, 1 true, -1 false (indexed by var); trail for undo */
static signed char *val;     /* value of variable */
static int *trail; static int trailn;
static inline int litval(int l) { int v = val[l>>1]; return (l&1) ? -v : v; } /* 1 sat, -1 falsified, 0 unassigned */
static inline void assign(int l) { val[l>>1] = (l&1) ? -1 : 1; trail[trailn++] = l; }

/* hash of a clause = order-independent hash of literal set, for deletions */
static uint64_t clshash(const int *lits, int len) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < len; i++) { uint64_t x = (uint64_t)(uint32_t)lits[i]; x *= 0x9E3779B97F4A7C15ULL; h ^= x; }
    return h * (uint64_t)(len + 1);
}

/* simple open hash: hash -> vec of clause indices */
#define HB 20
static vec hbuck[1<<HB];
static void hadd(uint64_t h, int idx) { vpush(&hbuck[h & ((1<<HB)-1)], idx); }

static int sortcmp(const void *a, const void *b) { return *(const int*)a - *(const int*)b; }

/* unit propagation over non-deleted clauses using watched literals.
 * returns 1 on conflict, 0 on fixpoint. */
static int propagate(int qhead) {
    while (qhead < trailn) {
        int fl = trail[qhead++] ^ 1;      /* literal that just became false */
        vec *w = &watch[fl];
        size_t i = 0, j = 0;
        int conflict = 0;
        for (i = 0; i < w->n; i++) {
            int ci = w->a[i];
            clause *c = cls[ci];
            if (c->deleted) continue;      /* drop lazily */
            /* ensure fl is c->lits[1] */
            if (c->lits[0] == fl) { c->lits[0] = c->lits[1]; c->lits[1] = fl; }
            /* clause satisfied? */
            if (litval(c->lits[0]) == 1) { w->a[j++] = ci; continue; }
            /* find replacement watch */
            int found = 0;
            for (int k = 2; k < c->len; k++) {
                if (litval(c->lits[k]) != -1) {
                    c->lits[1] = c->lits[k]; c->lits[k] = fl;
                    vpush(&watch[c->lits[1]], ci);
                    found = 1; break;
                }
            }
            if (found) continue;           /* moved to another watch list */
            /* no replacement: unit or conflict on lits[0] */
            w->a[j++] = ci;
            int v0 = litval(c->lits[0]);
            if (v0 == -1) { conflict = 1; i++; break; }
            if (v0 == 0) assign(c->lits[0]);
        }
        if (conflict) { for (; i < w->n; i++) w->a[j++] = w->a[i]; w->n = j; return 1; }
        w->n = j;
    }
    return 0;
}

/* attach a clause (len>=2) to watches; assumes lits[0], lits[1] chosen */
static void attach(int idx) {
    clause *c = cls[idx];
    vpush(&watch[c->lits[0]], idx);
    vpush(&watch[c->lits[1]], idx);
}

/* read integers from file token by token; returns vec of clause token lists */
static int read_clause(FILE *f, vec *out, int *is_delete) {
    out->n = 0; *is_delete = 0;
    int c;
    /* skip whitespace and comment lines */
    for (;;) {
        c = fgetc(f);
        if (c == EOF) return 0;
        if (c == 'c' || c == 'p') { while ((c = fgetc(f)) != EOF && c != '\n'); continue; }
        if (c == 'd') { *is_delete = 1; continue; }
        if (c == ' ' || c == '\t' || c == '\n' || c == '\r') continue;
        ungetc(c, f); break;
    }
    for (;;) {
        int x;
        if (fscanf(f, "%d", &x) != 1) return 0;
        if (x == 0) return 1;
        vpush(out, x);
    }
}

int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: %s cnf drup\n", argv[0]); return 2; }
    FILE *fc = fopen(argv[1], "r"); if (!fc) { perror("cnf"); return 2; }
    FILE *fp = fopen(argv[2], "r"); if (!fp) { perror("drup"); return 2; }

    /* pass 1 over cnf: find max var */
    vec tmp = {0}; int isdel;
    long fpos = 0;
    { int ch; while ((ch = fgetc(fc)) != EOF) { if (ch=='p'){ /* p cnf nv nc */ if (fscanf(fc, " cnf %d", &nvars)!=1){fprintf(stderr,"bad header\n");return 2;} while((ch=fgetc(fc))!=EOF&&ch!='\n'); fpos = ftell(fc); break;} while ((ch=fgetc(fc))!=EOF && ch!='\n'); } }
    if (nvars <= 0) { fprintf(stderr, "no header\n"); return 2; }
    /* proof may mention fresh vars? DRUP doesn't introduce vars. Reserve nvars. */
    val = calloc(nvars+1, 1);
    trail = malloc(sizeof(int)*2*(nvars+1)); trailn = 0;
    watch = calloc(2*(nvars+1)+2, sizeof(vec));

    /* load cnf clauses */
    fseek(fc, fpos, SEEK_SET);
    long ncnf = 0;
    int root_conflict = 0;
    while (read_clause(fc, &tmp, &isdel)) {
        ncnf++;
        clause *c = malloc(sizeof(clause) + sizeof(int)*(tmp.n?tmp.n:1));
        c->len = (int)tmp.n; c->deleted = 0;
        for (size_t i = 0; i < tmp.n; i++) {
            int l = tmp.a[i];
            if (l > nvars || -l > nvars) { fprintf(stderr, "var out of range in cnf\n"); return 2; }
            c->lits[i] = enc(l);
        }
        addcls_ptr(c);
        int idx = (int)ncls - 1;
        /* register hash on sorted encoded lits */
        int *s = malloc(sizeof(int)*(c->len?c->len:1));
        memcpy(s, c->lits, sizeof(int)*c->len);
        qsort(s, c->len, sizeof(int), sortcmp);
        hadd(clshash(s, c->len), idx);
        free(s);
        if (c->len == 0) root_conflict = 1;
        else if (c->len == 1) { int l = c->lits[0]; int v = litval(l); if (v == -1) root_conflict = 1; else if (v == 0) assign(l); }
        else attach(idx);
    }
    fclose(fc);
    if (!root_conflict && propagate(0) ) root_conflict = 1;
    int root_qhead = trailn; /* everything up to here is permanent */

    if (root_conflict) { printf("s VERIFIED (cnf is unsat by unit propagation alone)\n"); return 0; }

    /* process proof */
    long line = 0; int verified_empty = 0;
    vec elits = {0};
    while (read_clause(fp, &tmp, &isdel)) {
        line++;
        /* encode */
        elits.n = 0;
        for (size_t i = 0; i < tmp.n; i++) {
            int l = tmp.a[i];
            if (l > nvars || -l > nvars) { fprintf(stderr, "FAIL line %ld: var out of range\n", line); return 1; }
            vpush(&elits, enc(l));
        }
        if (isdel) {
            int *s = malloc(sizeof(int)*(elits.n?elits.n:1));
            memcpy(s, elits.a, sizeof(int)*elits.n);
            qsort(s, elits.n, sizeof(int), sortcmp);
            uint64_t h = clshash(s, (int)elits.n);
            vec *b = &hbuck[h & ((1<<HB)-1)];
            int hit = 0;
            for (size_t i = 0; i < b->n; i++) {
                clause *c = cls[b->a[i]];
                if (c->deleted || c->len != (int)elits.n) continue;
                int *t = malloc(sizeof(int)*(c->len?c->len:1));
                memcpy(t, c->lits, sizeof(int)*c->len);
                qsort(t, c->len, sizeof(int), sortcmp);
                int eq = memcmp(t, s, sizeof(int)*c->len) == 0;
                free(t);
                if (eq) {
                    /* never delete clauses that are root units: keeps root trail sound */
                    if (c->len >= 2) c->deleted = 1;
                    hit = 1; break;
                }
            }
            free(s);
            (void)hit; /* deleting an absent clause is sound; ignore */
            continue;
        }
        /* RUP check: assert negation of clause, propagate, expect conflict */
        int save = trailn;
        int conflict = 0;
        for (size_t i = 0; i < elits.n && !conflict; i++) {
            int l = elits.a[i];
            int v = litval(l);
            if (v == 1) conflict = 1;          /* literal already true at root: negation conflicts */
            else if (v == 0) assign(l ^ 1);    /* assert negation */
        }
        if (!conflict) conflict = propagate(save);
        /* undo */
        while (trailn > save) { int l = trail[--trailn]; val[l>>1] = 0; }
        if (!conflict) { fprintf(stderr, "FAIL line %ld: clause is not RUP\n", line); return 1; }
        if (elits.n == 0) { verified_empty = 1; break; }
        /* add clause */
        clause *c = malloc(sizeof(clause) + sizeof(int)*(elits.n?elits.n:1));
        c->len = (int)elits.n; c->deleted = 0;
        memcpy(c->lits, elits.a, sizeof(int)*elits.n);
        addcls_ptr(c);
        int idx = (int)ncls - 1;
        int *s = malloc(sizeof(int)*c->len);
        memcpy(s, c->lits, sizeof(int)*c->len);
        qsort(s, c->len, sizeof(int), sortcmp);
        hadd(clshash(s, c->len), idx);
        free(s);
        if (c->len == 1) {
            /* persistent unit: extend root trail */
            int l = c->lits[0]; int v = litval(l);
            if (v == -1) { verified_empty = 1; break; } /* contradiction at root => unsat */
            if (v == 0) { assign(l); if (propagate(root_qhead)) { verified_empty = 1; break; } }
            root_qhead = trailn;
        } else attach(idx);
    }
    fclose(fp);
    if (verified_empty) { printf("s VERIFIED (empty clause derived; %ld cnf clauses, %ld proof lines)\n", ncnf, line); return 0; }
    fprintf(stderr, "FAIL: proof ended without deriving the empty clause (%ld lines)\n", line);
    return 1;
}
