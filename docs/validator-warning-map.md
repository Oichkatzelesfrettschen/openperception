# Validator Warning Map

This document maps each validator gate, warning code, and active runtime
warning to the corresponding debt row in `docs/KNOWN_ISSUES.md` or task row
in `docs/task-ledger.md`.

Last updated: 2026-04-12

---

## Runtime Status Summary

```
make validate
```

| Gate | Name | Severity | Status (2026-04-12) | Debt |
|------|------|----------|---------------------|------|
| GATE-001 | SEIZURE | BLOCKING | SKIPPED (requires manifest) | ROADMAP v0.3.0+ |
| GATE-002 | CONTRAST | BLOCKING | PASS | -- |
| GATE-003 | CVD | WARNING | WARN | KI-007 |
| GATE-004 | SPATIAL | WARNING | PASS | -- |
| GATE-005 | TEMPORAL_DEPTH | WARNING | PASS | -- |
| GATE-006 | COGNITIVE | WARNING | PASS | -- |
| GATE-007 | ACHROMAT | WARNING | WARN | KI-008 |
| TYPE-001 | TYPOGRAPHY | auxiliary | PASS | -- |
| PROFILE-001 | AXIS_PROFILE | auxiliary | PASS | -- |
| SCALE-001 | QUANTIZATION | auxiliary | PASS | -- |

---

## Active Warnings

### GATE-003 CVD -- KI-007

**Warning message**: `mono/primary-vs-accent: Oklab distance 0.178 in borderline range [0.15, 0.20)`

**Root cause**: `primaryStrong` (#374151, gray-700) and `accentStrong` (#6B7280, gray-500)
are adjacent stops on the gray ramp. The mono variant maps both to adjacent gray
stops because the source hues (indigo-700 and slate-500) have similar BT.709
luminance.

**Affected file**: `tokens/color-tokens.json` (mono variant)

**Debt row**: `docs/KNOWN_ISSUES.md` KI-007

**Resolution**: Assign more separated gray stops for `primaryStrong` and `accentStrong`
in the mono variant. Re-run `make validate` to confirm GATE-002 and GATE-003 both pass.

---

### GATE-007 ACHROMAT -- KI-008

**Warning message**: `mono/viz.categorical[0-1] contrast: 2.13:1 between categorical[0] (#374151) and [1] (#6B7280)`

**Root cause**: Same adjacent-gray-stop issue as KI-007. Both categorical[0] and
categorical[1] in the mono variant are adjacent ramp stops, giving 2.13:1 contrast
between them.

**Affected file**: `tokens/color-tokens.json` (mono variant, `viz.categorical`)

**Debt row**: `docs/KNOWN_ISSUES.md` KI-008

**Resolution**: Assign gray-900 and gray-400 (or similar non-adjacent stops) to
`categorical[0]` and `categorical[1]` in the mono variant. Confirm GATE-002 and
GATE-007 both pass after change.

---

## Skipped Gates

### GATE-001 SEIZURE

**Status**: Not implemented. Requires `--seizure-manifest` argument pointing to a
frame-sequence manifest.

**Debt row**: `ROADMAP.md` (Deferred to v0.3.0+)

**When to run**: When checking animated UI components or video content for
photosensitive safety compliance.

---

## Resolving All Warnings

The two active warnings (GATE-003 and GATE-007) share the same root cause:
the mono variant maps chromatic roles with similar BT.709 luminance to adjacent
gray ramp stops. A single token change fixing `primaryStrong` and `categorical[0]`
to `gray-900` (or similarly dark stop) would resolve both.

Steps:
1. Edit `tokens/color-tokens.json` mono variant: set `primaryStrong` and
   `categorical[0]` to a darker stop (e.g., gray-900 = `#111827`)
2. Run `make mono-tokens` to regenerate the CSS
3. Run `make validate` -- GATE-002, GATE-003, and GATE-007 should all PASS
4. Update KI-007 and KI-008 status to "resolved" in `docs/KNOWN_ISSUES.md`
