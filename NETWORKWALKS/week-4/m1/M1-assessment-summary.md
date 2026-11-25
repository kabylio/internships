# M1 — Initial Access Assessment

**Client:** Mediroza General Hospital  
**Program:** NetworkWalks — Week 4  
**Assessment type:** Black-box  
**Target:** https://medirozahospital.com

## 1. Reconnaissance

The following activities were completed:

- DNS resolution and HTTP response inspection.
- robots.txt and sitemap inspection.
- Homepage and login-page enumeration.
- Patient and staff application endpoint inspection.
- Public directory-index inspection.
- HTTP response-header inspection.
- Static stylesheet inspection.

## 2. Confirmed observations

### F-01 — Public directory listing
Directory indexes were accessible under:
- /patient/
- /staff/
- /old/

### F-02 — PHP version disclosure
Login endpoints disclosed PHP/8.2.36 through X-Powered-By.

### F-03 — Missing security headers
The six checked security headers were absent from GET responses
for `/`, `/patient/login.php`, and `/staff/login.php`.
Evidence:
- `evidence/get_security_headers.txt`
- `evidence/get_login_security_headers.txt`

This observation is limited to those three tested endpoints.

## 3. Access-control observations

Unauthenticated requests to:
- /patient/portal.php
- /patient/download.php

returned HTTP 302 redirects to login.php.

This indicates an authentication gate but does not establish complete authorization effectiveness.

## 4. M1 objective status

**Status: Partially completed.**

Public application structure and security weaknesses were identified. Successful unauthorized access and retrieval of the three challenge PDFs have not been demonstrated.

## 5. Evidence

Supporting evidence is stored in:
- ../evidence/
- ../recon/
- F-01-directory-listing.md
- F-02-php-version-disclosure.md
- F-03-missing-security-headers.md

## 6. Limitations

No patient records, database contents, or employee information were accessed or extracted during this assessment phase.
