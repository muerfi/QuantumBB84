# BB84 Protocol Overview

BB84 is a quantum key distribution protocol where Alice and Bob build a shared secret key while checking for eavesdropping.

## Core flow

1. **Preparation (Alice)**
   - Generate random data bits.
   - Generate random bases (Z or X).
   - Encode each bit in the chosen basis and send qubits to Bob.

2. **Measurement (Bob)**
   - Choose random bases (Z or X).
   - Measure each received qubit.

3. **Sifting (public discussion)**
   - Alice and Bob reveal only their basis choices.
   - Keep indices where bases matched; discard the rest.

4. **Parameter estimation**
   - Reveal part of the sifted bits as check bits.
   - Estimate the quantum bit error rate (QBER).

5. **Decision**
   - If QBER is too high, abort.
   - Otherwise continue with error correction and privacy amplification.

## Interception intuition

In a simple intercept-resend attack, Eve's random basis guesses introduce extra errors. In ideal conditions, this raises the expected QBER and can be detected statistically.

## Important implementation note

A simulation can illustrate BB84 logic, but real deployment security depends on hardware behavior, finite-key effects, authentication of the classical channel, and implementation-specific countermeasures.
