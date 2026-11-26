# Penetration Testing Report
## Mediroza General Hospital

**Program:** NetworkWalks — Week 4  
**Batch:** B083  
**Assessment:** Black-box penetration test  
**Target:** https://medirozahospital.com  
**Assessment duration:** 5 days

---

# 1. Executive Summary

This report documents the results of a partially completed
black-box assessment conducted over the scheduled five-day period.
Testing confirmed publicly accessible directory listings, PHP
version disclosure, and HTTP security-header hardening weaknesses
on the specific endpoints examined.

Three observations were documented. Successful initial access,
M2/M3 challenge objectives, authentication bypass, injection, and
unauthorized access to patient records were not demonstrated.
Accordingly, this report does not claim a completed penetration
test or a comprehensive assessment of the target.

# 2. Scope

**In-scope target:** medirozahospital.com

Testing activities documented:
- DNS and web reconnaissance.
- Public resource and directory inspection.
- Login-page and endpoint inspection.
- HTTP response-header review.
- Static resource inspection.

No denial-of-service testing or social engineering was performed.

# 3. Methodology

1. Reconnaissance and information gathering.
2. Web application enumeration.
3. Authentication-surface inspection.
4. Security configuration review.
5. Evidence collection and finding documentation.

# 4. Findings

## F-01 — Public Directory Listing

**Severity:** Medium (provisional)  
**Status:** Confirmed

Directory indexes were accessible under:
- /patient/
- /staff/
- /old/

The listings exposed application filenames, a reports directory,
an error-log filename, and a database-backup filename.

**Reproduction:**
1. Send an unauthenticated GET request to each affected directory.
2. Observe the HTTP response and directory index.
3. Record the listed filenames without accessing their contents.

**Evidence:**
- `evidence/patient_directory_listing.txt`
- `evidence/staff_directory_listing.txt`
- `evidence/old_directory_listing.txt`

**Limitation:** The contents of the listed reports, error log, and
database backup were not verified.

**Recommendation:** Disable directory indexing and restrict access
to sensitive files. Store backups and logs outside the web root.

## F-02 — PHP Version Disclosure

**Severity:** Low  
**Status:** Confirmed

Login responses disclosed PHP/8.2.36 through X-Powered-By.

**Evidence:**
- `evidence/patient_login_headers.txt`
- `evidence/staff_login_headers.txt`

**Recommendation:** Disable unnecessary technology-disclosure
headers and maintain supported, updated server software.

## F-03 — Missing HTTP Security Headers

**Severity:** Informational  
**Status:** Observed on three tested GET endpoints

GET responses from `/`, `/patient/login.php`, and `/staff/login.php`
did not show CSP, HSTS, X-Frame-Options, X-Content-Type-Options,
Referrer-Policy, or Permissions-Policy.

**Evidence:** `evidence/get_security_headers.txt` and
`evidence/get_login_security_headers.txt`.

**Recommendation:** Configure appropriate security headers and
validate them across all relevant routes and browser workflows.

# 5. Positive Security Observations

Unauthenticated requests to the patient portal and download
endpoint returned HTTP 302 redirects to login.php.

This demonstrates a visible authentication gate, but does not
prove that authorization controls are fully effective.

# 6. Assessment Limitations

The three challenge PDFs, database contents, employee records,
and shareholder information have not been verified or extracted.

A GET request to `/patient/reports/` returned HTTP 403 Forbidden
on 26 November 2026. No PDF filenames were retrieved. This result
documents a server-side access restriction; it does not establish
that the challenge PDFs are absent. See
`evidence/m2_reports_directory_403.txt`.

M1 remains partially completed: directory exposure and other
observations were documented, but successful initial access was
not demonstrated. M2 and M3 remain incomplete and unverified.

# 7. Remediation Priorities

1. Disable public directory indexing.
2. Move backups and logs outside the public web root.
3. Review access controls for all sensitive resources.
4. Remove unnecessary server-version disclosure.
5. Configure and validate HTTP security headers.

# 8. Conclusion

The assessment confirmed a directory-listing misconfiguration
and identified additional information-disclosure and security
hardening observations.

Further authorized testing is required to establish the impact
of the exposed resources and complete the remaining challenge
objectives.
