# Security Policy

## Sensitive data

Do not open a public issue containing API keys, session tokens, cookies, account identifiers, private portfolio snapshots, or other secrets.

The repository intentionally stores no Binance credentials. Authentication and permissions for Binance Agent OS/MCP should remain in the supported client environment.

## Reporting a vulnerability

For a public hackathon prototype, please report non-sensitive implementation issues through GitHub Issues. For a vulnerability that would require disclosing secrets or private account data, contact the repository maintainer privately through their GitHub profile instead of posting the details publicly.

## Execution boundary

The Streamlit dashboard is an analysis/proposal layer and does not place orders. Changes that bypass explicit human authorization are outside the intended security model.
