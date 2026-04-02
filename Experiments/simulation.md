# Simulation Notes

This file previously contained a long raw console dump from exploratory Qiskit runs.

To keep the repository readable and reproducible, that dump has been removed and replaced with a short summary.

## What was being tested

- BB84 behavior with and without interception.
- Distribution of Bob's measurement outcomes over repeated simulator shots.
- Simple success/failure checks based on check-bit agreement.

## Why the old output was removed

- It mixed legacy backend names and outdated API usage.
- It was difficult to verify line-by-line against the current code.
- The volume of raw output made it harder to find the actual experimental logic.

## Recommended next step

If reproducible experiment reporting is needed, add a script that:
1. fixes random seeds,
2. saves metrics to a structured file (CSV/JSON), and
3. prints a short run summary with configuration + aggregate results.
