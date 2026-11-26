# F-01 — Public Directory Listing

**Target:** https://medirozahospital.com  
**Assessment:** NetworkWalks — Week 4  
**Category:** Security Misconfiguration  
**Affected paths:**
- /patient/
- /staff/
- /old/

## Description

The web server exposes directory indexes without requiring authentication.

The listings disclose:
- Patient application files and a reports directory.
- A publicly listed error log.
- Staff login application path.
- A database backup filename.

## Evidence

- `evidence/patient_directory_listing.txt`
- `evidence/staff_directory_listing.txt`
- `evidence/old_directory_listing.txt`

The listings exposed filenames and directory structure. The contents
of the listed error log, reports, and database backup were not verified.

## Security Impact

An unauthenticated visitor can enumerate files and application structure.
This may expose sensitive information if the listed resources are
also publicly accessible.

## Severity

Low.
Severity is Low because directory indexing exposes filenames and structure; sensitive file contents are assessed separately under F6.

## Recommendation

- Disable automatic directory indexing.
- Restrict access to sensitive directories.
- Store database backups outside the web root.
- Protect logs and application configuration files.
- Review access controls and server configuration.

## Status

Directory listing confirmed.
Sensitive file contents not yet verified.
