# result.json and nanopubs.jsonld

`result`:
- `nanopubs[]` — `{@id, @type, head{assertion,provenance,pubinfo}, assertion, provenance, pubinfo}`.
- `assertions[]` — the flat form: `{subject, relation, object, polarity, qualifiers, evidence, confidence, evidence_id, nanopub}`.
- `counts` — `{claims, triples, positive, negative, with_qualifiers}`.
- `serialisation` — `nanopub-jsonld/4-graph`.

`nanopubs.jsonld` adds an `@context` mapping `np`, `prov`, `sio` and the four
assertion slots. `head` must name all three other graphs; the audit checks it.

`polarity` ∈ `positive` | `negative` | `null`. `null` only appears when no triple
was found, and the assertion is then listed under `uncertainty`.
