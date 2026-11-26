# Penetration Testing Report
## Mediroza General Hospital

**Program:** NetworkWalks — Week 4
**Batch:** B083
**Assessment type:** Black-box web application penetration test
**Target:** https://medirozahospital.com
**Original assessment period:** 22–24 November 2026
**Follow-up evidence verification:** 26 November 2026

---

# 1. Executive Summary

The assessment identified six security findings affecting the
Mediroza General Hospital web application.

The most significant issue was SQL injection in the patient login
endpoint. A crafted username input bypassed the login flow and
created a session that could access the patient portal. This
demonstrates unauthorized patient-portal access; administrative
privileges were not established.

Additional findings concern unauthorized access to patient report
resources, weak passwords protecting local copies of PDF reports,
sensitive metadata embedded in a PDF, and a publicly indexed legacy
SQL backup.

The public backup's directory listing and HTTP response were
independently verified during follow-up. The SQL file itself was
not downloaded or inspected.

The findings and evidence limitations are documented below.
Follow-up checks performed on 26 November are distinguished from
the original assessment period.

# 2. Scope

**In-scope target:** `https://medirozahospital.com`

The assessment focused on the target web application, including:
- Public web resources and directory indexes.
- Patient and staff login interfaces.
- Patient portal authentication behavior.
- Report links and download resources.
- PDF password protection and document metadata.
- Public exposure of a legacy database backup.
- HTTP response headers.

No denial-of-service testing or social engineering was performed.
Other network services were not assessed as part of the web
application findings in this report.

# 3. Methodology

The assessment used a black-box approach:

1. Reconnaissance and web application enumeration.
2. Inspection of public directories and application resources.
3. Review of login forms and authentication behavior.
4. Controlled authentication-bypass testing.
5. Review of report-resource exposure.
6. Offline examination of locally available PDF copies.
7. Review of PDF metadata.
8. Verification of the publicly listed legacy backup URL.
9. Evidence integrity checks using SHA-256.

# 4. Findings

## F1 — Public Directory Listing

**Severity:** Low
**Classification:** Security Misconfiguration
**Status:** Confirmed

### Description

Unauthenticated directory indexes were accessible under:
- `/patient/`
- `/staff/`
- `/old/`

The listings disclosed application filenames, a reports directory,
an error-log filename, and a legacy database-backup filename.

### Security impact

Directory indexing exposes application structure and resource
names to unauthenticated visitors. The exposure can facilitate
further reconnaissance. The impact of individual listed resources
is assessed separately where independently verified.

### Evidence

- `evidence/patient_directory_listing.txt`
- `evidence/staff_directory_listing.txt`
- `evidence/old_directory_listing.txt`
- `evidence/f6/old_directory.html`

### Recommendation

Disable automatic directory indexing. Restrict access to sensitive
directories and store backups and logs outside the public web root.

---

## F2 — SQL Injection in Patient Login

**Severity:** Critical
**Classification:** Injection / Authentication Bypass
**Status:** Confirmed

### Affected endpoint

`POST /patient/login.php`

### Description

The patient login form accepted a username value that was vulnerable
to SQL injection. A crafted username input bypassed the normal
authentication flow.

The test input used was `admin' -- ` with an empty password.

### Verification

- A baseline invalid-credentials request returned HTTP 200.
- The injection request returned HTTP 302, redirecting to
  `portal.php`.
- An unauthenticated request to `/patient/portal.php` returned
  HTTP 302 and redirected to `login.php`.
- A request using the injection-created session returned HTTP 200.
- The response contained the patient portal interface, including
  `Patient Portal`, `My lab reports`, and `logout`.

### Security impact

An unauthenticated attacker could bypass patient login and access
the patient portal. This creates a path to sensitive patient
resources.

The evidence establishes patient-portal access. It does not
establish administrator privileges or administrative access to
the underlying system.

### Evidence

- `evidence/f2/RESULTS.txt`
- `evidence/f2/baseline.headers`
- `evidence/f2/injection.headers`
- `evidence/f2/portal_unauth.headers`
- `evidence/f2/portal_auth.headers`

Session cookie files are retained separately and must not be
included in the public submission.

### Recommendation

Use parameterized SQL queries or prepared statements for all
database operations. Apply server-side input handling, avoid
constructing SQL statements through string concatenation, and
review authentication logic. Invalidate potentially exposed
sessions and investigate access to patient records.

---

## F3 — Unauthorized Access to Patient Lab Reports

**Severity:** High
**Classification:** Broken Access Control
**Status:** Supported by original assessment evidence and local
artifacts; individual downloads were not replayed during the
26 November follow-up.

### Description

The patient portal displayed report download links associated
with multiple patient records, including:

- S. Dlamini — LR-2024-1187
- P. Reddy — LR-2024-1192
- E. Thompson — LR-2024-1205

The original assessment report records that these resources were
downloaded following the authentication bypass.

The follow-up evidence confirms the portal content and the
presence of local PDF artifacts. It does not independently
replay all three live download requests.

### Security impact

Access to reports belonging to other patients can expose
confidential medical information. This represents a serious
privacy and access-control failure.

### Evidence

- Patient portal response captured during the F2 verification.
- `m2/originals/` contains three local PDF artifacts.
- `evidence/m2_reports_directory_403.txt` records an unauthenticated
  request to the reports directory returning HTTP 403.

The directory-level 403 response does not establish that
individual report-download routes enforce correct authorization.

### Recommendation

Enforce object-level authorization on every report request.
Bind each report to the authenticated user's identity and verify
ownership on the server for every download. Do not rely on
unguessable identifiers or portal-page visibility as access
controls.

---

## F4 — Weak Passwords Protecting PDF Reports

**Severity:** High
**Classification:** Cryptographic / Password Weakness
**Status:** Three locally available PDF copies were successfully
cracked offline.

### Description

Three locally available password-protected PDF files were tested
using PDF hash extraction and offline dictionary-based password
recovery with John the Ripper and a common password wordlist.

All three extracted password hashes were recovered.

The files were subsequently checked with `qpdf` using their
recovered passwords. The PDFs reported encryption revision R=3
and 128-bit encryption under the PDF Standard Security Handler.

The evidence demonstrates weak password protection. It does not
demonstrate a break of the underlying encryption algorithm.

### Security impact

An attacker who obtains the protected PDFs may be able to recover
weak passwords offline and access their contents without
interacting with the web application.

### Evidence

- Local PDF artifacts and their SHA-256 hashes.
- PDF hash extraction and John the Ripper verification performed
  locally.
- Successful `qpdf --check` validation using recovered passwords.

Plaintext passwords and raw password hashes are intentionally
excluded from the public report and submission.

### Evidence limitation

The three locally tested files in `~/Downloads` have not been
conclusively reconciled with the separate files in `m2/originals/`
or every PDF referenced in the original assessment report.
The original report and local copies also contain differing
password and metadata details. These versions must not be treated
as identical without further verification.

### Recommendation

Use strong, unique passwords generated through an approved
secrets-management process. Avoid predictable passwords and
password reuse. Apply appropriate access controls to the original
documents and use modern document-protection practices.

---

## F5 — Sensitive PDF Metadata Disclosure

**Severity:** Medium
**Classification:** Information Disclosure
**Status:** Confirmed on a locally available PDF copy.

### Description

Metadata extracted from a locally available PDF included:

- Author: `j.malik`
- Producer: `Mediroza Lab Reporting Module`
- Creator: `Mediroza CMS 1.4.2`
- Subject: `Full Blood Count`
- Comments: `DB backup moved to /old before site migration, do not delete`

The comment disclosed an internal backup location and migration
context. This information provided a useful lead during the
assessment of the publicly exposed `/old/` directory.

### Security impact

Document metadata can disclose internal usernames, software
details, operational notes, and references to sensitive resources.
In this case, the comment exposed a reference to the legacy backup
location.

### Evidence

- ExifTool output from the locally available PDF after authorized
  local decryption.
- Metadata fields recorded during the follow-up verification.

### Evidence limitation

The local PDF's Creator and Subject values differ from the field
values transcribed in the original report. The metadata evidence
therefore refers to the tested local copy; the discrepancy is
not silently reconciled.

### Recommendation

Remove unnecessary metadata and internal comments before
publishing or distributing documents. Review document-generation
templates and automate metadata sanitization.

---

## F6 — Publicly Exposed Legacy SQL Backup

**Severity:** Critical
**Classification:** Sensitive Data Exposure / Security Misconfiguration
**Status:** Public directory listing and backup HTTP response
confirmed during follow-up.

### Description

The unauthenticated directory `/old/` returned HTTP 200 and
exposed a directory index.

The live listing contained:

`/old/mediroza_db_backup_2019.sql`

An unauthenticated HTTP HEAD request to the listed backup returned
HTTP 200 with content type `text/x-sql` and a content length of
6,346 bytes.

### Security impact

A publicly accessible database backup may expose sensitive
organizational or personal information. The observed public
availability of a SQL backup represents a critical exposure
because the file is served from the web root without an
authentication barrier.

The backup contents were not downloaded or inspected during
follow-up. Specific database tables or records are therefore
not independently confirmed by this verification.

### Evidence

- `evidence/f6/old_directory.headers`
- `evidence/f6/old_directory.html`
- `evidence/f6/backup_headers.txt`
- `evidence/f6/RESULTS.txt`
- `evidence/f6/SHA256SUMS.txt`

All four evidence-file checksum validations passed.

### Evidence limitation

The original report references a different backup filename:
`mediroza_hospital.sql`.

The live directory listing observed on 26 November exposed
`mediroza_db_backup_2019.sql`. The observed live filename is used
in this finding. The SQL file itself was not downloaded.

### Recommendation

Remove the backup from the public web root immediately. Store
database backups in access-controlled locations, restrict access
through server-side authorization, and review web-server
configuration to prevent backup files from being served publicly.
Assess whether the exposed backup requires incident response,
credential rotation, or notification.

# 5. Auxiliary Observations

## A1 — PHP Version Disclosure

**Severity:** Low
**Status:** Confirmed

The patient and staff login responses disclosed PHP/8.2.36 through
the `X-Powered-By` response header.

**Evidence:**
- `evidence/patient_login_headers.txt`
- `evidence/staff_login_headers.txt`

**Recommendation:** Disable unnecessary technology-disclosure
headers and maintain supported, updated server software.

## A2 — Missing HTTP Security Headers

**Severity:** Informational
**Status:** Observed on three tested GET endpoints.

The responses from `/`, `/patient/login.php`, and
`/staff/login.php` did not show the following headers:

- Content-Security-Policy
- Strict-Transport-Security
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy
- Permissions-Policy

**Evidence:**
- `evidence/get_security_headers.txt`
- `evidence/get_login_security_headers.txt`

The observation is limited to these three endpoints and does not
independently demonstrate an exploitable vulnerability.

**Recommendation:** Configure appropriate security headers
according to application requirements and validate them across
all relevant routes.

# 6. Overall Remediation Priorities

1. Fix the SQL injection vulnerability in the patient login flow.
2. Enforce patient-specific authorization for every report request.
3. Remove the publicly accessible SQL backup and review exposure.
4. Replace weak PDF passwords and review document distribution.
5. Remove sensitive internal comments and metadata from documents.
6. Disable public directory indexing.
7. Remove unnecessary PHP version disclosure.
8. Configure and validate appropriate HTTP security headers.

# 7. Conclusion

The assessment identified critical weaknesses in authentication
and exposure of sensitive resources. The confirmed SQL injection
allowed access to the patient portal, while follow-up verification
confirmed that a legacy SQL backup was publicly listed and
served by the web server.

The report distinguishes independently verified observations
from evidence inherited from the original assessment and local
artifacts. The SQL backup was not downloaded, administrative
privileges were not established, and discrepancies between
different local PDF copies remain unresolved.

Remediation should prioritize the authentication bypass,
patient-record authorization, and removal of the public backup.
