# PWVault — Secure Coding Review

**Program:** CodeAlpha Cyber Security Internship
**Task:** Secure Coding Review (Task 3)
**Application:** PWVault — password manager
**Review type:** Source-code security review
**Status:** Completed

## 1. Objective

Review the PWVault source code for security weaknesses using static-analysis tools, dependency vulnerability checks, automated tests, and manual code inspection.

This is a scoped educational security review. It is not an independent certification, formal penetration test, or guarantee that the application is vulnerability-free.

## 2. Scope and methodology

The review covered the application and server-side components, including:

- Authentication, registration, and account recovery
- Password hashing, token handling, and second-factor authentication
- Passkey registration and authentication
- Entry and shared-vault authorization
- Administrative operations
- API schemas and input validation
- Docker deployment configuration and security headers

Methods and tools:

- Manual source-code inspection
- Bandit for Python static analysis
- pip-audit for Python dependency advisories
- npm audit for JavaScript dependency advisories
- pytest for automated tests

## 3. Findings

### PWV-001 — High: Administrator account pre-claim through unverified email registration

**Affected components:** `pwvault_server/config.py`, `pwvault_server/routes_auth.py`, `pwvault_server/routes_admin.py`

**Description:**

The registration configuration defaults to open registration when no environment override is supplied. During registration, the submitted email address is compared against configured administrator email addresses. A matching address is assigned the administrator role.

The reviewed registration flow does not verify ownership of the submitted email address before granting that role. The invitation check also does not apply to configured administrator email addresses.

An attacker who registers a configured administrator email address before its legitimate owner may therefore obtain administrative privileges, provided the service is exposed and that account has not already been claimed.

**Impact:**

An unauthorized user could gain administrative capabilities, including user management, role changes, account disabling, invitation creation, and audit-log access. The application's zero-knowledge design limits direct access to users' plaintext vault contents, but does not remove the administrative risk.

**Evidence:**

- `s1.png`: registration configuration and default.
- `s2.png`: registration logic and role assignment.
- `s3.png`: administrative capabilities.
- `.env.example`: documents the lack of email verification.

**Recommendation:**

- Do not assign administrator privileges solely from a user-submitted email address.
- Use a trusted bootstrap process or a one-time administrative provisioning command.
- Verify email ownership before relying on email identity.
- Ensure invite-only registration does not bypass administrator provisioning controls.
- Add regression tests for attempted administrator account pre-claim.

**Status:** Finding identified during source review; no exploitation against a live deployment was performed.

### PWV-002 — Medium: Missing application-level IP/global rate limiting

**Affected component:** Authentication endpoints in `pwvault_server`

**Description:**

The application implements account-level failed-login tracking and temporary account lockout. The reviewed application code did not show an application-level IP-based or global rate limiter.

Repeated authentication failures against a known account may therefore trigger account lockout and temporarily deny access to its legitimate owner.

**Existing protection:**

- Default lockout after five failed attempts.
- Default lockout duration of 15 minutes.
- HTTP 429 response and `Retry-After` behavior.

**Impact:**

An attacker may repeatedly trigger account lockouts, creating an availability and account-denial risk.

**Evidence:**

- `s4.png`: account lockout implementation.
- `s10.png`: search for application-level rate-limiting implementation.

**Recommendation:**

- Add IP-based and global authentication rate limits.
- Consider progressive delays and abuse monitoring.
- Ensure reverse-proxy or WAF controls are configured and verified.
- Test lockout behavior without allowing attackers to cause indefinite denial of service.

**Limitation:** External reverse-proxy and WAF configurations were not assessed. This finding concerns the reviewed application code.

## 4. Automated security checks

| Check | Result |
|---|---|
| Bandit | One low-severity candidate reviewed manually |
| pip-audit | No known vulnerabilities found |
| npm audit | 0 vulnerabilities reported |
| pytest | 175 passed, 0 failed, 0 skipped |
| Test warning | 1 Starlette/httpx deprecation warning |

### Bandit finding disposition

Bandit reported a possible hardcoded password at `pwvault/vault.py:73`.

Manual inspection showed that the value was an empty string used to clear username and password fields for non-login entry types in `Entry.__post_init__()`. This is intentional sanitization, not a hardcoded credential.

The alert was treated as a false positive and was not suppressed.

Evidence: `s7.png` and `s11.png`.

### Dependency checks

`pip-audit` reported no known vulnerabilities in the resolved Python dependencies checked.

`npm audit` reported zero vulnerabilities across 40 audited packages.

These results reflect known advisories available to the tools at the time of testing. They do not prove that dependencies are free of all vulnerabilities.

## 5. Automated test results

The full pytest suite completed with:

- 175 passed
- 0 failed
- 0 skipped
- 1 warning

The Node-dependent UI tests were included in the test run.

Evidence: `s5.png` and `s6.png`.

## 6. Additional security observations

The manual review also examined:

- Argon2id password hashing and minimum KDF parameters.
- JWT algorithm pinning and token validation.
- TOTP replay prevention and recovery-code consumption.
- WebAuthn challenge expiration and one-use handling.
- User-scoped entry and shared-vault authorization.
- API input validation and payload size limits.
- Security headers and Content Security Policy.
- Docker read-only filesystem, dropped capabilities, and proxy-only application exposure.

No additional confirmed vulnerability is reported from these checks. This does not mean these components are guaranteed secure.

## 7. Limitations

- No live production deployment was tested.
- No exploitation against third-party systems was performed.
- External infrastructure, reverse proxies, WAFs, and hosting configuration were not independently assessed.
- Automated scanners detect only classes of issues covered by their rules and advisory databases.
- The review was limited to the source code and configuration available in the reviewed project copy.

## 8. Conclusion

The review identified two security concerns requiring attention:

1. Administrator role assignment based on an unverified submitted email address.
2. Lack of application-level IP/global rate limiting, despite existing account-level lockout protection.

The automated test suite passed, and the dependency scanners reported no known vulnerabilities in the checked dependencies. These results support the review but do not establish that PWVault is vulnerability-free.

**Overall recommendation:** Prioritize secure administrator provisioning, then implement and test layered authentication rate limiting.
