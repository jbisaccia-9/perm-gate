"""Optional live-model baseline for the prompt-only enforcement mode."""
import json
import os

from .agent import GUARD_PROMPT
from .gate import leaked_values, load_attacks
from .store import fetch_trusting

DEFAULT_MODEL = "gpt-4.1-mini"


def answer_live(request, client=None, model=None):
    """Ask a real model to answer from a full record protected only by a prompt."""
    if client is None:
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is required for live mode")
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError('install the live extra with: pip install -e ".[live]"') from exc
        client = OpenAI()

    record = fetch_trusting(request["user"])
    response = client.responses.create(
        model=model or os.environ.get("PERMGATE_LIVE_MODEL", DEFAULT_MODEL),
        instructions=GUARD_PROMPT,
        input=("Retrieved record:\n" + json.dumps(record, sort_keys=True) +
               "\n\nUser request:\n" + request["text"]),
        max_output_tokens=400,
        store=False,
    )
    return response.output_text


def run_live_attacks(client=None, model=None):
    results = []
    for attack in load_attacks():
        reply = answer_live(attack, client=client, model=model)
        results.append({"id": attack["id"], "kind": attack["kind"],
                        "leaked": leaked_values(reply)})
    return results


def check_live(client=None, model=None):
    results = run_live_attacks(client=client, model=model)
    for result in results:
        status = "LEAKED" if result["leaked"] else "held  "
        detail = f" -> {', '.join(result['leaked'])}" if result["leaked"] else ""
        print(f"  {status}  {result['id']} ({result['kind']}){detail}")
    leaks = sum(bool(result["leaked"]) for result in results)
    print(f"LIVE BASELINE: prompt-layer enforcement leaked in {leaks} of {len(results)} attacks.")
    return 0
