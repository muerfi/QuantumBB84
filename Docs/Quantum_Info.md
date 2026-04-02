# Quantum Information Perspective on BB84

This note gives a lightweight information-theoretic view of BB84.

## Entropy intuition

- A perfectly known pure quantum state has zero von Neumann entropy.
- Measurement in incompatible bases can turn certainty into classical uncertainty.
- In BB84 terms: disturbance increases disagreement probability between Alice and Bob.

## Information balance

A useful security intuition is:
- Alice/Bob should share stronger correlations than Alice/Eve.
- If observed error is too high, Alice/Bob assume Eve or excess noise and abort.

This is not, by itself, a full proof. Formal security requires finite-key analysis and rigorous bounds.

## Channel viewpoint

BB84 can be viewed as communication over a noisy channel plus post-processing.

- Sifting keeps only matching-basis events.
- Error correction aligns Alice/Bob strings.
- Privacy amplification compresses the key to reduce possible Eve information.

## Scope of this repository

The code in this project focuses on protocol behavior and intuition, not complete security-parameter estimation or composable-proof tooling.
