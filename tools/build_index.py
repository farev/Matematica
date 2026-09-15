#!/usr/bin/env python3
"""Emit ATTEMPTED.md: the compact index of every conjecture attempted here.

Exists so a research session can learn what has already been tried without
reading 32 conjecture READMEs and 38 log entries (about 166k tokens). The
index costs roughly 1k.

It covers unmerged branches on purpose. Six problems have been attacked only
on branches that never landed, and a session that consults main alone cannot
see them; that blind spot is what produced six independent attacks on the
same Davenport problem in August 2026.

Run from the repository root:

    python3 tools/build_index.py             # writes ATTEMPTED.md
    python3 tools/build_index.py --stdout    # prints it, writes nothing

Reads the working tree, log/ filenames and `git branch -r --no-merged`.
Never edit ATTEMPTED.md by hand.

Use --stdout from a research session. Every session that regenerated the
file in place would record its own date and commit in the header, so every
branch would carry a different ATTEMPTED.md and every merge would conflict
on it. Printing instead keeps the working tree clean and leaves nothing to
commit.
"""

import collections
import glob
import os
import re
import subprocess
import sys

LABELS = ("PROVED", "CERTIFIED", "NUMERICAL")

# Hand-maintained. Directory names alone cannot tell that these are one
# problem, so the tangles found by hand get recorded here. Key is the
# canonical name; values are directory names seen in the wild.
ALIASES = {
    "Erdos #699 (binomial gcd)": ["erdos-699", "binomial-gcd"],
    "plus/minus Davenport": [
        "plus-minus-davenport", "plusminus-davenport", "pm-davenport",
    ],
}

# Slugs that are a second same-day session, not a separate problem.
LOG_SUFFIXES = re.compile(r"-(r\d+|part\d+|session\d+)$")


def sh(*args):
    try:
        out = subprocess.run(
            args, capture_output=True, text=True, timeout=60, check=False
        )
        return out.stdout if out.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def sessions_from_logs():
    """Attempt record, keyed by slug. Filenames only, so this is cheap."""
    by_slug = collections.defaultdict(list)
    for path in sorted(glob.glob("log/*.md")):
        name = os.path.basename(path)[:-3]
        m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)$", name)
        if not m:
            continue
        date, slug = m.group(1), LOG_SUFFIXES.sub("", m.group(2))
        by_slug[slug].append(date)
    return by_slug


def read_conjecture(slug):
    """Status keyword and result labels from one conjecture README."""
    path = os.path.join("conjectures", slug, "README.md")
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError:
        return "?", []

    # Both "**Status:**" and the older "**Status.**" spelling occur.
    m = re.search(r"^\*\*Status[:.]\*\*\s*(.+)$", text, re.M)
    status = "?"
    if m:
        # The field has drifted into carrying whole clauses. Keep the leading
        # vocabulary word and drop the commentary. Anything outside the
        # vocabulary stays "?", which usefully flags a README that has
        # drifted from TEMPLATE.md rather than papering over it.
        head = re.split(r"[—(,\-]", m.group(1).strip())[0].strip().lower()
        status = head if head in ("active", "parked", "closed") else "?"

    # Prefer the Results sections, whose headings often carry an annotation
    # ("## Results (2026-08-09 session)") and which may run to end of file.
    # The oldest READMEs predate TEMPLATE.md and have no sections at all, so
    # fall back to the whole file rather than reporting no results for a
    # conjecture that plainly has them.
    secs = re.findall(
        r"^##\s*Results\b.*?$(.*?)(?=^##\s|\Z)", text, re.M | re.S
    )
    body = "".join(secs) if secs else text
    found = [lab for lab in LABELS if lab in body]
    return status, found


def branch_only_dirs():
    """Conjecture directories that exist on some unmerged branch but not main."""
    on_main = {
        os.path.basename(d)
        for d in glob.glob("conjectures/*")
        if os.path.isdir(d)
    }
    # An empty --no-merged result means one of two very different things:
    # every branch has landed, or this clone has no remote branch refs at
    # all (a shallow or single-branch sandbox clone). Reporting the second
    # as "all clear" would be exactly the false reassurance that keeps the
    # duplication loop running, so check that refs exist first.
    if not sh("git", "rev-parse", "--verify", "origin/main").strip():
        return None, on_main
    if len([b for b in sh("git", "branch", "-r").splitlines()
            if "origin/claude/" in b]) == 0:
        return None, on_main
    raw = sh("git", "branch", "-r", "--no-merged", "origin/main")

    found = collections.defaultdict(lambda: {"branches": [], "dates": []})
    for line in raw.splitlines():
        branch = line.strip()
        if not branch.startswith("origin/claude/"):
            continue
        short = branch[len("origin/"):]
        names = sh("git", "diff", "--name-only", f"origin/main...{branch}",
                   "--", "conjectures/")
        date = sh("git", "log", "-1", "--format=%ad", "--date=short",
                  branch).strip()
        slugs = {
            p.split("/")[1] for p in names.splitlines()
            if p.startswith("conjectures/") and len(p.split("/")) > 2
        }
        for slug in slugs - on_main:
            found[slug]["branches"].append(short)
            found[slug]["dates"].append(date)
    return found, on_main


def group_branch_slugs(found):
    """Fold directory-name variants of one problem into a single row."""
    canon = {}
    for name, variants in ALIASES.items():
        for v in variants:
            canon[v] = name

    groups = collections.defaultdict(
        lambda: {"slugs": [], "branches": [], "dates": []}
    )
    for slug, info in found.items():
        # Fall back to the last hyphen-separated token, which catches
        # spelling drift like plus-minus-/plusminus-/pm- on one subject.
        key = canon.get(slug) or slug.rsplit("-", 1)[-1]
        g = groups[key]
        g["slugs"].append(slug)
        g["branches"].extend(info["branches"])
        g["dates"].extend(info["dates"])

    # The token fallback only earns a name of its own when it actually
    # merged two spellings. A lone directory is named by its own slug, so
    # the table never shows a bare word like "walks" as a problem name.
    named = {}
    for key, g in groups.items():
        slugs = sorted(set(g["slugs"]))
        named[key if (key in ALIASES or len(slugs) > 1) else slugs[0]] = g
    return named


def main():
    if not os.path.isdir("conjectures") or not os.path.isdir("log"):
        sys.exit("run from the repository root")

    logs = sessions_from_logs()
    found, on_main = branch_only_dirs()

    rows = []
    for slug in sorted(on_main):
        if slug == "TEMPLATE.md":
            continue
        status, labels = read_conjecture(slug)
        dates = sorted(logs.get(slug, []))
        count = len(dates) if dates else 1
        last = dates[-1] if dates else "no log"
        rows.append((slug, status, count, last, " ".join(labels) or "-"))

    head = sh("git", "rev-parse", "--short", "HEAD").strip() or "unknown"
    today = sh("date", "+%Y-%m-%d").strip()

    out = []
    out.append("# Attempted conjectures\n")
    out.append(
        "Generated by [`tools/build_index.py`](tools/build_index.py). "
        "Do not edit by hand.\n"
    )
    out.append(
        "**Read this instead of sweeping `conjectures/` and `log/`.** Every "
        "problem attempted here is in one of the two tables below. A problem "
        "absent from both is genuinely new; a problem present in either has "
        "been attacked and is taken.\n"
    )
    out.append(
        "`labels claimed` lists which of PROVED / CERTIFIED / NUMERICAL "
        "appear in that conjecture's own README. It is a routing hint, not a "
        "ranking: it does not say which result is strongest, and it carries "
        "no verification of its own. Read the conjecture README before "
        "repeating any of it. `status` is `?` where the README has drifted "
        "from `conjectures/TEMPLATE.md` and states no parseable status, and "
        "`last` is `no log` where a session left no `log/` entry; both are "
        "real defects this index surfaces rather than hides.\n"
    )
    out.append(f"Generated {today} from main at `{head}`. "
               f"{len(rows)} on main, "
               f"{sum(len(v['slugs']) for v in group_branch_slugs(found).values()) if found else 0}"
               " attempted only on unmerged branches.\n")

    out.append(f"\n## On main ({len(rows)})\n")
    out.append("| conjecture | status | sessions | last | labels claimed |")
    out.append("|---|---|---|---|---|")
    for slug, status, count, last, labels in rows:
        out.append(
            f"| [{slug}](conjectures/{slug}/) | {status} | {count} | "
            f"{last} | {labels} |"
        )

    out.append("\n## Attempted but not on main\n")
    if found is None:
        out.append(
            "> Branch data unavailable (no git, or no `origin/main`). This "
            "section is incomplete, so do not treat absence here as proof a "
            "problem is untouched.\n"
        )
    elif not found:
        out.append("None. Every attempted problem has landed on main.\n")
    else:
        groups = group_branch_slugs(found)
        out.append(
            "These have been attacked, but the work sits on branches that "
            "never merged, so they do **not** appear in `conjectures/` on "
            "main. Treat them as taken. Where one problem carries several "
            "directory names, that is the same tangle being re-attacked "
            "under a new spelling.\n"
        )
        out.append("| problem | directory names used | branches | last |")
        out.append("|---|---|---|---|")
        for key in sorted(groups):
            g = groups[key]
            names = ", ".join(f"`{s}`" for s in sorted(set(g["slugs"])))
            n = len(set(g["branches"]))
            last = max(g["dates"]) if g["dates"] else "?"
            out.append(f"| {key} | {names} | {n} | {last} |")

    text = "\n".join(out) + "\n"
    if "--stdout" in sys.argv[1:]:
        sys.stdout.write(text)
        return
    with open("ATTEMPTED.md", "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"wrote ATTEMPTED.md: {len(rows)} on main, "
          f"{len(found) if found else 0} branch-only directories")


if __name__ == "__main__":
    main()
