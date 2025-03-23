# BB84 Attack Simulations

## PNS Attack (Photon Number Splitting)
- **Principle**: Exploits multi-photon pulses to extract bits without disturbing Bob.
- **File**: `PNS_Attack.py`
- **Mathematics**: \( P(k \geq 2) = 1 - e^{-\mu} - \mu e^{-\mu} \).

## Beam Split Attack
- **Principle**: Eve splits the signal and measures a fraction of the photons.
- **File**: `Beam_Split_Attack.py`
- **Physics**: Transformation \( |\psi\rangle \to \sqrt{1-\tau}|\psi\rangle_{\text{Bob}} + \sqrt{\tau}|\psi\rangle_{\text{Eve}} \).
