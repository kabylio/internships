# F-03 — Missing HTTP Security Headers

**Target:** https://medirozahospital.com  
**Severity:** Informational  
**Classification:** Security Misconfiguration  
**Status:** Observed on three tested GET endpoints

## Description

Three public endpoints were inspected using HTTP GET requests:

- `/`
- `/patient/login.php`
- `/staff/login.php`

The responses did not contain the following headers:

- Content-Security-Policy
- Strict-Transport-Security
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy
- Permissions-Policy

## Evidence

- `evidence/get_security_headers.txt`
- `evidence/get_login_security_headers.txt`

All three endpoints returned HTTP 200.

## Impact

The absence of these headers may reduce browser-side security protections.
The practical impact depends on the application's functionality,
deployment configuration, and exposure to relevant attack scenarios.

This observation does not independently demonstrate an exploitable
vulnerability.

## Recommendation

Configure appropriate security headers according to application
requirements. Validate the resulting policy across all relevant routes
and test for compatibility before deployment.

## Limitations

Testing covered only the three listed public GET endpoints.
Other application routes and browser-enforced behavior were not assessed.
