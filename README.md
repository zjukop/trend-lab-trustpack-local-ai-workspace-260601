# TrustPack: Safe-by-Default Local AI Workspace Kit

Local-first starter for an auditable AI workspace with **approval-gated actions** and **risk-scored commands**.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
trustpack --help
trustpack ask "summarize this repo"
trustpack run "rm -rf /tmp/demo" --approve
```

## What this starter includes

- Minimal CLI for `ask`, `run`, and `bundle`
- Risk scoring + approval gate for shell actions
- Redacted debug bundle export (env + logs scaffold)
- Smoke test to verify install and CLI basics

## Notes

This is a tiny, runnable foundation intended for expansion into a full local AI workspace (Docker/Ollama/OpenAI, memory ingestion, plugins, etc.).
