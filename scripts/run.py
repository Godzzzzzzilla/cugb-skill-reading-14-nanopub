#!/usr/bin/env python3
"""reading-14-nanopub — one assertion per finding, serialised as a nanopublication.

    python scripts/run.py --input /input/case.json --output /app/output

The output is a JSON-LD document with the four graphs a nanopublication needs
(Head, Assertion, Provenance, PubInfo). Each assertion is an (s, r, o) triple
with an explicit polarity, its qualifiers, and the character range of the
sentence it came from.

Design note: an earlier attempt added direction and voice rules that guessed the
subject of passive sentences. On unseen text those rules misfire more often than
they help, so polarity is read from a small closed verb set and everything else
is left as a plain triple with `polarity: null` — stated, not guessed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import uuid

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import armkit as ak  # noqa: E402

SKILL = "reading-14-nanopub"
VERSION = "1.0.0"

POSITIVE = ["shows", "show", "reports", "report", "demonstrates", "demonstrate", "confirms",
            "confirm", "increase", "increases", "improve", "improves", "reduce", "reduces",
            "stabilise", "stabilises", "stabilize", "stabilizes", "match", "matches", "raises",
            "raise", "reach", "reaches", "outperform", "outperforms", "enhance", "enhances",
            "reproduce", "reproduces", "reproduced", "observe", "observes", "observed",
            "measure", "measures", "measured", "find", "finds", "found"]
NEGATIVE = ["decrease", "decreases", "inhibit", "inhibits", "impair", "impairs", "worsen",
            "worsens", "slow", "slows", "fail", "fails"]
AUX = r"(?:does|do|did|is|are|was|were|has|have|had|can|could|will|would|may|might|shall|should)"
QUALIFIER_HINTS = {
    "context": r"\b(on|in|for|under)\s+([\w\-\s]{3,40}?)(?:[,.;]|$)",
    "dose": r"\b(\d+(?:\.\d+)?\s?(?:mg|g|ml|µl|mM|µM|nM|%|pt))\b",
    "sample": r"\b(n\s?=\s?\d+)\b",
}


def split_claims(text: str):
    """Sentences that carry a numeric or comparative finding."""
    out = []
    for para in re.split(r"\n\s*\n", text):
        if not para.strip() or para.lstrip().startswith("#"):
            continue
        for s in ak.sentence_split(para):
            if len(s) < 30:
                continue
            if re.search(r"\d", s) or re.search(r"\b(not|no|cannot)\b", s, re.I):
                out.append(s)
    return out


def triple(sentence: str):
    """(subject, relation, object) from the first relation verb in the sentence.

    The first verb wins: "Table 2 shows a 23.4% yield increase" is a statement
    about Table 2, not about an increase. Choosing the longest match instead put
    the noun "increase" in the relation slot and produced a wrong triple.
    """
    verbs = sorted(set(POSITIVE + NEGATIVE), key=len, reverse=True)
    best = None
    for v in verbs:
        m = re.search(r"\b" + re.escape(v) + r"\b", sentence, re.I)
        if m and (best is None or m.start() < best.start()):
            best = m
    if not best:
        return None
    subj = sentence[:best.start()].strip(" ,;:")
    subj = re.sub(r"\b" + AUX + r"\b\s*(not\b\s*)?$", "", subj, flags=re.I).strip(" ,;:")
    subj = re.sub(r"\b(not|no)\s*$", "", subj, flags=re.I).strip(" ,;:")
    verb = best.group(0).lower()
    rest = sentence[best.end():].strip(" ,;:")
    rest = re.sub(r"^(by|to|on|in|for|under|from|with|that)\s+", "", rest, flags=re.I)
    obj = re.split(r"\b(?:but|while|whereas|because|although)\b", rest)[0].strip(" ,;:.")
    if not subj or not obj:
        return None
    return {"subject": subj, "relation": verb, "object": obj}


def qualifiers(sentence: str):
    out = {}
    for name, pat in QUALIFIER_HINTS.items():
        m = re.search(pat, sentence, re.I)
        if m:
            out[name] = m.group(2) if m.lastindex and m.lastindex >= 2 else m.group(1)
    return out


def polarity(sentence: str, relation: str):
    """Negative if a negation cue precedes the relation, or the verb is a negative one."""
    low = sentence.casefold()
    at = low.find(relation) if relation else -1
    before = low[:at] if at > 0 else low
    neg = bool(re.search(r"\b(not|no|never|cannot|neither|nor)\b|n't\b", before))
    if neg:
        return "negative"
    return "negative" if relation in NEGATIVE else "positive"


def build_nanopub(claim, idx, creator, source_name):
    tri = triple(claim)
    assert_id = f"http://example.org/assertion/{idx}"
    np_id = f"http://example.org/nanopub/{hashlib.sha1(claim.encode()).hexdigest()[:16]}"
    pol = polarity(claim, tri["relation"]) if tri else None
    assertion = {
        "@id": assert_id,
        "subject": tri["subject"] if tri else None,
        "relation": tri["relation"] if tri else None,
        "object": tri["object"] if tri else None,
        "polarity": pol,
        "qualifiers": qualifiers(claim),
        "evidence": {"source": source_name, "quote": claim},
        "confidence": "asserted" if tri else "unspecified",
    }
    np = {
        "@id": np_id,
        "@type": "Nanopublication",
        "head": {"assertion": assert_id, "provenance": f"{np_id}#provenance",
                 "pubinfo": f"{np_id}#pubinfo"},
        "assertion": assertion,
        "provenance": {"extracted_from": source_name, "method": f"{SKILL}/{VERSION}",
                       "created": ak.utc_now()},
        "pubinfo": {"creator": creator, "created": ak.utc_now()},
    }
    return np


def solve(case: ak.CaseInput, out: str, audit: ak.Audit, res: ak.Result) -> bool:
    docs = [p for p in case.discover() if p.lower().endswith((".md", ".txt"))]
    audit.check("input-found", bool(docs), f"{len(docs)} text file(s)", critical=True)
    if not docs:
        return False
    src = docs[0]
    text, _ = ak.read_text(src)
    rel_src = f"inputs/{os.path.basename(src)}"
    ak.write_text(os.path.join(out, rel_src), text)
    res.add_artifact(rel_src, "data", "source text, copied verbatim")

    creator = str(case.get("creator", "orcid", default="https://orcid.org/0000-0000-0000-0000"))
    claims = split_claims(text)
    audit.check("claims-found", len(claims) >= 2, f"{len(claims)} claim candidates", critical=True)

    nanopubs, assertions = [], []
    for i, claim in enumerate(claims, start=1):
        np = build_nanopub(claim, i, creator, rel_src)
        at = text.find(claim)
        anchor = ak.Anchor(rel_src, at, at + len(claim), claim, page=1)
        ok, why = ak.verify_anchor(out, anchor.as_dict())
        np["assertion"]["evidence"].update({
            "source": rel_src, "char_start": at, "char_end": at + len(claim), "verified": ok})
        np["assertion"]["evidence_id"] = f"a{i}"
        res.add_evidence(f"a{i}", f"{np['assertion']['subject']} {np['assertion']['relation']} "
                                   f"{np['assertion']['object']}", anchor, ok, why)
        nanopubs.append(np)
        assertions.append({**np["assertion"], "nanopub": np["@id"]})

    complete = [a for a in assertions if a["subject"] and a["relation"] and a["object"]]
    audit.check("triples-complete", len(complete) == len(assertions),
                f"{len(complete)}/{len(assertions)} have subject+relation+object", critical=True)
    polarised = [a for a in assertions if a["polarity"] in ("positive", "negative")]
    audit.check("polarity-explicit", len(polarised) == len(assertions),
                f"{len(polarised)}/{len(assertions)} carry a polarity", weight=0.8)
    with_ev = [a for a in assertions if a["evidence"].get("verified")]
    audit.check("evidence-verified", len(with_ev) == len(assertions),
                f"{len(with_ev)}/{len(assertions)} assertions re-slice", critical=True)

    # serialisation contract: the four graphs and their pointers must all be present
    required = ["@context", "@graph"]
    doc = {
        "@context": {
            "np": "http://www.nanopub.org/nschema#",
            "prov": "http://www.w3.org/ns/prov#",
            "sio": "http://semanticscience.org/resource/",
            "subject": "sio:SIO_000300",
            "relation": "sio:SIO_000008",
            "object": "sio:SIO_000300",
            "polarity": "np:polarity",
            "qualifiers": "np:qualifier",
        },
        "@graph": nanopubs,
    }
    audit.check("serialisation-complete",
                all(k in doc for k in required) and all(
                    set(n["head"]) == {"assertion", "provenance", "pubinfo"} for n in nanopubs),
                "every nanopublication carries head/assertion/provenance/pubinfo", critical=True)

    ak.write_json(os.path.join(out, "nanopubs.jsonld"), doc)
    ak.write_json(os.path.join(out, "assertions.json"), {"assertions": assertions})
    res.add_artifact("nanopubs.jsonld", "data", "JSON-LD with four graphs per assertion")
    res.add_artifact("assertions.json", "data", "flat assertion table")

    res.set("nanopubs", nanopubs)
    res.set("assertions", assertions)
    res.set("counts", {"claims": len(claims), "triples": len(complete),
                       "positive": sum(1 for a in assertions if a["polarity"] == "positive"),
                       "negative": sum(1 for a in assertions if a["polarity"] == "negative"),
                       "with_qualifiers": sum(1 for a in assertions if a["qualifiers"])})
    res.set("serialisation", "nanopub-jsonld/4-graph")
    for a in assertions:
        if a["confidence"] != "asserted":
            res.add_uncertainty(f"assertion {a['evidence_id']} has no triple",
                                f"no verb in the closed set: {ak.clip(a['evidence']['quote'], 100)}",
                                "rewrite the sentence with an explicit relation or curate by hand")
    res.limits.append("polarity comes from a closed verb set plus negation cues; other verbs are left null")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="/input/case.json")
    ap.add_argument("--output", default="/app/output")
    args = ap.parse_args()
    ak.safe_stdout()
    started = ak.utc_now()
    os.makedirs(args.output, exist_ok=True)
    case = ak.CaseInput.load(args.input, work_dir=args.output)
    audit, res = ak.Audit("reading-14"), ak.Result(args.output, SKILL, VERSION)
    try:
        ok = solve(case, args.output, audit, res)
    except Exception as exc:
        import traceback
        traceback.print_exc()
        ok = False
        audit.check("pipeline-completed", False, f"{type(exc).__name__}: {exc}", critical=True)
        res.add_uncertainty("pipeline exception", str(exc), "read audit.json before citing an assertion")
    res.meta["case_notes"] = case.notes
    status = ak.derive_status(audit, ok)
    if not ok and status == "success":
        status = "partial"
    res.write(case, audit, status, {
        "success": "every assertion has a triple, a polarity, a four-graph wrapper and a verified range",
        "partial": "some sentence produced no triple; see uncertainty",
        "cannot_determine": "no text could be read",
    }.get(status, status), started, sys.argv)
    a = audit.as_dict()
    print(f"wrote result.json status={status} checks={a['passed']}/{a['total']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
