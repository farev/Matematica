"""Positive controls for the dpm engine. Every check here must pass before any
new value is trusted. Run: python3 controls.py

Anchors:
  * cyclic law d_pm(C_n) = floor(log2 n): proved in NOTE.md (Lemma L6) and
    matching the published D_pm(C_n) = floor(log2 n) + 1 (Adhikari et al.,
    (secondary) via search snippets, 2026-08-24).
  * D_pm(C_3+C_3+C_9) = 6: published value, (secondary) via search snippet.
  * d_pm(C_3+C_3) = 2: hand-computed in NOTE.md (four sign classes, all
    3-subsets checked by hand).
  * isomorphism invariance: C_15 vs C_3 x C_5, C_5 x C_15 vs C_15 x C_5 and
    vs C_5 x C_5 x C_3.
  * forced cells: groups where lower_d == upper_d must come out at that value.
"""

from dpm_core import AbelianGroup, search_dpm, floor_log2
import time

fails = 0


def check(label, got, want):
    global fails
    ok = got == want
    if not ok:
        fails += 1
    print(f"[{'ok' if ok else 'FAIL'}] {label}: got {got}, want {want}")


t0 = time.time()

# 1. cyclic law, exhaustive for n = 2..48 and straddling 2^6
for n in list(range(2, 49)) + [63, 64, 65]:
    r = search_dpm(AbelianGroup([n]))
    assert r["exhaustive"]
    check(f"C{n}", r["dpm"], floor_log2(n))

# 2. hand anchor C3+C3
r = search_dpm(AbelianGroup([3, 3]))
check("C3xC3 (hand)", r["dpm"], 2)

# 3. published anchor C3+C3+C9 -> D=6, d=5
r = search_dpm(AbelianGroup([3, 3, 9]))
check("C3xC3xC9 (published, secondary)", r["dpm"], 5)

# 4. forced small rank-2 cells (lower==upper): C5xC5, C3xC9, C2xC2, C4xC4
for mods, want in (([5, 5], 4), ([3, 9], 4), ([2, 2], 2), ([4, 4], 4), ([2, 4], 3)):
    G = AbelianGroup(mods)
    assert G.lower_d() == G.upper_d() == want, (mods, G.lower_d(), G.upper_d())
    r = search_dpm(G)
    check(f"{G.name()} (forced)", r["dpm"], want)

# 5. isomorphism invariance
a = search_dpm(AbelianGroup([15]))["dpm"]
b = search_dpm(AbelianGroup([3, 5]))["dpm"]
check("C15 == C3xC5", a, b)
a = search_dpm(AbelianGroup([5, 15]))["dpm"]
b = search_dpm(AbelianGroup([15, 5]))["dpm"]
c = search_dpm(AbelianGroup([5, 5, 3]))["dpm"]
check("C5xC15 == C15xC5", a, b)
check("C5xC15 == C5xC5xC3", a, c)

# 6. negative control: the engine must NOT accept a set with a signed zero-sum.
from dpm_core import verify_pm_zsf
ok, _ = verify_pm_zsf((5, 15), [(1, 0), (2, 0), (3, 0)])  # 1+2-3=0 mod 5... (1)+(2)=(3)
assert not ok, "negative control failed: (1,0),(2,0),(3,0) has 1+2-3=0"
print("[ok] negative control: signed zero-sum correctly detected")

print(f"\n{fails} failures; total {time.time()-t0:.1f}s")
raise SystemExit(1 if fails else 0)
