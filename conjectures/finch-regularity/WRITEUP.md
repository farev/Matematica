# Session narrative — 2026-08-02

Written as it happened, including the parts that went nowhere.

## The network was gone

First thing, per the mandate: check that the open literature is reachable.
It was not. `arxiv.org`, `oeis.org`, `erdosproblems.com`, `mathoverflow.net`,
`en.wikipedia.org`, `semanticscholar.org`, `doi.org`, `zbmath.org` — every one
of them returned **HTTP 403 on CONNECT** at the egress proxy. The proxy's own
status endpoint logged each refusal as `connect_rejected: gateway answered 403
(policy denial or upstream failure)`. Only `api.github.com` and
`raw.githubusercontent.com` answered, and GitHub access is scoped to this
repository alone, so the GitHub-hosted mirrors of the Erdős problem database and
of `formal-conjectures` were refused too.

WebSearch worked — it runs outside the sandbox — so I had *summaries* of the
literature but never a primary source. That single fact shaped the whole
session, and it is why every citation in `NOTE.md` is marked secondary and why
the novelty claim is hedged everywhere it appears.

## Three candidates, all killed by recon

I ran four recon agents in parallel while reading the repo.

**Lonely Runner Conjecture.** I picked it believing the frontier was 7 runners
(Barajas–Serra 2008). That was eighteen years stale. Rosenfeld proved 8 runners
in September 2025; Trakulthongchai 9 and 10 in November; Sungkawichai–
Trakulthongchai 11, 12 and 13 in April 2026. A group is shipping every two
months, the method is a prime-divisibility argument on top of a
linearly-exponential checking bound, and the last few primes for 8 runners took
"tens of hours" each. Four cores against that is not a contest. **Killed.**

**Cap sets in AG(n,3).** `a₇ ≥ 236` has not moved since Calderbank–Fishburn
1994; `a₈ ≥ 512` has not moved since FunSearch in December 2023, despite
AlphaEvolve, PatternBoost, X-evolve and FlowBoost all existing in the interim
and all having been pointed at extremal combinatorics. When four AI search
systems with industrial compute have failed to move a record for two and a half
years, four cores will not. **Killed.**

**Wilf's conjecture.** Genuinely open, and I liked it. But it has been verified
to genus 100 (Delgado–Eliahou–Fromentin 2025), and the structural wall is depth
`q = 4`, where — this is the decisive fact — the standard `W₀(S) ≥ 0` method
*provably* cannot work: near-misses with `W₀ = −1` exist at depth 4 with
arbitrarily large embedding dimension. So the bottleneck is an idea, not a
computation, and the field has four active groups. **Killed**, with regret.

The internal thread — closing the `(1,1,0)` relation class for additive squares
— was concrete but is a range-extension of an existing result, and the mandate
biases to the new. Logged, not chosen.

## What I actually chose, and why it was a good bet

While the recon agents ran, I went looking on my own and landed on 1-additive
sequences. The hook was mechanical rather than aesthetic. If `U(a,b)` has
finitely many even elements `E`, then for odd `x` a representation `x = u+v`
must have exactly one even summand, so

> `x ∈ U ⟺ #{e ∈ E : x−e ∈ U} = 1`

and the right-hand side reads only the window `[x−max E, x)`. A bounded window
means a deterministic finite automaton, and a repeated automaton state is a
*proof* that the sequence is periodic forever after. Almost nothing else I
considered all day had that property: a computation that terminates in a proof
rather than in evidence.

The reference generator reproduced Ulam's `U(1,2) = 1,2,3,4,6,8,11,13,16,18,26,…`
on the first run, and a C rewrite agreed with it on 121 `(a,b)` pairs at
`N = 20000`. Positive control in hand, I swept the landscape.

## The structure fell out immediately

`E(2,b) = {2, 2b+2}`. `E(4,b) = {4, 2b+4, 4b+4}`. `E(6,b) = {6, 2b+6, 4b+6,
6b+6, 16b}`. `E(8,b) = {8, …, 8b+8, 20b}`. The shape is `{a} ∪ {2jb+a : j ≤
a/2}`, plus for `a ≥ 6` one extra element `(2a+4)b`.

And then the anomaly. At `N = 10⁴`, `U(4,b)` had exactly three even elements for
every odd `b` — except `b = 7, 15, 31`, which had four. Those are `2^k − 1`. The
fourth elements were 206, 926, 3902; fitting a quadratic through them gave
`4b² + 2b − 4` exactly, and `b = 63` then predicted 15998 and delivered 15998.

I nearly published that off the small scan, which would have been a mistake:
`b = 63`'s extra element sits at 15998, *beyond* the `N = 10⁴` horizon, so the
first sweep was silently truncating. Rerunning every `b` to `6b² + 4000` fixed
it, and the final scan covers all 255 odd `b` in `[5, 513]` with no gaps:
exactly seven exceptions, `b = 2^k−1` for `k = 3..9`, always `4b²+2b−4`.

That anomaly turned out to be the point. Cassaigne–Finch prove `U(4,v)` regular
for `v ≡ 1 (mod 4)` via "precisely three even terms" *(secondary)* — and every
`2^k − 1` is `≡ 3 (mod 4)`. The exceptional family sits exactly in the residue
class their theorem omits. That is not a coincidence; it is the obstruction.

## What failed

**The first certificate was too strict.** I wrote condition (C) as "every even
residue class must be forced to have **≥ 2** representations". `U(4,5)` and
`U(4,9)` failed on classes 12, 20, 164 mod 192. I spent a while assuming a bug
in the residue arithmetic before seeing that the requirement is wrong, not the
code: I need `≠ 1`, and a class with **zero** forced representations is
perfectly good — such an even number is simply not in the sequence. One
character of logic; it took twenty minutes and it unlocked most of the table.

**The Python cycle detector filled to the horizon regardless.** It found the
cycle, then kept generating out to `horizon` before doing anything useful. Fixed
by filling only to `B`.

**Large windows beat the hash-table approach.** Storing every window state costs
memory proportional to the period; `U(4,7)` has `P = 11{,}301{,}098`, and the
Python version simply never got there. Rewriting the cycle search with Brent's
algorithm (O(1) memory) is what made the exceptional case reachable at all.

**`U(4,15)`, `U(4,31)`, `U(4,63)` are still not certified.** No window-state
cycle within the step budget. Their windows are `~4b²` bits wide. I do not know
whether their periods are astronomically large or whether the transients are
merely very long — `U(4,35)` has `X₁ = 1{,}666{,}723` with a period of only
5326, so long transients with short periods demonstrably happen.

**a = 20 and several `b ≡ 3 (mod 4)` cases ran out of budget** rather than
failing: `B` exceeded the memory cap, or Brent exceeded the step cap. Those are
resource limits, not mathematical obstructions, and they are recorded as such.

## The check that mattered most

Everything rests on the certificate being sound, so the failure mode I was most
worried about was a verifier that says PASS too easily. Two things guard it.

First, the C verifier is written from the statement of Theorem 1, not ported
from the Python — different cycle algorithm, independently re-derived residue
and finite checks. It agrees with the Python certifier on `E`, `P` and `|R|` in
**all 32 rows**. (`X₁` differs, because Brent finds the least valid one; any
valid `X₁` proves the theorem.)

Second, and more convincing: the certificate is *self-correcting*, and I have a
live demonstration. Run the verifier on `U(4,63)` with `X₀ = 4000` — below its
exceptional even element — and it does not quietly certify a false even set. It
rejects, with `even-15998-has-exactly-one-rep`, naming the exact element it was
missing. A verifier that catches its own truncation is worth more than one that
agrees with me.

A separate confirmation arrived from outside: one of the recon agents, told only
to read literature, wrote its own independent implementation to sanity-check a
snippet it distrusted, and reported back the same exceptional family
(`4v²+2v−4` at `v = 7,15,31,63,127`) and the same eight (period, fundamental
difference) pairs I had. Different code, different author, same numbers.

## Where it landed

Theorem 1 proved; 32 sequences certified, 20 of them in cases reported open;
the exceptional family pinned across 255 values of `b`; a 2-adic period law
`P = 2^{⌊log₂(b−1)⌋+3}(b+1)` that holds for all twelve tested `b ≡ 1 (mod 4)`
and, awkwardly for the clean story, also for `b = 19`.

That last detail is worth keeping in view. The tidy version of this session
would say "`b ≡ 1 (mod 4)` is smooth, `b ≡ 3 (mod 4)` is wild". `b = 19` says
the real dichotomy is something else, and I do not know what it is.

The honest summary of the novelty is narrower than the result count suggests:
Theorem 1 is almost certainly a certificate-carrying restatement of Finch's 1992
criterion, and I have not read Finch's tables — they are on a page I could not
open. The 20 new cases and the exceptional family are what I would defend, and
even those are hedged until someone reads the primary sources.
