# Scientific Notes

These notes describe the scientific scope of the Quantum Key Distribution Simulation Lab. They are written to separate accepted protocol ideas from what is actually modeled in this repository.

## What QKD tries to achieve

Quantum key distribution aims to let two parties, conventionally Alice and Bob, establish shared secret key material while using quantum systems and authenticated public discussion to test for disturbance. In a complete cryptographic setting, the resulting key would then be used by a separate symmetric cryptographic system.

A QKD protocol is not just a quantum circuit. A deployable system also needs authenticated classical communication, parameter estimation, error correction, privacy amplification, finite-key security analysis, and an implementation model that accounts for real devices.

## BB84 in this repository

The refactored BB84 model represents the prepare-and-measure protocol at a classical simulation level:

1. Alice samples random bits and random bases.
2. Bob samples random measurement bases.
3. When Bob's basis matches Alice's preparation basis, Bob receives the transmitted bit in the ideal noiseless model.
4. When the bases do not match, Bob's result is sampled as random.
5. Matching-basis positions are retained during sifting.
6. A fraction of sifted bits is used as a public check sample for QBER.
7. Remaining sifted bits are reported as candidate key bits.

Optional components include independent bit-flip noise and a toy intercept-resend eavesdropper. The model is useful for studying protocol mechanics and finite-shot statistics. It is not a proof of BB84 security.

## E91 in this repository

The E91 module is deliberately labeled `E91-simplified`. It models entangled-pair intuition and basis reconciliation:

1. Alice and Bob choose among three basis labels.
2. Matching settings are modeled as correlated outcomes before optional bit-flip noise.
3. Nonmatching settings are discarded during key sifting.
4. A check fraction is used to estimate QBER.

This is not a full E91 implementation. A scientifically complete E91 study would need measurement settings suitable for Bell-test analysis, CHSH or related statistics, explicit acceptance rules, finite-key treatment, and a device/implementation model.

## QBER

The quantum bit error rate is the fraction of compared check bits where Alice and Bob disagree. In this project it is computed as:

```text
QBER = number of mismatched check bits / number of compared check bits
```

QBER is a statistic, not an explanation by itself. A high observed QBER may come from channel noise, detector effects, basis misalignment, implementation bugs, adversarial disturbance, or a small unlucky sample. A low observed QBER in a toy simulation does not prove that no adversary was present.

## Why idealized eavesdropping can cause detectable disturbance

In BB84, the two encoding bases are incompatible. In an ideal intercept-resend sketch, Eve does not know the preparation basis before measuring. If she measures in the wrong basis, her result is not reliable for Alice's original state. When she resends a state based on that result, Bob may later observe errors in positions where Alice and Bob used matching bases. Public comparison of a random check sample can reveal this disturbance statistically.

This repository's intercept-resend attack is a toy model. It does not represent a general adversary, coherent attacks, side-channel attacks, photon-number-splitting attacks, detector-control attacks, or implementation-specific exploits.

## Why simulation is not a security proof

A simulation explores a chosen model. A security proof makes a quantified statement under clearly stated assumptions. These are different activities.

A finite-shot simulation can show that a particular model with a particular seed and parameter set produced a particular QBER and candidate key length. It cannot, by itself, establish composable secrecy, authenticate the classical channel, bound Eve's information in an implementation-independent way, or validate hardware assumptions.

## Practical requirements for real QKD

Real QKD analysis normally has to address at least the following areas:

- **Hardware assumptions:** source state quality, intensity statistics, detector response, timing behavior, calibration, and loss.
- **Authentication:** Alice and Bob need an authenticated classical channel; otherwise an active adversary can impersonate parties.
- **Finite-key analysis:** finite samples require statistical confidence bounds and security parameters.
- **Error correction:** Alice and Bob must reconcile differing sifted strings while accounting for information leaked during reconciliation.
- **Privacy amplification:** reconciled strings must be compressed to reduce any adversary's information.
- **Side-channel analysis:** real devices can leak information outside the ideal protocol model.
- **Implementation security:** software, firmware, random-number generation, device control, logging, and operations all matter.

## Pedagogical simulation versus deployable cryptography

A pedagogical simulation is valuable when it makes assumptions visible and produces reproducible outputs. A deployable cryptographic system requires a much broader engineering and proof framework. This repository belongs to the first category. It can help users learn what BB84 and simplified E91-style sifting are, how QBER is computed, why finite samples fluctuate, and why idealized attacks are only sketches.

The safest interpretation of package output is: "under this idealized finite-shot model and these parameters, the simulated check sample had this QBER and the toy threshold decision was this." It should not be interpreted as a statement about real-world secrecy.
