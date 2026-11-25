#!/usr/bin/env python3
"""Self-test for reading-14-nanopub."""
from __future__ import annotations
import json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import armkit as ak
import run as skill
PASS = FAIL = 0
def check(n, c, d=""):
    global PASS, FAIL
    if c: PASS += 1; print(f"  ok {n}" + (f" — {d}" if d else ""))
    else: FAIL += 1; print(f"  FAIL {n}" + (f" — {d}" if d else ""))
def main():
    print("reading-14 selftest")
    check("armkit pinned", bool(ak.VERSION), ak.VERSION)
    t = skill.triple("Sparse routing reduces inference cost by 0.7x.")
    check("subject", t and t["subject"] == "Sparse routing", str(t))
    check("relation", t and t["relation"] == "reduces")
    check("object keeps the qualifier", t and "0.7x" in t["object"], t and t["object"])
    t2 = skill.triple("The router does not increase perplexity.")
    check("negated subject is clean", t2 and t2["subject"] == "The router", str(t2))
    check("negation detected", skill.polarity("The router does not increase perplexity.", "increase") == "negative")
    t3 = skill.triple("Table 2 shows a 23.4% yield increase.")
    check("first verb wins", t3 and t3["relation"] == "shows", str(t3))
    with tempfile.TemporaryDirectory() as td:
        case = ak.CaseInput.load(os.path.join(ROOT, "examples", "case.json"))
        audit, res = ak.Audit("t"), ak.Result(td, "reading-14")
        ok = skill.solve(case, td, audit, res)
        doc = res.write(case, audit, ak.derive_status(audit, ok), "t", ak.utc_now(), ["selftest"])
        check("demo completes", ok)
        check("status success", doc["status"] == "success", doc["status"])
        check("every triple complete", doc["result"]["counts"]["triples"] == doc["result"]["counts"]["claims"])
        asrt = doc["result"]["assertions"]
        check("polarity explicit", all(a["polarity"] in ("positive", "negative") for a in asrt))
        check("four graphs per nanopub", all(set(n["head"]) == {"assertion", "provenance", "pubinfo"}
                                            for n in doc["result"]["nanopubs"]))
        check("jsonld written", os.path.isfile(os.path.join(td, "nanopubs.jsonld")))
        bad = [e for e in doc["evidence"] if not ak.verify_anchor(td, e["anchor"])[0]]
        check("anchors re-slice", not bad, f"{len(doc['evidence'])} anchors")
    print(f"\n{PASS} passed, {FAIL} failed")
    return 0 if FAIL == 0 else 1
if __name__ == "__main__":
    raise SystemExit(main())
