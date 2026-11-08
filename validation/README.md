# Acceptance and validation evidence

These records are portable producer attestations for the final accepted edition.
Chapter records preserve scientific-file hashes, two distinct nonauthor AI full
review identities, original report digests and required targeted-clearance
digests. They are exported only after the producer validates the actual private
reports. Those reports, raw captions, source downloads and browser proofs remain
private. Public checks preserve the original acceptance; they do not reopen or
independently authenticate the private reports or certify mathematical truth.

Check the public snapshot and rebuild its navigation without private evidence:

```sh
python -X utf8 tools/check_course.py --release --exported-evidence
python -X utf8 tools/build_course.py --exported-evidence
```

`structure-checks.json`, `reader-checks.json`, `reproduction-checks.json` and
`release-checks.json` record separate producer checks. Numerical reproduction is
byte-for-byte for all25 laboratories and figure generators in a source-free copy.
Browser checks cover offline desktop/phone rendering, controls and printing.
Finite computations, AI scientific review and sampled source frames have bounded
scopes; none constitutes formal proof certification or continuous video review.

The producer uses `python tools/check_course.py --release` and
`python tools/export_validation.py` with actual private evidence available.
Producer mode never silently falls back to public acceptance records.
