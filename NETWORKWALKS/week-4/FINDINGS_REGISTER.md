# Mediroza General Hospital — Findings Register

**Program:** NetworkWalks — Week 4
**Batch:** B083
**Target:** https://medirozahospital.com
**Assessment type:** Black-box web application assessment

| ID | Finding | Classification | Severity | Status |
|---|---|---|---|---|
| F1 | Public directory listing | Security Misconfiguration | Low | Confirmed |
| F2 | SQL injection in patient login — authentication bypass | Injection / Authentication Bypass | Critical | Confirmed |
| F3 | Unauthorized access to patient lab reports | Broken Access Control | High | Report-supported; live downloads not replayed in follow-up |
| F4 | Weak PDF passwords | Cryptographic / Password Weakness | High | Three local PDF copies cracked offline; source-version discrepancy remains |
| F5 | Sensitive PDF metadata disclosure | Information Disclosure | Medium | Confirmed on a local PDF copy |
| F6 | Publicly exposed legacy SQL backup | Sensitive Data Exposure / Security Misconfiguration | Critical | Public directory listing and backup HTTP response confirmed; SQL contents not downloaded |

## Auxiliary observations

| ID | Observation | Severity | Status |
|---|---|---|---|
| A1 | PHP version disclosure (`X-Powered-By`) | Low | Confirmed |
| A2 | Missing HTTP security headers on three tested GET endpoints | Informational | Observed; limited endpoint coverage |

## Important limitations

- F2 demonstrates access to the patient portal, not administrator privileges.
- F3 is supported by the portal's report links and previously collected report artifacts. The three download requests were not independently replayed during the 26 November follow-up.
- F4 was verified against three local PDF files. Their relationship to the PDFs referenced in the original report has not been conclusively reconciled.
- F5 metadata was verified on a local PDF copy. Some metadata field labels differ between the original report and the local copy.
- F6 was verified through an unauthenticated directory listing and an HTTP HEAD response for the listed SQL backup. The backup was not downloaded or inspected.
- The live backup filename observed during follow-up differs from the filename cited in the original report.
- Follow-up verification performed on 26 November 2026 is distinguished from the original assessment period of 22–24 November 2026.
