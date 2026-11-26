# Mediroza General Hospital — Findings Register

Assessment: NetworkWalks Week 4
Target: https://medirozahospital.com

| ID | Finding | Classification | Severity | Status |
|---|---|---|---|---|
| F-01 | Public directory listing | Security Misconfiguration | Medium (provisional) | Confirmed |
| F-02 | PHP version disclosure | Information Disclosure | Low | Confirmed |
| F-03 | Missing HTTP security headers | Security Misconfiguration | Informational | Observed on 3 GET endpoints |

## Positive Security Observations

- Patient portal redirects unauthenticated requests to login.php.
- Patient download endpoint redirects unauthenticated requests to login.php.

These observations do not establish complete access-control effectiveness.

## Outstanding Objectives

- M1: Partially completed. Directory exposure and other observations were documented, but successful initial access was not demonstrated.
- M2: Not completed. The patient reports directory returned HTTP 403; no PDF files were retrieved or assessed.
- M3: Not completed. Employee and shareholder data were not accessed or verified.
- M4: Report prepared, internally checked, packaged, and published to GitHub.

## Evidence Limitations

- Directory listings are confirmed.
- Contents of listed sensitive files have not been verified.
- No successful authentication bypass or injection has been demonstrated.
- F-03 was observed on GET responses from `/`, `/patient/login.php`, and `/staff/login.php`; evidence is stored in `evidence/get_security_headers.txt` and `evidence/get_login_security_headers.txt`.


## Additional M2 Evidence

- `evidence/m2_reports_directory_403.txt`: GET request to `/patient/reports/` returned HTTP 403 Forbidden on 26 November 2026. No PDF filenames were retrieved. This does not establish that the PDFs are absent; M2 remains incomplete.
