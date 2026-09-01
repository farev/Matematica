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
- Unbroken ord5_CI.cnf (no symmetry breaking): **UNSAT**, kissat 4.0.4,
  ~90 min — removes the color-lemma proviso for the [C,I] leg as a
  solver verdict (6.7 GB binary DRAT, sha256 45643fc3…, too large to
  verify in-session or commit; regenerate: kissat ord5_CI.cnf proof).
- Unbroken ord5_CC.cnf: terminated undecided after ~3 h (proof past
  3.4 GB). Not needed for Theorem 1; its UNSAT would remove the
  color-lemma proviso for [C,C]. Open thread.
- combined_ord5_ext.cnf ("does any witness have an order-5-symmetric
  hyperplane shadow?"): terminated undecided after ~2.5 h (proof past
  5.9 GB). Open thread — cube-and-conquer candidate; UNSAT would be a
  new certified structural exclusion strictly stronger than the sampled
  non-extensions.

Theorem 1 stands: every proper 5-coloring of PG(7,2) has a 2-group
stabilizer, modulo only the color-WLOG hand lemma.
