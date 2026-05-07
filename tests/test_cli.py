import json
import subprocess
import sys


def run_cli(*args: str) -> dict[str, object]:
    completed = subprocess.run(
        [sys.executable, "-m", "quantum_bb84", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def test_cli_smoke_bb84_without_eve():
    summary = run_cli("simulate", "bb84", "--qubits", "32", "--seed", "42")

    assert summary["protocol"] == "BB84"
    assert summary["qubits"] == 32
    assert summary["seed"] == 42
    assert summary["eve"] is None


def test_cli_smoke_bb84_with_intercept_resend_eve():
    summary = run_cli(
        "simulate",
        "bb84",
        "--qubits",
        "64",
        "--eve",
        "intercept_resend",
        "--eve-rate",
        "0.2",
        "--seed",
        "42",
    )

    assert summary["protocol"] == "BB84"
    assert summary["eve"] == "intercept_resend"
    assert summary["eve_rate"] == 0.2


def test_cli_smoke_e91():
    summary = run_cli("simulate", "e91", "--pairs", "32", "--seed", "42")

    assert summary["protocol"] == "E91-simplified"
    assert summary["pairs"] == 32
    assert summary["seed"] == 42
