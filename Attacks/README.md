# BB84 Attack Simulations

## PNS Attack (Photon Number Splitting)
- **Principle**: Exploits multi-photon pulses to extract bits without disturbing Bob.
- **File**: `PNS_Attack.py`
- **Mathematics**: \( P(k \geq 2) = 1 - e^{-\mu} - \mu e^{-\mu} \).

## Beam Split Attack
- **Principle**: Eve splits the signal and measures a fraction of the photons.
- **File**: `Beam_Split_Attack.py`
- **Physics**: Transformation \( |\psi\rangle \to \sqrt{1-\tau}|\psi\rangle_{\text{Bob}} + \sqrt{\tau}|\psi\rangle_{\text{Eve}} \).

## PNS Attack (Photon Number Splitting)
- **File**: `PNS_Attack.py`

## Split-Beam Attack
- **File**: `Beam_Split_Attack.py`

## Coherent Attack
- **Principle**: Eve applies a global unitary operation \( U = e^{-i \theta H} \) to correlate her qubits with Alice's.
- **File**: `Coherent_Attack.py`
- **Mathematics**: Minimal disturbance if \( \theta \ll 1 \), but \( I(A:E) \propto \sin^2\theta \).
