# Breaking Weak RSA on Purpose

A small, reproducible lab that generates deliberately weak RSA keys and breaks them
with [RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool), alongside a properly
generated RSA-2048 control key that resists every attack. Written to accompany a
Medium article on why RSA keys fail in practice, not in theory.

## What's here

| Path | What it is |
|---|---|
| `scripts/generate_keys.py` | Generates 5 keys: 3 deliberately weak (Fermat, Wiener, shared-factor pair) and 1 sound RSA-2048 control |
| `scripts/run_lab.sh` | Runs all 4 experiments end to end and times each one |
| `keys/` | Generated keys (public keys as `.pub`, metadata incl. the real p/q/d as `.json` so you can verify the math) |
| `results/results.md` | Raw command output and timings from the run used in the article |

## Reproduce it

```bash
git clone <this-repo>
cd rsa-lab
python3 -m venv venv && source venv/bin/activate
pip install git+https://github.com/RsaCtfTool/RsaCtfTool.git
./scripts/run_lab.sh
```

Expect the three weak keys to fall in well under a second each, and the control key
to resist every attack within its timeout.

## The four experiments

1. **Fermat's attack** — p and q chosen too close together.
2. **Wiener's attack** — private exponent d chosen too small.
3. **Common-factor attack** — two separate keys generated with a shared prime.
4. **Control** — a sound RSA-2048 key, attacked with all of the above plus two
   general-purpose factoring methods, as a negative control.

## Why this matters

None of these are flaws in RSA the algorithm. They are flaws in how a specific key
was generated — usually traceable to weak, reused, or insufficiently seeded
randomness. The same failure class is behind real incidents such as the
[ROCA vulnerability](https://en.wikipedia.org/wiki/ROCA_vulnerability) in
smart-card and TPM key generation.

## Ethics and scope

Every key here was generated locally, specifically for this lab. RsaCtfTool is a
CTF/educational tool; use it only on keys you own or are explicitly authorized to
test. See the [upstream project](https://github.com/RsaCtfTool/RsaCtfTool) for the
full list of supported attacks.

## Author

Gabriele Fusi — transitioning from financial/insurance consulting into
cybersecurity and data/AI.
