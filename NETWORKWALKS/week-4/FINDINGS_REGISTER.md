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

- M1: Authorized initial-access assessment and proof.
- M2: Assessment of the three challenge PDFs.
- M3: Authorized assessment of critical data exposure.
- M4: Report draft prepared; final QA and evidence packaging pending.

## Evidence Limitations

- Directory listings are confirmed.
- Contents of listed sensitive files have not been verified.
- No successful authentication bypass or injection has been demonstrated.
- F-03 was observed on GET responses from `/`, `/patient/login.php`, and `/staff/login.php`; evidence is stored in `evidence/get_security_headers.txt` and `evidence/get_login_security_headers.txt`.
