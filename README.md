# perm-gate

[![ci](https://github.com/jbisaccia-9/perm-gate/actions/workflows/ci.yml/badge.svg)](https://github.com/jbisaccia-9/perm-gate/actions) · [captured results](RESULTS.md)

**Prompt instructions are requests. Permissions are guarantees. This repo
proves the difference with a test suite.**

A toy assistant answers questions over a records store with two enforcement
modes. In **prompt mode**, security is a guard instruction ("never reveal
gov_id or case_notes") and the assistant fetches full records. In
**permission mode**, the credential itself is scoped: restricted fields are
stripped at the data layer, so nothing model-shaped ever holds them. The same
five-attack suite runs against both:

```
prompt mode:      LEAKED 4 of 5   (content injection, roleplay, "anything
                                   sensitive", format pivot)
permission mode:  0 of 5          (the credential cannot fetch what the
                                   prompt cannot protect)
```

The deceptive result is the one that passes: the plain direct ask is refused
in *both* modes — which is exactly why prompt-layer security demos look safe
and fail in production.

## Honesty about the setup

The "assistant" here is **not an LLM** — it is a deliberately naive
instruction-follower built to fail the way injected models fail (it obeys
directives embedded in retrieved content, and its guardrail is wording it can
be argued out of). That naivety is the experimental control. The claim under
test is architectural, not behavioral: prompt-layer security depends on how
the reader behaves; permission-layer security does not. A real model is less
naive on any given day — and the architecture still shouldn't bet on it.

CI enforces both directions: permission mode must show **zero** leaks, and
prompt mode must still **demonstrate** the failure — if the naive agent ever
stops leaking, the gate reports the demo as vacuous and fails the build.

Part of the *-gate* family: [kappa-gate](https://github.com/jbisaccia-9/kappa-gate) ·
[roi-gate](https://github.com/jbisaccia-9/roi-gate) ·
[phi-gate](https://github.com/jbisaccia-9/phi-gate) ·
[trade-gate](https://github.com/jbisaccia-9/trade-gate).

## Quickstart

```
python -m venv .venv
.venv/bin/pip install -U pip
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m pytest -q
.venv/bin/python -m permgate gate permission
.venv/bin/python -m permgate gate prompt
```

All records are fictional; the "identifiers" are labeled fakes. MIT license.
