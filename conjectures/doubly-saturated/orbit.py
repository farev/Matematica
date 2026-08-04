# Are the nine n=19 hits one isomorphism class?  Multiplier maps x -> a*x are graph isomorphisms
# of circulants, sending S to a*S.  Compute the orbit of {1,3,5,6} under Z_19^*.
n = 19
def norm(S):  return tuple(sorted(min(d % n, (-d) % n) for d in S))
base = norm([1,3,5,6])
orb = sorted({ norm([a*d for d in base]) for a in range(1, n) })
print("orbit size:", len(orb))
for S in orb: print("   S =", S)
