# Security and Research Data Policy

## Never commit
- passwords, API keys or tokens;
- `.env` files;
- private keys/certificates;
- personally identifiable participant data;
- restricted operational or tactical information;
- confidential institutional documents;
- copyrighted full-text PDFs without redistribution permission.

## Frontend secret rule
If any future web dashboard is created, variables exposed to browser bundles (for example `VITE_`, `NEXT_PUBLIC_`, `REACT_APP_`) must never contain secrets.

## Reporting
If a secret is committed, rotate/revoke it immediately and remove it from Git history before continuing work.
