"""Command-line interface for the Quantum Key Distribution Simulation Lab."""

from __future__ import annotations

import argparse
import json
from typing import Sequence

from quantum_bb84.protocols.bb84 import simulate_bb84
from quantum_bb84.protocols.e91 import simulate_e91


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(
        prog="quantum_bb84",
        description="Reproducible educational BB84/E91 QKD finite-shot simulations.",
    )
    subcommands = parser.add_subparsers(dest="command", required=True)
    simulate = subcommands.add_parser("simulate", help="run a finite-shot protocol simulation")
    protocols = simulate.add_subparsers(dest="protocol", required=True)

    bb84 = protocols.add_parser("bb84", help="simulate idealized BB84")
    bb84.add_argument("--qubits", type=int, default=1000, help="number of transmitted qubits")
    bb84.add_argument("--seed", type=int, default=None, help="deterministic random seed")
    bb84.add_argument("--eve", choices=["intercept_resend"], default=None, help="optional toy Eve model")
    bb84.add_argument("--eve-rate", type=float, default=0.0, help="probability that Eve intercepts each signal")
    bb84.add_argument("--noise", type=float, default=0.0, help="independent bit-flip noise probability")
    bb84.add_argument("--check-fraction", type=float, default=0.25, help="fraction of sifted bits used for QBER")
    bb84.add_argument("--threshold", type=float, default=0.11, help="toy accept/abort QBER threshold")

    e91 = protocols.add_parser("e91", help="simulate simplified E91-style entangled-pair sifting")
    e91.add_argument("--pairs", type=int, default=1000, help="number of entangled pairs")
    e91.add_argument("--seed", type=int, default=None, help="deterministic random seed")
    e91.add_argument("--noise", type=float, default=0.0, help="independent bit-flip noise probability")
    e91.add_argument("--check-fraction", type=float, default=0.25, help="fraction of sifted bits used for QBER")
    e91.add_argument("--threshold", type=float, default=0.11, help="toy accept/abort QBER threshold")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and print a JSON summary."""

    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "simulate" and args.protocol == "bb84":
        result = simulate_bb84(
            qubits=args.qubits,
            seed=args.seed,
            eve=args.eve,
            eve_rate=args.eve_rate,
            noise_probability=args.noise,
            check_fraction=args.check_fraction,
            threshold=args.threshold,
        )
    elif args.command == "simulate" and args.protocol == "e91":
        result = simulate_e91(
            pairs=args.pairs,
            seed=args.seed,
            noise_probability=args.noise,
            check_fraction=args.check_fraction,
            threshold=args.threshold,
        )
    else:  # pragma: no cover - argparse prevents this path.
        parser.error("unsupported command")
    print(json.dumps(result.summary(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
