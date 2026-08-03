import sys, json, time
from cert2 import certify
from ulam import ulam
a = int(sys.argv[1]); bs = [int(x) for x in sys.argv[2].split(',')]
H = int(float(sys.argv[3])) if len(sys.argv) > 3 else 3000000
for b in bs:
    probe = ulam(a, b, max(3000, 60*(a+1)*b))
    Ep = [x for x in probe if x % 2 == 0]
    W = max(Ep) if Ep else 0
    X0 = max(4000, 6*W)
    t0 = time.time()
    try:
        r = certify(a, b, X0=X0, horizon=H)
    except Exception as ex:
        r = {"ok": False, "why": f"exception {type(ex).__name__}: {ex}"}
    r['a']=a; r['b']=b; r['secs']=round(time.time()-t0,1)
    print(json.dumps(r)); sys.stdout.flush()
