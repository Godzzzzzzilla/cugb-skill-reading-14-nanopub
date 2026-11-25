# reading-14-nanopub

Findings → nanopublication assertions with explicit polarity and a verified
source range. Submission for **阅读14｜Nanopublication** (product-arena-09).

## What is structured

Every sentence that carries a number or a negation becomes one assertion with
subject / relation / object, a polarity, its qualifiers, and a character range in
the source. The JSON-LD wrapper carries the four graphs a nanopublication needs.

## Measured on the bundled demo

| quantity | value |
|---|---|
| claim candidates | 6 |
| complete triples | 6 / 6 |
| explicit polarity | 6 / 6 |
| assertions re-slicing | 6 / 6 |
| four-graph wrappers | 6 / 6 |
| audit | 6/6, `status: success` |

Sample triples from the run:

| subject | relation | object | polarity |
|---|---|---|---|
| Sparse routing | reduces | inference cost by 0.7x … | positive |
| The router | increase | perplexity on the validation split | negative |
| Table 2 | shows | a 23.4% yield increase … | positive |

## Design note

Earlier work on this task added direction and voice rules and lost points: the
rules produced false triples. This version keeps the rule set small, makes
polarity explicit, and reports a sentence it cannot structure instead of forcing
one.

## Files

```
SKILL.md               what an agent loads
scripts/run.py         claim detection, triples, JSON-LD
scripts/verify.py      independent anchor verifier
scripts/selftest.py    14 checks
scripts/armkit.py      shared core
examples/case.json     demo input (six findings)
run/                   a real run
```

## Reproduce

```bash
python3 scripts/run.py --input examples/case.json --output /tmp/out
python3 scripts/verify.py --result /tmp/out/result.json
python3 scripts/selftest.py
```
