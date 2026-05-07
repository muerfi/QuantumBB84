# References and Background Topics

This repository is educational. The items below are starting points for scientific context, not a complete bibliography and not a substitute for current security proofs or implementation-security literature.

## Foundational references

- Bennett and Brassard, 1984: the original BB84 quantum cryptography proposal, commonly cited under the title "Quantum cryptography: Public key distribution and coin tossing."
- Ekert, 1991: the original entanglement-based QKD proposal based on Bell's theorem.
- Reviews and lecture notes on quantum key distribution, finite-key security, and practical implementation security.

No DOI list is provided here because this document intentionally avoids adding unchecked bibliographic metadata.

## Suggested background topics

If you are using this repository for study, useful topics to search in textbooks, review articles, or course notes include:

- BB84 protocol;
- E91 protocol;
- quantum key distribution;
- quantum bit error rate;
- basis reconciliation and key sifting;
- intercept-resend attack;
- Bell inequalities and CHSH tests;
- finite-key security;
- error correction for QKD;
- privacy amplification;
- authenticated classical channels;
- weak coherent pulses and photon-number splitting;
- detector efficiency, dark counts, and channel loss;
- side-channel attacks and practical QKD implementation security;
- composable cryptographic security definitions.

## How to use references with this project

When comparing the code to the literature, keep the model boundary clear:

- Literature may describe formal protocols and security proofs under explicit assumptions.
- This repository implements idealized finite-shot simulations and toy attack sketches.
- Agreement with a simple simulation trend is not the same as proving real-system security.
- If a new document adds exact citations, verify titles, authors, venues, years, and identifiers against reliable sources before committing them.
