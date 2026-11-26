# M1 — Initial Access Assessment

**Client:** Mediroza General Hospital
**Program:** NetworkWalks — Week 4
**Assessment type:** Black-box web application assessment
**Target:** https://medirozahospital.com

## 1. Reconnaissance

Activities included:

- DNS resolution and HTTP response inspection.
- robots.txt and sitemap inspection.
- Homepage and login-page enumeration.
- Patient and staff application endpoint inspection.
- Public directory-index inspection.
- HTTP response-header inspection.
- Static resource inspection.

## 2. Confirmed findings and observations

### F1 — Public directory listing
Directory indexes were accessible under:
- `/patient/`
- `/staff/`
- `/old/`

Severity: Low.

### F2 — SQL injection in patient login
A crafted username input bypassed the patient login flow.
The resulting session accessed `/patient/portal.php` and returned
the patient portal content.

Severity: Critical.

Evidence: `../evidence/f2/RESULTS.txt`.

Administrative privileges were not established.

### Auxiliary observation A1 — PHP version disclosure
Patient and staff login responses disclosed PHP/8.2.36 through
the `X-Powered-By` header.

Severity: Low.

### Auxiliary observation A2 — Missing HTTP security headers
Six security headers were absent from the three tested GET
endpoints: `/`, `/patient/login.php`, and `/staff/login.php`.

Severity: Informational. Coverage was limited to these endpoints.

## 3. Access-control observations

An unauthenticated request to `/patient/portal.php` returned
HTTP 302 and redirected to `login.php`.

A request using the injection-created session returned HTTP 200
and displayed the patient portal.

This confirms an authentication bypass in the tested login flow.
It does not establish administrator access.

## 4. M1 objective status

**Status: Initial access demonstrated.**

The patient login SQL injection was confirmed and the resulting
session was verified against the patient portal.

## 5. Evidence

Supporting evidence is stored in:
- `../evidence/`
- `../recon/`
- `F-01-directory-listing.md`
- `A-01-php-version-disclosure.md`
- `A-02-missing-security-headers.md`

## 6. Limitations

M1 evidence establishes patient-portal access only. It does not
establish administrative privileges or complete access to the
underlying server or database.
