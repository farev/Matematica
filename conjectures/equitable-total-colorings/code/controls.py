"""controls.py -- positive/negative controls for the encoder and the checker."""
import sys, time, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/tmp/claude-0/-home-user-Matematica/bc2c3ee2-f3c1-5718-9876-930480583604/scratchpad/work")
import tc
from verify_tc import decode_model, check_total_coloring, is_cubic_simple, is_connected

H16_E = [(0, 2), (0, 8), (0, 15), (1, 7), (1, 9), (1, 12), (2, 4), (2, 13),
         (3, 5), (3, 7), (3, 15), (4, 10), (4, 14), (5, 8), (5, 11), (6, 7),
         (6, 12), (6, 13), (8, 15), (9, 11), (9, 13), (10, 12), (10, 14), (11, 14)]
H16_A = {  # profile (6,4,4,2): color -> (S_i, M_i)  (Appendix A.1)
    0: ([2, 3, 8, 9, 12, 14], [(0, 15), (1, 7), (4, 10), (5, 11), (6, 13)]),
    1: ([7, 10, 13, 15], [(0, 8), (1, 9), (2, 4), (3, 5), (6, 12), (11, 14)]),
    2: ([0, 4, 5, 6], [(1, 12), (2, 13), (3, 7), (8, 15), (9, 11), (10, 14)]),
    3: ([1, 11], [(0, 2), (3, 15), (4, 14), (5, 8), (6, 7), (9, 13), (10, 12)]),
}
H16_B = {  # profile (4,4,4,4)
    0: ([1, 5, 13, 14], [(0, 2), (3, 7), (4, 10), (6, 12), (8, 15), (9, 11)]),
    1: ([7, 9, 10, 15], [(0, 8), (1, 12), (2, 4), (3, 5), (6, 13), (11, 14)]),
    2: ([2, 3, 6, 8], [(0, 15), (1, 7), (4, 14), (5, 11), (9, 13), (10, 12)]),
    3: ([0, 4, 11, 12], [(1, 9), (2, 13), (3, 15), (5, 8), (6, 7), (10, 14)]),
}
H18_E = [(0, 5), (0, 8), (0, 17), (1, 4), (1, 12), (1, 15), (2, 5), (2, 8),
         (2, 14), (3, 6), (3, 9), (3, 17), (4, 6), (4, 7), (5, 11), (6, 12),
         (7, 13), (7, 15), (8, 17), (9, 13), (9, 16), (10, 11), (10, 14), (10, 15),
         (11, 12), (13, 16), (14, 16)]
H18_A = {  # profile (6,6,4,2)
    0: ([1, 3, 5, 7, 8, 16], [(0, 17), (2, 14), (4, 6), (9, 13), (10, 15), (11, 12)]),
    1: ([0, 2, 4, 9, 10, 12], [(1, 15), (3, 6), (5, 11), (7, 13), (8, 17), (14, 16)]),
    2: ([6, 14, 15, 17], [(0, 8), (1, 12), (2, 5), (3, 9), (4, 7), (10, 11), (13, 16)]),
    3: ([11, 13], [(0, 5), (1, 4), (2, 8), (3, 17), (6, 12), (7, 15), (9, 16), (10, 14)]),
}
H18_B = {  # profile (6,4,4,4)
    0: ([0, 2, 3, 7, 12, 16], [(1, 15), (4, 6), (5, 11), (8, 17), (9, 13), (10, 14)]),
    1: ([1, 11, 13, 17], [(0, 8), (2, 5), (3, 9), (4, 7), (6, 12), (10, 15), (14, 16)]),
    2: ([4, 5, 14, 15], [(0, 17), (1, 12), (2, 8), (3, 6), (7, 13), (9, 16), (10, 11)]),
    3: ([6, 8, 9, 10], [(0, 5), (1, 4), (2, 14), (3, 17), (7, 15), (11, 12), (13, 16)]),
}


def cert_to_coloring(cert):
    vcol, ecol = {}, {}
    for c, (S, M) in cert.items():
        for v in S:
            vcol[v] = c
        for e in M:
            ecol[tuple(sorted(e))] = c
    return vcol, ecol


def run(name, n, edges, expect_type=None, expect_equit=None):
    assert is_cubic_simple(n, edges), name
    assert is_connected(n, edges), name
    res = {}
    for sb in (True, False):
        for eq in (True, False):
            cl, nv = tc.encode(n, edges, equitable=eq, symbreak=sb)
            t = time.time(); sat, model = tc.solve(cl, 'cadical195'); dt = time.time() - t
            ok = None
            if sat:
                vc, ec = decode_model(n, edges, model)
                ok, msg, sizes = check_total_coloring(n, edges, vc, ec, equitable=eq)
                assert ok, (name, eq, sb, msg)
                res[(eq, sb)] = ("SAT", tuple(sorted(sizes, reverse=True)), dt)
            else:
                res[(eq, sb)] = ("UNSAT", None, dt)
    # consistency across symmetry breaking
    assert res[(True, True)][0] == res[(True, False)][0], (name, res)
    assert res[(False, True)][0] == res[(False, False)][0], (name, res)
    # equitable SAT => plain SAT
    if res[(True, True)][0] == "SAT":
        assert res[(False, True)][0] == "SAT"
    typ = 1 if res[(False, True)][0] == "SAT" else 2
    equit = res[(True, True)][0] == "SAT"
    line = f"{name:14s} n={n:2d} Type {typ}  equitable-4TC: {'yes' if equit else 'no':3s}  " \
           f"sizes(eq)={res[(True,True)][1]} sizes(plain)={res[(False,True)][1]}  g6={tc.to_graph6(n, edges)}"
    flag = ""
    if expect_type is not None and expect_type != typ:
        flag += f"  ** EXPECTED TYPE {expect_type} **"
    if expect_equit is not None and expect_equit != equit:
        flag += f"  ** EXPECTED equitable={expect_equit} **"
    print(line + flag, flush=True)
    return typ, equit


if __name__ == "__main__":
    print("== checker controls on the paper's explicit certificates ==")
    for nm, n, E, cert, expect in [("H16 (6,4,4,2)", 16, H16_E, H16_A, (11, 10, 10, 9)),
                                   ("H16 (4,4,4,4)", 16, H16_E, H16_B, (10, 10, 10, 10)),
                                   ("H18 (6,6,4,2)", 18, H18_E, H18_A, (12, 12, 11, 10)),
                                   ("H18 (6,4,4,4)", 18, H18_E, H18_B, (12, 11, 11, 11))]:
        assert is_cubic_simple(n, E) and is_connected(n, E)
        vc, ec = cert_to_coloring(cert)
        ok, msg, sizes = check_total_coloring(n, E, vc, ec, equitable=False)
        ok2, msg2, _ = check_total_coloring(n, E, vc, ec, equitable=True)
        print(f"{nm}: valid 4-total coloring: {ok} ({msg}); sizes {sorted(sizes, reverse=True)} "
              f"expected {list(expect)}; equitable-check: {ok2} ({msg2})")
        assert ok and tuple(sorted(sizes, reverse=True)) == expect
    n, E = tc.graph_R()
    print("R: cubic", is_cubic_simple(n, E), "connected", is_connected(n, E), "n", n, "m", len(E), "g6", tc.to_graph6(n, E))
    vc, ec = tc.figure1_coloring_of_R()
    ok, msg, sizes = check_total_coloring(n, E, vc, ec, equitable=False)
    ok2, msg2, _ = check_total_coloring(n, E, vc, ec, equitable=True)
    print(f"R Figure-1 coloring: valid 4-total coloring: {ok} ({msg}); sizes {sorted(sizes, reverse=True)}; equitable-check: {ok2} ({msg2})")
    assert ok and not ok2
    # negative controls for the checker: corrupt the coloring
    vc2 = dict(vc); vc2[0] = vc2[2]  # T and L of top gadget are adjacent -> same color must be rejected
    print("negative control (adjacent vertices same color):", check_total_coloring(n, E, vc2, ec)[:2])
    ec2 = dict(ec); e0 = min(ec2); ec2[e0] = vc[e0[0]]  # edge gets endpoint's color
    print("negative control (edge = endpoint color):", check_total_coloring(n, E, vc, ec2)[:2])
    ec3 = dict(ec); es0 = [e for e in ec3 if e[0] == 0]; ec3[es0[0]] = ec3[es0[1]]  # two edges at vertex 0 same color
    print("negative control (adjacent edges same color):", check_total_coloring(n, E, vc, ec3)[:2])
    assert not check_total_coloring(n, E, vc2, ec)[0] and not check_total_coloring(n, E, vc, ec2)[0] and not check_total_coloring(n, E, vc, ec3)[0]
    # graph6 round trip
    n6, E6 = tc.parse_graph6(tc.to_graph6(n, E))
    assert n6 == n and sorted(E6) == sorted(E)

    print("\n== encoder controls (known facts from arXiv:2609.05259 Sec. 2, 4, 5) ==")
    run("K4", *tc.K4(), expect_type=2, expect_equit=False)
    run("K3,3", *tc.K33(), expect_type=2, expect_equit=False)
    run("L6 prism", *tc.prism(3), expect_type=1, expect_equit=True)
    run("L8", *tc.prism(4), expect_type=1, expect_equit=True)
    run("L10", *tc.prism(5), expect_type=2, expect_equit=False)
    run("L12", *tc.prism(6), expect_type=1, expect_equit=True)
    run("L14", *tc.prism(7), expect_type=1, expect_equit=True)
    run("L18", *tc.prism(9), expect_type=1, expect_equit=True)
    run("Petersen", *tc.gpetersen(5, 2), expect_type=1, expect_equit=True)
    run("G(6,2)", *tc.gpetersen(6, 2), expect_type=1)
    run("G(9,2)", *tc.gpetersen(9, 2), expect_type=1)
    run("M8 Moebius", *tc.mobius(4), expect_type=2, expect_equit=False)
    run("M10 Moebius", *tc.mobius(5), expect_type=2, expect_equit=False)
    run("M12 Moebius", *tc.mobius(6), expect_type=2, expect_equit=False)
    run("M14 Moebius", *tc.mobius(7), expect_type=2, expect_equit=False)
    run("H16", 16, H16_E, expect_type=1, expect_equit=True)
    run("H18", 18, H18_E, expect_type=1, expect_equit=True)
    run("R", *tc.graph_R(), expect_type=1, expect_equit=False)
