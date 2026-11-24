# CodeAlpha — Task 3: Secure Coding Review

This folder contains the PWVault secure coding review report, its PDF version, and the supporting evidence captured during the review.

## Contents

- `SECURITY-REVIEW.md` — detailed scope, methodology, findings, recommendations, test results, and limitations.
- `PWVault_Secure_Coding_Review_Restyled.pdf` — PDF report with the original report pages and a supporting evidence appendix.
- `Screenshots/` — 11 supporting screenshots referenced inline in the Markdown report.

## Findings summary

- **PWV-001 — High:** Administrator account pre-claim through unverified email registration.
- **PWV-002 — Medium:** Missing application-level IP/global rate limiting.
- Bandit candidate manually reviewed and classified as a false positive.

## Automated checks

- Bandit: 2,859 lines of code reviewed; one manually reviewed false-positive candidate.
- pip-audit: no known vulnerabilities found in resolved dependencies.
- npm audit: zero vulnerabilities reported.
- pytest: 175 passed, 0 failed, 0 skipped.

See `SECURITY-REVIEW.md` for the complete analysis and evidence.

## Limitations

This is an educational source-code security review. It is not a formal independent audit, certification, or live penetration test. External infrastructure controls were not assessed.
