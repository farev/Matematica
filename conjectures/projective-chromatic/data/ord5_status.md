Order-5 certification runs (kissat 4.0.4), 2026-09-01:

- ord5_CC_cbrk.cnf (color-precedence-broken [C,C], sound WLOG under the S5
  color action): **UNSAT** after ~40 min — so there is NO [C,C]-type
  order-5-invariant 5-coloring of PG(7,2), CERTIFIED modulo the trivial
  color-WLOG hand lemma. 812 MB DRAT proof; independent drat-trim check
  launched (result recorded here when done).
- ord5_CC.cnf (unbroken): still running (its UNSAT would remove the
  color-lemma caveat).
- ord5_CI.cnf (unbroken): still running.
- ord5_CI_cbrk.cnf (color-broken [C,I]): launched after the CC verdict.
- combined_ord5_ext.cnf: still running.

If CI lands UNSAT (either form): Theorem 1 (2-group stabilizers) is
complete, modulo the color lemma where only broken forms finished.
