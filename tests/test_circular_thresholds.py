"""Smoke tests for conjectures/circular-thresholds.

Fast checks only: they guard the encoder against the from-the-definition
checker, and pin the two small published constants the session calibrated
against.  Run with:  python3 -m pytest tests/test_circular_thresholds.py
"""
import os
import random
import sys
from fractions import Fraction

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
CONJ = os.path.join(os.path.dirname(HERE), 'conjectures', 'circular-thresholds')
sys.path.insert(0, CONJ)

pytest.importorskip('pysat')
pytest.importorskip('numpy')

import circspec  # noqa: E402
import pump  # noqa: E402


def naive_circular_afree(w, alpha):
    """Straight from the definition: every factor of the circular word of
    length <= m has exponent <= alpha."""
    m = len(w)
    for i in range(m):
        for l in range(2, m + 1):
            u = [w[(i + t) % m] for t in range(l)]
            p = next((pp for pp in range(1, l)
                      if all(u[t] == u[t + pp] for t in range(l - pp))), None)
            if p is not None and Fraction(l, p) > alpha:
                return False
    return True


def test_rt_values():
    assert circspec.RT(3) == Fraction(7, 4)
    assert circspec.RT(4) == Fraction(7, 5)
    assert circspec.RT(5) == Fraction(5, 4)
    assert circspec.RT(9) == Fraction(9, 8)


def test_checkers_agree_on_random_words():
    random.seed(20260803)
    a = Fraction(7, 4)
    for _ in range(120):
        m = random.randint(2, 16)
        w = [random.randrange(3) for _ in range(m)]
        assert naive_circular_afree(w, a) == pump.circ_afree(w, a, 0)[0]


def test_sat_witnesses_are_genuine():
    """Every SAT witness must survive the independent O(m^3) checker."""
    for n, ms in ((3, range(23, 33)), (5, range(64, 72))):
        a = circspec.RT(n)
        for m in ms:
            ok, w = circspec.solve(n, m, a)
            assert ok, (n, m)
            assert naive_circular_afree(w, a), (n, m, w)


def test_n3_spectrum_exceptions_below_23():
    """Positive control: CRT_I(3) = RT(3) = 7/4 is known, so the ternary
    spectrum must be cofinite.  Pin the small exceptional set."""
    a = circspec.RT(3)
    expected = {5, 7, 9, 10, 14, 16, 17, 22}
    for m in range(1, 24):
        ok, _ = circspec.solve(3, m, a)
        assert ok == (m not in expected), m


def test_crt_s_calibration():
    """Gorbunova / Currie-Mol: at alpha = CRT_S(k) every length is realizable.
    Checked on a short range for k = 5, 6."""
    for n, alpha in ((5, Fraction(4, 3)), (6, Fraction(4, 3))):
        for m in range(1, 25):
            ok, w = circspec.solve(n, m, alpha)
            assert ok, (n, m)
            assert naive_circular_afree(w, alpha), (n, m, w)


def test_ternary_morphism_passes_H1_H4():
    """The q=28 morphism of NOTE.md section 7."""
    h0 = [int(c) for c in '0120212010201210120102120210']
    rep = pump.morphcheck(3, h0, circspec.RT(3), verbose=False)
    assert rep['H1'] and rep['H2'] and rep['H3'] and rep['H4']
    assert rep['N0'] == 8 and rep['P0'] == 75


def test_pumping_one_step():
    """Lemma A in action: h(w0) must be circular threshold at length 560."""
    h0 = [int(c) for c in '0120212010201210120102120210']
    w0 = [int(c) for c in '01202101210212012102']
    a = circspec.RT(3)
    assert pump.circ_afree(w0, a, 2)[0]
    w1 = pump.apply_morph(3, h0, w0)
    assert len(w1) == 560
    assert pump.circ_afree(w1, a, 2)[0]


def test_D_cutoff_small_cases():
    """Result L: longest RT(n)^+-free word with <= 2 distinct differences."""
    import dcut
    assert dcut.longest(5, circspec.RT(5), (1, 2)) == 8
    assert dcut.longest(7, circspec.RT(7), (1, 2)) == 10
