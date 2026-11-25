---
name: findings-to-nanopubs
description: Turn reported findings into nanopublication assertions — subject, relation, object, polarity, qualifiers and an exact source range — serialised as JSON-LD with head, assertion, provenance and pubinfo graphs. Use when asked to structure claims, build a claim graph, or produce nanopublications.
---

# Findings to nanopublications

One sentence, one assertion, one range. The output is a JSON-LD document in which
every nanopublication carries the four graphs the format requires, and every
assertion can be traced to the characters it came from.

## One command

**Where to run it.** The scripts resolve their own paths, so they work from
any working directory. If your shell starts in `/app/work` (the contract's work
directory), call the absolute path of the script —
`python3 /skills/weekly-skill/scripts/run.py --input /input/case.json --output /app/output`
— or `cd` into the folder holding this `SKILL.md` first and use the relative form
below.

```bash
python3 scripts/run.py --input /input/case.json --output /app/output
```

## What it writes

| file | content |
|---|---|
| `nanopubs.jsonld` | `@graph` of nanopublications: `head`, `assertion`, `provenance`, `pubinfo` |
| `assertions.json` | the flat assertion table, easier to diff |
| `result.json` | `nanopubs`, `assertions`, `counts`, `evidence` |

An assertion is:

```json
{"subject": "Sparse routing", "relation": "reduces",
 "object": "inference cost by 0.7x on 32k-token contexts",
 "polarity": "positive", "qualifiers": {"context": "32k-token contexts"},
 "evidence": {"source": "inputs/findings.md", "char_start": 12, "char_end": 81,
              "quote": "…", "verified": true}}
```

## How the triple is read

1. **The first relation verb wins.** `Table 2 shows a 23.4% yield increase` is a
   statement about Table 2; taking the longest match would put the noun
   "increase" in the relation slot.
2. **Auxiliaries and negation are stripped from the subject.**
   `The router does not increase …` yields subject `The router`, not `The router
   does`.
3. **Polarity is explicit.** A negation cue before the relation, or a negative
   verb, gives `negative`. Nothing else is guessed.
4. **No verb in the closed set → no triple.** The assertion is still emitted with
   `confidence: unspecified` and listed under `uncertainty`, because a sentence
   that cannot be structured is a finding about the text, not a reason to drop it.

## Why the rules are few

An earlier attempt added direction rules for passive voice (guessing the agent)
and role checks for subject/object. On unseen text those rules misfired more often
than they fired, and every false triple costs more than a missing one. The rule
set here is deliberately small, and `polarity: null` is a legal, reported outcome.

## Failure handling

| situation | behaviour |
|---|---|
| no verb from the set | assertion without triple, `confidence: unspecified`, listed |
| negated claim | `polarity: negative` |
| sentence shorter than 30 chars | skipped as a claim candidate |
| no numeric or negated content | skipped (a claim needs something checkable) |
| empty input | `cannot_determine` |

## Limits

- Relations are surface verbs, not ontology terms; mapping to a vocabulary is a
  curation step this skill does not do.
- Passive sentences keep their grammatical subject; the agent is not inferred.
- A nominalised finding is read through the verb that introduces it.
