#!/usr/bin/env python3
"""Certified boundary pairs for conjectured generalized Schur values.

For each triple (s,t,u) with conjectured value N = s*t*u - t*u - u - 1
(Ahmed-Schaal Conjecture 2.1), run the full certificate protocol:

  1. UNSAT at N   : Glucose42 with DRUP proof, checked by the independent
                    C checker rup_check (tools/satcert). Proves S <= N.
  2. SAT at N-1   : witness coloring, checked by verify_witness.py
                    (independent bitset algorithm). Proves S > N-1.
  Together: S(3;s,t,u) = N, every step certified.

If step 1 comes back SAT instead, the conjecture is REFUTED at (s,t,u):
the witness is verified and saved, and the driver climbs upward to locate
the true value (certifying the eventual boundary).

Artifacts per triple, written to certs/:
  s{s}_{t}_{u}_n{N}.drup       DRUP proof of UNSAT at N
  s{s}_{t}_{u}_n{N-1}.witness  verified coloring of [1,N-1]
CNF files are NOT stored (tens of MB): the encoder is deterministic, so
`python3 schur3.py s,t,u N` regenerates them byte-identically; results.csv
records each CNF's SHA-256.

Usage: new_values.py 4,4,10 4,5,8 ...      (each triple runs sequentially)
"""
import csv, hashlib, os, subprocess, sys, time
from schur3 import decide, encode, write_witness, rup_check


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_wit(path):
    here = os.path.dirname(os.path.abspath(__file__))
    r = subprocess.run([sys.executable, os.path.join(here, "verify_witness.py"), path],
                       capture_output=True, text=True)
    return r.returncode == 0, r.stdout.strip()


def boundary_pair(ts, N, certdir="certs", results="data/results.csv"):
    tag = "s" + "_".join(map(str, ts))
    os.makedirs(certdir, exist_ok=True)
    row = {"triple": ",".join(map(str, ts)), "conjectured": N}

    t0 = time.time()
    res, aux = decide(ts, N, certdir, tag, proof=True, solver="glucose")
    row["unsat_time_s"] = round(time.time() - t0, 1)

    if res == "SAT":
        # conjecture refuted at this triple: verify + save witness, then climb
        wf = os.path.join(certdir, f"{tag}_n{N}.witness")
        write_witness(wf, ts, N, aux)
        ok, msg = verify_wit(wf)
        print(f"{ts} REFUTATION: SAT at conjectured N={N}; witness {'OK' if ok else 'BAD'}", flush=True)
        row.update(verdict="REFUTED_AT_N", S="", rup="", witness="OK" if ok else "BAD")
        _append(results, row)
        n = N + 1
        while True:
            t1 = time.time()
            res2, aux2 = decide(ts, n, certdir, tag, proof=True, solver="glucose")
            el = round(time.time() - t1, 1)
            if res2 == "SAT":
                print(f"{ts} n={n} SAT {el}s (climbing)", flush=True)
                n += 1
                continue
            ok2, _ = rup_check(*aux2)
            print(f"{ts} TRUE VALUE S={n} rup={'VERIFIED' if ok2 else 'FAIL'} {el}s", flush=True)
            sha = sha256_file(aux2[0]); os.remove(aux2[0])
            row2 = {"triple": row["triple"], "conjectured": N, "verdict": "TRUE_VALUE",
                    "S": n, "unsat_time_s": el, "rup": "VERIFIED" if ok2 else "FAIL",
                    "witness": "", "cnf_sha256": sha}
            _append(results, row2)
            return

    assert res == "UNSAT"
    ok, msg = rup_check(*aux)
    row["rup"] = "VERIFIED" if ok else "FAIL"
    cnffile, prooffile = aux
    row["proof_bytes"] = os.path.getsize(prooffile)
    row["cnf_sha256"] = sha256_file(cnffile)
    os.remove(cnffile)  # regenerable (deterministic encoder); too big to keep

    t0 = time.time()
    res2, aux2 = decide(ts, N - 1, certdir, tag, proof=False, solver="glucose")
    row["sat_time_s"] = round(time.time() - t0, 1)
    assert res2 == "SAT", f"{ts}: UNSAT at N-1={N-1}?! conjecture value wrong on the low side"
    wf = os.path.join(certdir, f"{tag}_n{N-1}.witness")
    write_witness(wf, ts, N - 1, aux2)
    ok2, msg2 = verify_wit(wf)
    row["witness"] = "OK" if ok2 else "BAD"
    row["verdict"] = "CONFIRMED" if (ok and ok2) else "CERT_INCOMPLETE"
    row["S"] = N
    _append(results, row)
    print(f"{ts} S={N} {row['verdict']} unsat={row['unsat_time_s']}s "
          f"sat={row['sat_time_s']}s proof={row['proof_bytes']}B rup={row['rup']} wit={row['witness']}", flush=True)


def _append(path, row):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    exists = os.path.exists(path)
    cols = ["triple", "conjectured", "verdict", "S", "unsat_time_s", "sat_time_s",
            "proof_bytes", "rup", "witness", "cnf_sha256"]
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        if not exists:
            w.writeheader()
        w.writerow(row)


if __name__ == "__main__":
    results = os.environ.get("RESULTS", "data/results.csv")
    for arg in sys.argv[1:]:
        ts = tuple(int(x) for x in arg.split(","))
        s, t, u = ts
        N = s * t * u - t * u - u - 1
        boundary_pair(ts, N, results=results)
