#!/usr/bin/env bash
# Reproduces every experiment in "Breaking Weak RSA on Purpose".
# Usage: ./scripts/run_lab.sh   (run from the repo root, inside the venv)
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== Generating keys (1 weak-but-sound RSA key per flaw, plus a healthy control) =="
python scripts/generate_keys.py

echo
echo "== Experiment 1: Fermat's attack (close primes) =="
time RsaCtfTool --publickey keys/fermat.pub --attack fermat --private

echo
echo "== Experiment 2: Wiener's attack (small private exponent) =="
time RsaCtfTool --publickey keys/wiener.pub --attack wiener --private

echo
echo "== Experiment 3: Common-factor attack (two keys sharing a prime) =="
time RsaCtfTool --publickey "keys/commonfactor_a.pub,keys/commonfactor_b.pub" --attack common_factors --private

echo
echo "== Experiment 4: Control key (RSA-2048, properly generated) — expected to resist =="
time RsaCtfTool --publickey keys/control.pub \
    --attack fermat wiener pollard_rho pollard_p_1 williams_pp1 \
    --private --timeout 20 || echo "(failure here is the expected, correct outcome)"
