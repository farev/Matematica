import numpy as np, time
from verify_big import gaps_up_to_segmented
from microscope_bench import run_lengths, equal_value_runs, two_valued_max
t0 = time.time()
g = gaps_up_to_segmented(10**10).astype(np.int64)[1:]
print(f"gaps ready ({time.time()-t0:.0f}s)", flush=True)
L_cpap = equal_value_runs(g)
h = np.abs(np.diff(g)); eqh = (h[1:]==h[:-1]) & (h[1:]!=0)
L_dconst = int(run_lengths(eqh).max())+2
L_par0 = int(run_lengths(g%4==0).max()); L_par2 = int(run_lengths(g%4==2).max())
L_2val = two_valued_max(g)
lg = np.log(1e10)
print(f"x=10^10: L_cpap={L_cpap} (CPAP of {L_cpap+1} primes, {L_cpap/lg:.2f} log x)")
print(f"L_dconst={L_dconst} L_par0={L_par0} L_par2={L_par2} ({L_par2/lg:.2f} log x) L_2val={L_2val}")
