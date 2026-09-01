Order-5 certification, final status (2026-09-01):

- ord5_CC_cbrk.cnf ([C,C], color-broken): UNSAT, kissat 4.0.4 ~40 min.
  Proof: 812,151,699-byte binary DRAT, sha256
  3140a05af4ef7201d249859494f0a4cc5b103058e77a731a184e367d784aa122,
  VERIFIED by drat-trim in 2,173.7 s (12,529,597 lemmas, 5,211 RAT
  lemmas in core, 239,361,928 resolution steps). Too large to commit;
  regenerate: kissat ord5_CC_cbrk.cnf proof.
- ord5_CI_cbrk.cnf ([C,I], color-broken): UNSAT twice — Glucose42 5.5 s,
  307,292-line pure DRUP VERIFIED by tools/satcert/rup_check (shipped:
  certs/ord5_CI_cbrk.drup.gz), and kissat ~7 min, DRAT VERIFIED by
  drat-trim (6.2 s).
- Soundness of the breaking: color-WLOG lemma, proved in NOTE section 4.
- Unbroken ord5_CC.cnf / ord5_CI.cnf: still running at session close
  (not needed for Theorem 1; would remove the color-lemma proviso).
- combined_ord5_ext.cnf: still running at session close.

Theorem 1 stands: every proper 5-coloring of PG(7,2) has a 2-group
stabilizer, modulo only the color-WLOG hand lemma.
