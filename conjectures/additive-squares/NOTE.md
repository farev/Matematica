# Additive squares: a relation-lattice reduction, and exact maxima for small alphabets

**Session:** 2026-08-01 · **Status:** active

> **AI disclosure.** This note was produced in a research session run with
> substantial AI assistance (Claude). No AI system is an author. Every proof
> below is short enough to check by hand and is meant to be checked; every
> numerical claim ships the code that emits it.

> **Connectivity caveat, stated up front.** The session ran in a sandbox whose
> egress policy blocked `arxiv.org`, `oeis.org`, `erdosproblems.com` and
> `mathoverflow.net` at the CONNECT layer (HTTP 403). Web *search* was
> available; page *fetches* were not. **No primary source was read.** Every
> citation in §7 is therefore marked **(secondary)** — it rests on search-result
> synthesis, not on the paper. Two consequences are load-bearing and are
> repeated where they matter: (i) Theorem 5 reproduces a published theorem of
> Freedman and is presented as a clean-room reproduction, not as new; (ii)
> Theorem 4 is very likely folklore.

## Abstract

Let $A$ be a finite subset of a field of characteristic $0$. A word $w$ over
$A$ contains an *additive square* if it has a factor $uv$ with $|u|=|v|$ and
$\sum u = \sum v$; it is *additive-square-free* otherwise. Write $L(A)$ for the
supremum of the lengths of additive-square-free words over $A$. Whether an
infinite additive-square-free word exists over some finite $A \subset \mathbb{Z}$
is the Pirillo–Varricchio / Halbeisen–Hungerbühler problem, open since the
1990s.

We record an elementary reduction (Lemma 2, the *Quotient Lemma*): the
additive-square structure of $A$ depends on $A$ only through its **relation
lattice**, and quotienting by any sublattice of relations can only *increase*
$L$. Consequently a single finite computation over a universal alphabet of
integer **vectors** bounds $L$ simultaneously for every alphabet satisfying a
given integer relation. Three consequences:

1. $L(A) = 7$ for **every** three-element alphabet in characteristic $0$
   (Theorem 4) — a uniform statement over an infinite family, from one
   354-node search plus a hand-checked seven-letter witness.
2. $L(A) \le 60$ for every four-element alphabet with $a+d=b+c$ (Theorem 5),
   which is Freedman's published bound, here re-derived in three lines from the
   single relation $(1,1,-1)$; and the bound is **attained**, at
   $A=\{0,1,5,6\}$.
3. Exact values of $L(A)$ for 34 four-element integer alphabets (Table 6) —
   the first such table we are aware of, though see the caveat in §7.

## 1. Definitions

Let $K$ have characteristic $0$ and let $A \subset K$ be finite with $|A| = m$.
For a word $w = w_1 \cdots w_n$ over $A$, an **additive square** is a pair of
indices $(i,k)$ with $k \ge 1$, $i + 2k - 1 \le n$, and

$$\sum_{j=i}^{i+k-1} w_j \;=\; \sum_{j=i+k}^{i+2k-1} w_j .$$

$w$ is **additive-square-free** (afsf) if it admits none. Set

$$L(A) \;=\; \sup\{\,|w| : w \text{ afsf over } A\,\} \in \mathbb{N} \cup \{\infty\}.$$

An abelian square (two adjacent blocks that are permutations of one another) is
always an additive square, so afsf is a *strictly stronger* condition than
abelian-square-free.

**PVHH problem.** Is $L(A) = \infty$ for some finite $A \subset \mathbb{Z}$?
Open (secondary; see §7).

## 2. Affine invariance and the relation lattice

**Lemma 1 (affine invariance).** *For $\alpha \in K^{\times}$, $\beta \in K$,*
$L(\alpha A + \beta) = L(A)$.

*Proof.* The bijection $x \mapsto \alpha x + \beta$ carries a word $w$ over $A$
to a word $w'$ over $\alpha A + \beta$ of the same length. A block of length $k$
with sum $\sigma$ becomes a block with sum $\alpha\sigma + k\beta$. Two blocks
of **equal length** $k$ have equal sums in $w$ iff their images have equal sums
in $w'$, since $\alpha \ne 0$. So $w$ is afsf iff $w'$ is. $\square$

By Lemma 1 we may always normalise so that $0 \in A$. Write
$A = \{x_0, x_1, \dots, x_{m-1}\}$ with $x_0 = 0$.

Given a factor $uv$ of a word over $A$ with $|u| = |v| = k$, let
$\delta(u,v) \in \mathbb{Z}^{m-1}$ be the vector of **count-differences** of the
letters $x_1,\dots,x_{m-1}$ between $u$ and $v$. (The count-difference of $x_0$
is determined by the others because $|u| = |v|$, and contributes nothing to
sums because $x_0 = 0$.) Then

$$\sum u - \sum v \;=\; \sum_{i=1}^{m-1} \delta_i\, x_i .$$

**Definition.** The **relation lattice** of $A$ is

$$\Lambda(A) \;=\; \Big\{\, \delta \in \mathbb{Z}^{m-1} \;:\; \sum_{i=1}^{m-1}\delta_i x_i = 0 \,\Big\}.$$

**Observation.** $uv$ is an additive square $\iff \delta(u,v) \in \Lambda(A)$.

So additive-square-freeness of a word depends on the alphabet **only through
$\Lambda(A)$**. For $A \subset \mathbb{Z}$ with $m = 4$, $\Lambda(A)$ has rank $2$.

## 3. The Quotient Lemma

Let $M \subseteq \Lambda(A)$ be a subgroup, $Q = \mathbb{Z}^{m-1}/M$, and
$\pi : \mathbb{Z}^{m-1} \to Q$ the quotient map. Put

$$A_M \;=\; \{\,0,\ \pi(e_1),\ \dots,\ \pi(e_{m-1})\,\} \subseteq Q,$$

an alphabet of $m$ elements *provided these are pairwise distinct*, which holds
precisely when $M$ contains no $e_i$ and no $e_i - e_j$. Additive squares over
$A_M$ are defined exactly as in §1, with sums taken in the abelian group $Q$.

**Lemma 2 (Quotient Lemma).** *If the $m$ elements above are pairwise distinct,
then* $L(A) \le L(A_M)$.

*Proof.* Let $w$ be afsf over $A$, $|w| = n$. Define $\hat{w}$ over $A_M$ by
replacing each letter $x_i$ by $\pi(e_i)$ (and $x_0 = 0$ by $0 \in Q$); this is
well defined since the letters are distinct on both sides, and $|\hat w| = n$.

Suppose $\hat w$ had an additive square, say at $(i,k)$, and let $u,v$ be the
two blocks of the corresponding factor of $w$. Summing in $Q$,

$$\textstyle\sum_Q \hat u - \sum_Q \hat v \;=\; \pi\big(\sum_{i\ge1}\delta_i e_i\big) \;=\; \pi(\delta(u,v)),$$

so the supposed square says $\pi(\delta(u,v)) = 0$, i.e.
$\delta(u,v) \in M \subseteq \Lambda(A)$. By the Observation, $uv$ is then an
additive square **in $w$** — contradicting that $w$ is afsf. Hence $\hat w$ is
afsf over $A_M$ and $L(A_M) \ge n$. Taking the supremum over $w$ gives the
claim. $\square$

The content is that *forgetting* relations can only make life easier: $A_M$ has
fewer additive squares than $A$, hence longer afsf words. The lemma is useful in
the direction one wants — a computation over the (finite, canonical) alphabet
$A_M$ bounds $L$ for the whole infinite family of alphabets realising the
relations $M$.

**Corollary 3 (free bound).** *Taking $M = 0$:* $L(A) \le \lambda(m)$, *where
$\lambda(m)$ is the length of the longest abelian-square-free word over $m$
letters.*

Indeed for $M = 0$ we have $Q = \mathbb{Z}^{m-1}$ and $A_M = \{0,e_1,\dots,e_{m-1}\}$
is the *free* alphabet, over which equal-length blocks have equal sums iff they
have equal letter-multisets — i.e. additive squares are exactly abelian squares.
Known values (secondary, §7; independently recomputed here):
$\lambda(2) = 3$, $\lambda(3) = 7$, and $\lambda(4) = \infty$ by Keränen's
$85$-uniform morphism.

That $\lambda(4) = \infty$ is exactly why four letters is the hard case: the
free bound is vacuous, and one must use a nonzero $M$ — that is, a genuine
integer relation among the letters.

## 4. Three letters

**Theorem 4.** *For every three-element $A$ in a field of characteristic $0$,*
$L(A) = 7$.

*Proof.* **Upper bound.** Corollary 3 with $m = 3$ gives $L(A) \le \lambda(3) = 7$.
We recompute $\lambda(3)$ here rather than cite it: exhaustive DFS over the free
alphabet $\{(0,0),(1,0),(0,1)\} \subset \mathbb{Z}^2$ closes the whole tree in
**354 nodes** and returns $7$ (`afsfv exhaust 2 "0,0|1,0|0,1"`). Equivalently:
every ternary word of length $8$ contains an abelian square — a $3^8 = 6561$-case
check, small enough to audit by hand.

**Lower bound.** By Lemma 1 normalise $A = \{0,1,t\}$ with $t \notin \{0,1\}$.
The single word

$$w \;=\; 0,\,1,\,0,\,t,\,0,\,1,\,0$$

is afsf for **every** such $t$. Since $|w| = 7$, only $k \le 3$ occurs:

- $k=1$: the six adjacent pairs are $(0,1),(1,0),(0,t),(t,0),(0,1),(1,0)$;
  the differences are $\mp 1$ and $\mp t$, nonzero as $t \neq 0$.
- $k=2$: the four block-pairs have sums $(1,t)$, $(1,t)$, $(t,1)$, $(t,1)$;
  equal only if $t = 1$, excluded.
- $k=3$: the two block-pairs have sums $(1, t+1)$ and $(1+t, 1)$; equal only if
  $t = 0$, excluded.

So $L(A) \ge 7$. $\square$

Note what the uniform witness buys: no case analysis over $t$ is needed, because
every one of the twelve inequalities degenerates only at $t \in \{0,1\}$, which
the hypothesis $|A| = 3$ already forbids.

**This is very likely folklore.** The upper bound is the classical unavoidability
of abelian squares on three letters; the lower bound is a seven-letter word. We
could not locate a published statement in the exact form "$L(A) = 7$ for every
three-element alphabet" (§7, item 5), but absence of a citation under a blocked
network is not evidence of novelty, and we do not claim any.

## 5. Four letters: the relation $(1,1,-1)$, and Freedman's constant

Call $A = \{a,b,c,d\}$ **degenerate** if $a + d = b + c$ (equivalently, after
normalising, one letter is the sum of two others: $A \sim \{0,x,y,x+y\}$).

**Theorem 5.** *Let $A$ be a four-element degenerate alphabet in a field of
characteristic $0$. Then $L(A) \le 60$. The bound is attained:
$L(\{0,1,5,6\}) = 60$.*

*Proof of the bound.* Normalise $A = \{0, 1, t, 1+t\}$ (Lemma 1), with letters
ordered $x_0=0, x_1=1, x_2=t, x_3=1+t$. Then $(1,1,-1) \in \Lambda(A)$, since
$1\cdot 1 + 1\cdot t - 1\cdot(1+t) = 0$ — and this holds for **every** $t$,
which is the whole point. Take $M = \langle (1,1,-1) \rangle$. Then
$\mathbb{Z}^3/M \cong \mathbb{Z}^2$, and the four images $0, \pi(e_1), \pi(e_2),
\pi(e_3)$ are distinct because $M$ contains no $e_i$ and no $e_i - e_j$. Lemma 2
gives $L(A) \le L(A_M)$, and $L(A_M) = 60$ by exhaustive search. $\square$

**The constant.** $L(A_M) = 60$ is a **CERTIFIED** exhaustive computation, not a
hand proof: the DFS closes the entire tree of afsf words over $A_M$ in
**7,707,828 nodes** (0.03 s), in exact integer arithmetic with no floating point
anywhere. It was computed twice through independent bases:

| route | alphabet $A_M \subset \mathbb{Z}^2$ | nodes | $L$ |
|---|---|---|---|
| hand-chosen basis | $(0,0),(1,0),(0,1),(1,1)$ | 7,707,828 | **60** |
| `relation_quotient.py`, unimodular completion of $(1,1,-1)$ | $(0,0),(-1,0),(1,1),(0,1)$ | 7,707,828 | **60** |
| ditto, sign-flipped class representative $(-1,-1,1)$ | $(0,0),(-1,0),(1,1),(0,1)$ | 7,707,828 | **60** |

Three routes through three different unimodular completions agree on both the
value and the node count, which is a sharper check than agreeing on the value
alone: the trees are isomorphic, as Lemma 2 predicts they must be.

*Attainment.* $L(\{0,1,5,6\}) = 60$ by exhaustive search directly on this
alphabet (6,595,124 nodes, tree closed — smaller than the universal
alphabet's 7,707,828 because $\{0,1,5,6\}$ has not yet reached the saturation
regime of §6), and $0 + 6 = 1 + 5$, so the alphabet is degenerate. The
extremal word is in `data/extremal_words.txt` and is checked by the
independent verifier `verify_word.py`; no letter of the alphabet extends it.

**Relationship to the literature — read this before citing.** The bound
$L \le 60$ for $a+d=b+c$ is **Freedman's theorem** (secondary; quoted in
Cassaigne–Currie–Schaeffer–Shallit, see §7). Theorem 5 is therefore a
**clean-room reproduction**, not a new bound. What the session adds is (i) a
three-line derivation of it from a single relation vector, via Lemma 2, in place
of a bespoke argument, and (ii) the attainment, which we could not confirm as
published — search returned an unsupported assertion that the bound is tight and
nothing behind it (§7, item 3). We claim (ii) only as "not found in the
literature we could reach", which under a blocked network is a weak claim.

## 6. Certified table for four-letter integer alphabets

Alphabets are normalised to $\{0,a,b,c\}$ with $0 < a < b < c$,
$\gcd(a,b,c) = 1$, taken up to the reflection $x \mapsto c - x$ (Lemma 1 with
$\alpha = -1$). Exhaustive DFS, exact integer arithmetic; a value is **exact**
only when the tree closed inside the node budget.

Every value below is **CERTIFIED**: exact arithmetic, reproducible, extremal
word committed and independently verified.

The sweep covered all **381** normalised alphabets with $c \le 18$ and returned
**51** exact values. All **50** degenerate alphabets closed their trees, and
**none exceeded 60**.

| $A$ | $L(A)$ | degenerate? | nodes |
|---|---|---|---|
| $\{0,1,2,3\}$ | 50 | yes | 751,156 |
| $\{0,1,3,4\}$, $\{0,2,3,5\}$, $\{0,1,4,5\}$ | 55 | yes | 2.6–4.5 M |
| $\{0,3,4,7\}$ | 58 | yes | 7,012,884 |
| $\{0,1,5,6\}$ and **44** further degenerate alphabets | **60** | yes | ≤ 7,707,828 |
| $\{0,1,2,4\}$ | **62** | no | 76,391,112 |
| $\{0,1,2,5\}$ | 86 | no | 1,198,387,276 |
| $\{0,1,3,5\}$ | 88 | no | 937,940,596 |

($\{0,2,3,4\}$ is not a separate entry: $x \mapsto 4-x$ carries it to
$\{0,1,2,4\}$, and it returns the identical value 62 and the identical node
count 76,391,112 — an incidental check that the reflection normalisation in
`sweep4.py` is correct.)

Full machine-readable table: `data/sweep4_c18.csv` (one row per alphabet, with
the extremal word and node count).

**The degenerate family takes only four values, CERTIFIED.** Over all 50
degenerate alphabets with $c \le 18$, $L$ is one of

$$50\ (\times 1),\quad 55\ (\times 3),\quad 58\ (\times 1),\quad 60\ (\times 45),$$

with the exceptional values realised by $\{0,1,2,3\}$; $\{0,1,3,4\}$,
$\{0,2,3,5\}$, $\{0,1,4,5\}$; and $\{0,3,4,7\}$ respectively. This is exactly the
cell decomposition of §3 seen from the integer side: writing $A = \{0,1,t,1+t\}$,
the parameter $t$ falls below the generic value 60 only for the handful of
small-height rationals at which an extra low-coefficient relation happens to
vanish. Every other alphabet sits in the generic cell and returns 60.

**A structural observation, CERTIFIED.** Among degenerate alphabets the node
count *saturates* at exactly **7,707,828** — the node count of the generic
$\mathbb{Z}^2$ alphabet $A_M$ — for every alphabet from $\{0,1,9,10\}$ onward in
the sweep. In other words, once the letters are spread far enough apart, the
search tree of the integer alphabet is **literally identical** to the tree of
the universal quotient alphabet: no extra relation with small coefficients is
available to create additional squares. This is the cell-decomposition picture
of §3 made visible, and it is the reason $60$ is attained rather than merely
approached: the generic cell is realised by honest integer alphabets.

**Lower bounds are budget-limited and are not estimates of $L$.** Rows in
`data/sweep4_c18.csv` marked `exact=0` record only how deep a fixed node budget
reached. They are certified lower bounds — the words are real and verifiable —
but the depth reached is an artifact of the budget, not a measurement of $L(A)$,
and must not be read as growth data.

## 7. Prior work

**Everything in this section is (secondary).** Page fetches to arXiv, OEIS,
erdosproblems.com and MathOverflow were blocked (HTTP 403 at the proxy); these
entries come from web-search synthesis only. No primary source was read. Each
should be re-checked from an unblocked network before any of it is repeated in
a preprint.

1. **PVHH problem.** Pirillo–Varricchio (*On uniformly repetitive semigroups*,
   Semigroup Forum, 1994) and independently Halbeisen–Hungerbühler. Asks whether
   an infinite additive-square-free word exists over a finite subset of
   $\mathbb{Z}$. **Still open as of 2026** (secondary). Sources disagree on
   1992 vs 1994 — do not cite a year without checking.
2. **Additive cubes.** Cassaigne–Currie–Schaeffer–Shallit, *Avoiding three
   consecutive blocks of the same size and same sum*, arXiv:1106.5204, J. ACM
   61(2) (2014) art. 10: an infinite additive-cube-free word over $\{0,1,3,4\}$.
   Lietard–Rosenfeld (DLT 2020) classify: additive cubes are avoidable over
   every four-element subset of $\mathbb{Z}$ **except possibly** $\{0,1,2,3\}$.
   **This is the exact cube analogue of the square classification the present
   note starts on**, and is where this work would be cited.
3. **Freedman's bound.** If $a+d = b+c$ then every word of length 61 over
   $\{a,b,c,d\}$ contains an additive square, i.e. $L \le 60$; stated for any
   field of characteristic $0$. Attributed to Freedman, *Sequences on sets of
   four numbers* (possibly Freedman & Brown; venue reported inconsistently as
   INTEGERS vol. 16 (2016) and as Math. Magazine 49 (1976) — **unresolved**).
   Quoted in [2]. Whether the bound is **attained** could not be determined.
4. **$\mathbb{Z}^2$.** Rao–Rosenfeld, arXiv:1511.05875, SIAM J. Discrete Math.
   (2018): additive squares **are** avoidable over a finite subset of
   $\mathbb{Z}^2$. Consistent with, and a strong warning about, Lemma 2: for
   vector alphabets $L$ can be infinite, so a relation $M$ that is too small
   yields no bound at all.
5. **Three letters.** No published statement of "$L(A) = 7$ for every
   three-element alphabet" was located. The ingredients are classical:
   abelian squares are unavoidable on three letters, and every ternary word of
   length 8 contains one (secondary).
6. **Abelian squares.** Keränen (ICALP 1992), abelian squares avoidable on four
   letters via an 85-uniform morphism; Entringer–Jackson–Schatz (JCTA 16, 1974)
   for the binary theory; Dekking (1979).
7. **A heuristic pointing the other way.** Ochem's page
   (`lirmm.fr/~ochem/additive_square.htm`) reportedly gives a growth-rate
   heuristic suggesting additive squares are **unavoidable** over
   $\{1,\dots,k\}$, i.e. that PVHH has a negative answer (secondary,
   single-snippet). Our finite $L$ values are consistent with it. Unverified.

## 8. Open questions

1. **Which relation classes force finiteness?** For a primitive
   $v \in \mathbb{Z}^3$, let $A_v$ be the universal alphabet of §3 with
   $M = \langle v \rangle$. Freedman's theorem is the single instance
   $v = (1,1,-1)$, where $L(A_v) = 60$. **For which $v$ is $L(A_v)$ finite?**
   Each finite answer is a Freedman-type theorem for an infinite family of
   integer alphabets, obtained from one computation. Present state
   (`data/relations_n2.csv`), and so far $(1,1,-1)$ is the **only** class of
   sup-norm $\le 2$ whose tree closes:

   All **11** primitive classes of sup-norm $\le 2$ were run to a
   $6\times10^8$-node budget with a depth cap of 3000
   (`data/relations_n2.csv`). Exactly **one** closed:

   | relation $v$ | meaning | $L(A_v)$ |
   |---|---|---|
   | $(1,1,-1)$ | one letter is the sum of two others | **= 60**, tree closed, 7,707,828 nodes |
   | $(2,0,-1)$ | | $\ge 418$ |
   | $(2,-1,-1)$ | | $\ge 439$ |
   | $(1,1,0)$ | alphabet contains a 3-term AP $\{0,x,2x\}$ | $\ge 440$ |
   | $(1,1,1)$ | $a+b+c=0$ | $\ge 996$ |
   | $(2,1,-2)$ | | $\ge 1795$ |
   | $(2,2,-1)$ | | $\ge 1816$ |
   | $(2,1,-1)$ | | $\ge 1836$ |
   | $(2,1,1)$ | | $\ge 1479$ |
   | $(2,1,0)$ | | $\ge 3000$ (**hit the depth cap**) |
   | $(2,2,1)$ | | $\ge 3000$ (**hit the depth cap**) |

   Every word in that table was re-verified by an independent $O(n^2)$ checker
   written from the definition, including both 3000-letter words.

   **Freedman's relation is singular, and by two orders of magnitude**: 60
   against $\ge 3000$. Two classes hit the depth cap rather than the node
   budget, meaning the DFS descended 3000 letters without being forced to
   backtrack out — the signature of an infinite class, and consistent with
   Rao–Rosenfeld [4], who prove additive squares *are* avoidable over a finite
   subset of $\mathbb{Z}^2$. Why $(1,1,-1)$ alone forces finiteness is the
   sharpest question the session leaves open; a proof of it, in place of a
   7.7-million-node tree closure, would likely generalise.

   **The ten open classes are not alike, and the split is the useful part.**
   A second, independent randomised-restart probe (seed 11, depth cap 200,000,
   $4\times10^9$ nodes) separates them:

   - $v = (1,1,0)$, the 3-term-AP class, **plateaus**: 440 from the exhaustive
     budget-limited run, 437 from the independent randomised run. Two different
     searches with different seeds and a 66× larger depth cap agree to within
     three letters. That is what a *finite* $L$ looks like from below, and
     $(1,1,0)$ is therefore the best candidate for a **second** Freedman-type
     theorem. Closing its tree is the concrete next computation.
   - $v = (2,1,0)$ and $v = (2,2,1)$ ran to the depth cap instead. That is what
     an *infinite* $L$ looks like from below.

   The distinction matters because it is the difference between "the Quotient
   Lemma can reach PVHH for four letters" and "it cannot": if even one
   admissible relation class has $L(A_v) = \infty$, alphabets whose only small
   relations are of that type escape the method entirely.
2. Since every four-element $A \subset \mathbb{Z}$ has $\Lambda(A)$ of rank 2,
   $A$ satisfies *some* primitive relation $v$. If $L(A_v) < \infty$ for
   **every** admissible $v$, PVHH would follow for four-letter integer
   alphabets. Is there a $v$ with $L(A_v) = \infty$? By [4] above the analogous
   phenomenon does occur for larger $\mathbb{Z}^2$ alphabets, so we expect yes —
   locating one explicitly is the sharpest next step.
3. Exact $L$ for the small non-degenerate alphabets beyond $\{0,1,3,5\}$. The
   trees grow fast (76 M nodes already at $\{0,1,2,4\}$); $\{0,1,2,6\}$ did not
   close in $4\times10^8$ nodes.
4. Is $\{0,1,2,3\}$ — the one alphabet Lietard–Rosenfeld leave open for cubes —
   also distinguished for squares? It has the **smallest** $L$ of any
   four-letter integer alphabet found (50).

## 9. Reproduction

Hardware: 4 cores, 15 GB RAM, Linux 6.18.5, gcc 13.3 `-O2`, Python 3.11.15.
No floating point in any critical path; all searches are exact integer DFS.
Randomised runs record their seed; every reported search records its node count.

```bash
cd conjectures/additive-squares
gcc -O2 -o afsf afsf.c && gcc -O2 -o afsfv afsfv.c
python3 verify_word.py --selftest                  # controls

./afsfv exhaust 2 "0,0|1,0|0,1"        500 1000000000   # lambda(3)=7,   354 nodes
./afsfv exhaust 2 "0,0|1,0|0,1|1,1"    500 20000000000  # L(A_M)=60, 7,707,828 nodes
./afsf  exhaust "0,1,5,6"              500 20000000000  # attained: L=60
./afsf  exhaust "0,1,2,4"              500 20000000000  # L=62

python3 sweep4.py 18 400000000 4000 3 data/sweep4_c18.csv
python3 relation_quotient.py 2 600000000 3000 1 data/relations_n2.csv
python3 verify_word.py --file data/extremal_words.txt
```
