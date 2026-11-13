#!/usr/bin/env python3
"""
Generate deliberately weak RSA keys for the RsaCtfTool lab, plus one
correctly generated control key.

Every key here is created locally, on purpose, for a teaching lab.
Nothing here targets a real-world key.

Keys are written as PEM public keys (and, where useful, the matching
private values) into ../keys/.
"""
import json
import time
from pathlib import Path

from Crypto.PublicKey import RSA
from Crypto.Util.number import getPrime, isPrime, inverse

OUT = Path(__file__).resolve().parent.parent / "keys"
OUT.mkdir(exist_ok=True)

E = 65537


def save_pub(name, n, e):
    key = RSA.construct((n, e))
    (OUT / f"{name}.pub").write_bytes(key.publickey().export_key())


def save_meta(name, **kwargs):
    (OUT / f"{name}.json").write_text(json.dumps(kwargs, indent=2, default=str))


def gen_close_primes(bits=1024):
    """Fermat's weakness: p and q are too close together."""
    p = getPrime(bits // 2)
    # q close to p: walk upward from p by a small random-ish offset,
    # staying prime. This mimics a bad RNG that reuses entropy.
    q = p + 2
    while not isPrime(q):
        q += 2
    n = p * q
    save_pub("fermat", n, E)
    save_meta("fermat", bits=bits, p=p, q=q, n=n, e=E, flaw="p and q differ by a tiny amount")


def gen_small_d(bits=1024):
    """Wiener's attack: private exponent d is too small (d < N^0.25 / 3)."""
    while True:
        p = getPrime(bits // 2)
        q = getPrime(bits // 2)
        n = p * q
        phi = (p - 1) * (q - 1)
        # Target a small d, then derive e = d^-1 mod phi.
        d_bits = bits // 4 - 16  # comfortably inside Wiener's bound
        d = getPrime(d_bits)
        if d >= phi:
            continue
        try:
            e = inverse(d, phi)
        except ValueError:
            continue
        if e < 2 or e >= phi:
            continue
        save_pub("wiener", n, e)
        save_meta("wiener", bits=bits, p=p, q=q, n=n, e=e, d=d, flaw="private exponent d is abnormally small")
        return


def gen_shared_prime(bits=1024):
    """Common-factor attack: two different keys reuse the same prime p.

    This simulates a weak/broken RNG shared across two key-generation
    events (a real incident class, e.g. embedded devices seeding RNGs
    from similar boot-time entropy).
    """
    p = getPrime(bits // 2)
    q1 = getPrime(bits // 2)
    q2 = getPrime(bits // 2)
    n1, n2 = p * q1, p * q2
    save_pub("commonfactor_a", n1, E)
    save_pub("commonfactor_b", n2, E)
    save_meta(
        "commonfactor",
        bits=bits, p=p, q1=q1, q2=q2, n1=n1, n2=n2, e=E,
        flaw="two keys generated with a shared prime factor",
    )


def gen_control(bits=2048):
    """A properly generated RSA-2048 key: the baseline that should resist everything."""
    key = RSA.generate(bits, e=E)
    (OUT / "control.pub").write_bytes(key.publickey().export_key())
    save_meta("control", bits=bits, e=E, flaw="none (properly generated RSA-2048)")


if __name__ == "__main__":
    t0 = time.time()
    gen_close_primes()
    gen_small_d()
    gen_shared_prime()
    gen_control()
    print(f"Keys generated in {time.time() - t0:.2f}s -> {OUT}")
    for f in sorted(OUT.glob("*.pub")):
        print(" -", f.name)
