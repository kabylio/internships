# F-02 — PHP Version Disclosure

**Target:** https://medirozahospital.com
**Category:** Information Disclosure
**Affected endpoints:**
- /patient/login.php
- /staff/login.php

## Description

The HTTP responses expose the server-side PHP version through
the X-Powered-By response header.

Observed value:
PHP/8.2.36

## Evidence

- evidence/patient_login_headers.txt
- evidence/staff_login_headers.txt

## Security Impact

Technology disclosure helps an attacker identify the server-side
technology stack and select potentially relevant attack techniques.

This observation does not independently establish an exploitable
PHP vulnerability.

## Severity

Low — Informational disclosure.

## Recommendation

- Disable the X-Powered-By header.
- Keep PHP and its dependencies updated.
- Review server configuration to minimize unnecessary
  technology disclosure.

## Status

Confirmed.
