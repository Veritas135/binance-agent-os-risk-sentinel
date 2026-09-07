# Contributing

Contributions are welcome, especially improvements to explainability, deterministic risk logic, test coverage, Agent OS interoperability, and UI clarity.

## Development

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
streamlit run app.py
```

## Pull requests

Please keep changes focused and include tests for reasoning or parsing changes. Do not commit API keys, session tokens, cookies, private account snapshots, or fabricated Binance/Agent OS outputs.

Any feature that could lead to account actions must preserve the project's explicit human-confirmation boundary.
