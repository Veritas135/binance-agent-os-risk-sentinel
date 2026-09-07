# Publish this repository to GitHub

Recommended repository name:

`binance-agent-os-risk-sentinel`

Recommended description:

`Explainable multi-agent risk control system for Binance Agent OS — Market, Risk, Portfolio and Decision agents with a human-confirmation execution boundary.`

Recommended topics:

`binance`, `agent-os`, `mcp`, `ai-agent`, `multi-agent`, `streamlit`, `risk-management`, `hackathon`, `python`

## Option A — GitHub website

1. Create a new **public** repository named `binance-agent-os-risk-sentinel`.
2. Do not initialize it with a README, license, or .gitignore because these files already exist here.
3. Upload the contents of this folder, preserving `.github/`, `agents/`, `agent_os/`, `data/`, `docs/`, and `tests/`.
4. Commit with the message: `Initial public release: Binance Risk Sentinel v0.2.0`.
5. In repository settings/About, add the description and topics above.

## Option B — Git command line

After creating an empty public GitHub repository:

```bash
git init
git branch -M main
git add .
git commit -m "Initial public release: Binance Risk Sentinel v0.2.0"
git remote add origin https://github.com/YOUR_USERNAME/binance-agent-os-risk-sentinel.git
git push -u origin main
```

Then enable GitHub Actions if your account asks for permission. The included CI workflow runs compilation and pytest on Python 3.10, 3.11, and 3.12.
