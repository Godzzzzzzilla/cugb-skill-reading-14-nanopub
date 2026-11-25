# reading-14-nanopub — case demo-nanopub-01

- status: **success** (every assertion has a triple, a polarity, a four-graph wrapper and a verified range)
- checks: 6/6 passed, ratio=1.0
- evidence: 6 anchored claims
- finished: 2026-11-25T07:55:04Z

## Result

```json
{
 "nanopubs": [
  {
   "@id": "http://example.org/nanopub/5bb7f72e95a57bf2",
   "@type": "Nanopublication",
   "head": {
    "assertion": "http://example.org/assertion/1",
    "provenance": "http://example.org/nanopub/5bb7f72e95a57bf2#provenance",
    "pubinfo": "http://example.org/nanopub/5bb7f72e95a57bf2#pubinfo"
   },
   "assertion": {
    "@id": "http://example.org/assertion/1",
    "subject": "Sparse routing",
    "relation": "reduces",
    "object": "inference cost by 0.7x on 32k-token contexts",
    "polarity": "positive",
    "qualifiers": {
     "context": "32k-token contexts"
    },
    "evidence": {
     "source": "inputs/findings.md",
     "quote": "Sparse routing reduces inference cost by 0.7x on 32k-token contexts.",
     "char_start": 12,
     "char_end": 80,
     "verified": true
    },
    "confidence": "asserted",
    "evidence_id": "a1"
   },
   "provenance": {
    "extracted_from": "inputs/findings.md",
    "method": "reading-14-nanopub/1.0.0",
    "created": "2026-11-25T07:55:04Z"
   },
   "pubinfo": {
    "creator": "https://orcid.org/0000-0000-0000-0000",
    "created": "2026-11-25T07:55:04Z"
   }
  },
  {
   "@id": "http://example.org/nanopub/4494959e0a557674",
   "@type": "Nanopublication",
   "head": {
    "assertion": "http://example.org/assertion/2",
    "provenance": "http://example.org/nanopub/4494959e0a557674#provenance",
    "pubinfo": "http://example.org/nanopub/4494959e0a557674#pubinfo"
   },
   "assertion": {
    "@id": "http://example.org/assertion/2",
    "subject": "The router",
    "relation": "increase",
    "object": "perplexity on the validation split",
    "polarity": "negative",
    "qualifiers": {
     "context": "the validation split"
    },
    "evidence": {
     "source": "inputs/findings.md",
     "quote": "The router does not increase perplexity on the validation split.",
     "char_start": 81,
     "char_end": 145,
     "verified": true
    },
    "confidence": "asserted",
    "evidence_id": "a2"
   },
   "provenance": {
    "extracted_from": "inputs/findings.md",
    "method": "reading-14-nanopub/1.0.0",
    "created": "2026-11-25T07:55:04Z"
   },
   "pubinfo": {
    "creator": "https://orcid.org/0000-0000-0000-0000",
    "created": "2026-11-25T07:55:04Z"
   }
  },
  {
   "@id": "http://example.org/nanopub/faf2dd92bda9ef02",
   "@type": "Nanopublication",
   "head": {
    "assertion": "http://example.org/assertion/3",
    "provenance": "http://example.org/nanopub/faf2dd92bda9ef02#provenance",
    "pubinfo": "http://example.org/nanopub/faf2dd92bda9ef02#pubinfo"
   },
   "assertion": {
    "@id": "http://example.org/assertion/3",
    "subject": "Block-sparse attention",
    "relation": "improves",
    "object": "recall by 3.2 points over dense attention in our reproduction",
    "polarity": "positive",
    "qualifiers": {
     "context": "our reproduction"
    },
    "evidence": {
     "source": "inputs/findings.md",
     "quote": "Block-sparse attention improves recall by 3.2 points over dense attention in our reproduction.",
     "char_start": 146,
     "char_end": 240,
     "verified": true
    },
    "confidence": "asserted",
    "evidence_id": "a3"
   },
   "provenance": {
    "extracted_from": "inputs/findings.md",
    "method": "reading-14-nanopub/1.0.0",
    "created": "2026-11-25T07:55:04Z"
   },
   "pubinfo": {
    "creator": "https://orcid.org/0000-0000-0000-0000",
    "created": "2026-11-25T07:55:04Z"
   }
  },
  {
   "@id": "http://example.org/nanopub/4e077ac1156f02a8",
   "@type": "Nanopublication",
   "head": {
    "assertion": "http://example.org/assertion/4",
    "provenance": "http://example.org/nanopub/4e077ac1156f02a8#provenance",
    "pubinfo": "http://example.org/nanopub/4e077ac1156f02a8#pubinfo"
   },
   "assertion": {
    "@id": "http://example.org/assertion/4",
    "subject": "Dropout of 0.1",
    "relation": "stabilises",
    "object": "training",
    "polarity": "positive",
    "qualifiers": {},
    "evidence": {
     "source": "inputs/findings.md",
     "quote": "Dropout of 0.1 stabilises training but slows convergence by 12%.",
     "char_start": 241,
     "char_end": 305,
     "verified": true
    },
    "confidence": "asserted",
    "evidence_id": "a4"
   },
   "provenance": {
    "extracted_from": "inputs/findings.md",
    "method": "reading-14-nanopub/1.0.0",
    "created": "2026-11-25T07:55:04Z"
   },
   "pubinfo": {
    "creator": "https://orcid.org/0000-0000-0000-0000",
    "created": "2026-11-25T07:55:04Z"
   }
  },
  {
   "@id": "http://example.org/nanopub/a9f0571c62670133",
   "@type": "Nanopublication",
   "head": {
    "assertion": "http://example.org/assertion/5",
    "provenance": "http://example.org/nanopub/a9f0571c62670133#provenance",
    "pubinfo": "http://example.org/nanopub/a9f0571c62670133#pubinfo"
   },
   "assertion": {
    "@id": "http://example.org/assertion/5",
    "subject": "The reported ceiling of 92.4%",
    "relation": "reproduced",
    "object": "the original schedule",
    "polarity": "negative",
    "qualifiers": {
     "context": "the original schedule"
    },
    "evidence": {
     "source": "inputs/findings.md",
     "quote": "The reported ceiling of 92.4% was not reproduced under the original schedule.",
     "char_start": 306,
     "char_end": 383,
     "verified": true
    },
    "confidence": "asserted",
    "evidence_id": "a5"
   },
   "provenance": {
    "extracted_from": "inputs/findings.md",
    "method": "reading-14-nanopub/1.0.0",
    "created": "2026-11-25T07:55:04Z"
   },
   "pubinfo": {
    "creator": "https://orcid.org/0000-0000-0000-0000",
    "created": "2026-11-25T07:55:04Z"
   }
  },
  {
   "@id": "http://example.org/nanopub/09d8d414c2255acd",
   "@type": "Nanopublication",
   "head": {
    "assertion": "http://example.org/assertion/6",
    "provenance": "http://example.org/nanopub/09d8d414c2255acd#provenance",
    "pubinfo": "http://example.org/nanopub/09d8d414c2255acd#pubinfo"
   },
   "assertion": {
    "@id": "http://example.org/assertion/6",
    "sub
```

## Evidence

| id | claim | locator | ok |
|---|---|---|---|
| a1 | Sparse routing reduces inference cost by 0.7x on 32k-token contexts | `p.1 inputs/findings.md[12:80]` | ✓ |
| a2 | The router increase perplexity on the validation split | `p.1 inputs/findings.md[81:145]` | ✓ |
| a3 | Block-sparse attention improves recall by 3.2 points over dense attent | `p.1 inputs/findings.md[146:240]` | ✓ |
| a4 | Dropout of 0.1 stabilises training | `p.1 inputs/findings.md[241:305]` | ✓ |
| a5 | The reported ceiling of 92.4% reproduced the original schedule | `p.1 inputs/findings.md[306:383]` | ✓ |
| a6 | Table 2 shows a 23.4% yield increase for the treatment group relative  | `p.1 inputs/findings.md[384:469]` | ✓ |

## Limits

- polarity comes from a closed verb set plus negation cues; other verbs are left null
