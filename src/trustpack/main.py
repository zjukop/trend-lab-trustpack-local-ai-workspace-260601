from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path


def risk_score(command: str) -> int:
    risky = [r"\brm\b", r"sudo", r"curl\s+.*\|\s*sh", r"mkfs", r":\(\)\{"]
    return sum(30 for p in risky if re.search(p, command))


def redact_env() -> dict[str, str]:
    out: dict[str, str] = {}
    for k, v in os.environ.items():
        if any(s in k.upper() for s in ["KEY", "TOKEN", "SECRET", "PASSWORD"]):
            out[k] = "***REDACTED***"
        else:
            out[k] = v[:120]
    return out


def cmd_ask(prompt: str) -> int:
    print(f"[trustpack] local answer stub: {prompt}")
    print("citations: [README.md:1]")
    return 0


def cmd_run(command: str, approve: bool) -> int:
    score = risk_score(command)
    print(f"risk_score={score}")
    if score >= 30 and not approve:
        print("blocked: high-risk command. Re-run with --approve.")
        return 2
    cp = subprocess.run(command, shell=True, check=False)
    return cp.returncode


def cmd_bundle(output: str) -> int:
    p = Path(output)
    p.parent.mkdir(parents=True, exist_ok=True)
    payload = {"env": redact_env(), "notes": "Attach this file to issue reports."}
    p.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"wrote {p}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="trustpack", description="TrustPack local AI workspace starter")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ask = sub.add_parser("ask", help="Ask local workspace")
    p_ask.add_argument("prompt")

    p_run = sub.add_parser("run", help="Run shell command with risk gate")
    p_run.add_argument("command")
    p_run.add_argument("--approve", action="store_true", help="Approve risky command")

    p_bundle = sub.add_parser("bundle", help="Create redacted debug bundle")
    p_bundle.add_argument("--output", default="debug_bundle.json")

    return parser


def cli(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "ask":
        return cmd_ask(args.prompt)
    if args.cmd == "run":
        return cmd_run(args.command, args.approve)
    if args.cmd == "bundle":
        return cmd_bundle(args.output)
    return 1


if __name__ == "__main__":
    raise SystemExit(cli())
