# NetworkWalks Week 4 — Mediroza Assessment

## Package contents

- `report/`: Final penetration-test report and package integrity manifest.
- `FINDINGS_REGISTER.md`: Consolidated findings and severity register.
- `m1/`: Initial access assessment documentation.
- `evidence/`: Supporting HTTP, directory listing, and finding verification evidence.
- `m2/originals/`: Original locked PDF lab samples.
- `m2/f4-tested-downloads/`: Exact PDF copies used for offline password testing.

## Important evidence distinction

The PDFs in `m2/originals/` are not byte-identical to the PDFs in
`m2/f4-tested-downloads/`. The F4 password-recovery results apply
to the latter three files.

## Assessment limitations

- The SQL backup was confirmed accessible by HTTP response and
  directory listing; its contents were not downloaded or inspected.
- The F4-tested PDFs are separate from the original sample set.
- The F5 metadata observations apply to the locally tested PDF copy.
- Session cookies, recovered passwords, and raw password hashes
  are excluded from this submission.

## Integrity

Verify package files from this directory using:

`sha256sum -c report/SHA256SUMS.txt`
