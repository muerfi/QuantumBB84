# Repository Audit: Quantum Key Distribution Simulation Lab

Date: 2026-05-07
Repository audited: `muerfi/QuantumBB84`
Scope: audit only; no refactor, deletion, package reorganization, or code rewrite is proposed as an implemented change here.

## Executive summary

The repository already has a useful educational core: compact BB84 and E91 scripts, notes on physical intuition, attack-oriented sketches, and practical caveats. The current README is also appropriately cautious in several places: it describes the project as educational and explicitly states that it is not production-grade security software.

However, the codebase is not yet a rigorous scientific Python/Qiskit laboratory. It is a collection of prototypes, notes, duplicated simulations, and exploratory scripts with inconsistent assumptions. The largest technical issues are duplicated BB84 logic, fragile Qiskit execution patterns, no reproducible seed control, no tests, hard-coded tiny experiment sizes, unstructured outputs, path-dependent plotting scripts, and ambiguous separation between reusable code and experiments. The largest scientific/documentation issues are that several attack scripts use names associated with real implementation attacks while implementing only loose toy sketches; some messages print phrases such as "Secure key" or "attack successful" without enough qualification; and E91 is presented as an entanglement-based key-generation demonstration rather than a full E91 security workflow, which should remain explicit.

The recommended direction is to preserve the educational spirit while gradually moving toward a small installable package named `quantum_bb84`, with protocol modules, attack toy models, analysis utilities, simulation runners, tests, documented assumptions, and reproducible experiment outputs.

## Current repository state

### Top-level layout observed

```text
.
├── Attacks/
│   ├── Attack_q-bits.py
│   ├── BeamSplit-Attack.py
│   ├── PNS_Attack.py
│   └── README.md
├── Docs/
│   ├── BB84_Protocol.md
│   ├── Equations/
│   │   ├── QuantumBB84_Equation.pdf
│   │   ├── figs/
│   │   └── scripts/
│   ├── Philosophy.md
│   ├── Practical-limits.md
│   ├── Quantum_Info.md
│   └── Quantum_Physics.md
├── Experiments/
│   └── simulation.md
├── Protocols/
│   ├── BB84/
│   │   ├── BB84_Simulation.py
│   │   └── README.md
│   ├── E91/
│   │   ├── E91_Simulation.py
│   │   └── README.md
│   └── README.md
├── Quantum_security/
│   ├── BB84_No_Eve.py
│   ├── BB84_Simulation.py
│   ├── BB84_With_Eve.py
│   ├── Interactive-visualization.py
│   ├── Multirun-stats.py
│   ├── Noise_Analysis.py
│   └── utils.py
├── Resources/
│   ├── glossary.md
│   └── references.md
├── LICENSE
└── README.md
```

### File classification

| File or directory | Current role | Notes |
|---|---|---|
| `README.md` | Project overview | Good educational framing; already avoids many strong production-security claims. Needs future alignment with a package/CLI once implemented. |
| `Docs/BB84_Protocol.md` | Educational note | Clear protocol-level overview. Should later add explicit assumptions, finite-shot caveats, and references to concrete code paths. |
| `Docs/Quantum_Physics.md` | Educational note | Useful conceptual background. Should remain non-claim-heavy and tied to simulation assumptions. |
| `Docs/Quantum_Info.md` | Educational note | Appropriate lightweight information-theoretic framing; not a formal proof. |
| `Docs/Practical-limits.md` | Educational/practical caveat note | Important to preserve because it counters overclaiming. Needs expansion as project becomes more polished. |
| `Docs/Philosophy.md` | Reflective note | Preserve as optional context, but keep separate from technical claims. |
| `Docs/Equations/QuantumBB84_Equation.pdf` | Report artifact | Preserve if it is original project material, but its assumptions should be reviewed before being cited as project authority. |
| `Docs/Equations/figs/*.png` | Figure artifacts | Preserve until regenerated from reproducible scripts. Later decide whether they are source figures or generated outputs. |
| `Docs/Equations/scripts/*.py` | Exploratory plotting scripts | Outdated/fragile: save paths are hard-coded to `C:/Users/`, and scripts do not declare output filenames or seeds. |
| `Experiments/simulation.md` | Legacy experiment note | Useful as a historical note. Not a reproducible experiment record yet. |
| `Resources/glossary.md` | Educational reference | Preserve; later expand and standardize terminology. |
| `Resources/references.md` | Reference list | Preserve, but replace bare/old documentation links with specific citations and avoid unsupported reference sprawl. |
| `Protocols/README.md` | Protocol comparison note | Useful and cautious. Should later point to runnable, tested modules. |
| `Protocols/BB84/README.md` | Implementation note | Useful. Future version should describe exact model assumptions and limitations. |
| `Protocols/BB84/BB84_Simulation.py` | Reusable-code candidate / prototype | Best current BB84 entry point because it includes intercept probability and `sample_counts`, but it is still script-style and not a tested API. |
| `Protocols/E91/README.md` | Implementation note | Good caveat that no full CHSH/Bell workflow exists. Preserve. |
| `Protocols/E91/E91_Simulation.py` | Reusable-code candidate / prototype | Minimal E91-style entangled-pair demo. Needs scientific review of measurement settings and bit mapping before being treated as rigorous E91. |
| `Quantum_security/utils.py` | Reusable helper code | Most reusable current code. Needs deterministic RNG option, validation, and clearer naming. |
| `Quantum_security/BB84_Simulation.py` | Duplicated prototype | Duplicates `Protocols/BB84/BB84_Simulation.py` with different behavior and assumptions. Candidate for merge/rewrite. |
| `Quantum_security/BB84_No_Eve.py` | Duplicated prototype | Split variant of BB84. Candidate for replacement by parameterized BB84 simulation. |
| `Quantum_security/BB84_With_Eve.py` | Duplicated prototype | Split variant of BB84. Candidate for replacement by parameterized intercept-resend model. |
| `Quantum_security/Noise_Analysis.py` | Exploratory analysis script | Useful idea, but fragile output path, hard-coded parameters, and simplistic noise model. Candidate for experiment module after validation. |
| `Quantum_security/Multirun-stats.py` | Exploratory statistical script | Important direction, but currently hard-coded, non-reproducible, and not integrated with a results schema. |
| `Quantum_security/Interactive-visualization.py` | Exploratory visualization script | Useful visualization idea; file name prevents normal module import and output path is fixed. |
| `Attacks/PNS_Attack.py` | Attack toy model | Name is stronger than implementation. Needs explicit toy-model caveat and a scientifically reviewed model if retained. |
| `Attacks/BeamSplit-Attack.py` | Attack toy model | Same concern; file name with hyphen prevents normal import. |
| `Attacks/Attack_q-bits.py` | Exploratory/coherent-attack sketch | Needs renaming and scientific review. Current "coherent attack" model is not a full adversarial model. |

## Main technical problems

### 1. Duplicated BB84 implementations

The repository contains multiple BB84 variants:

- `Quantum_security/BB84_Simulation.py`
- `Quantum_security/BB84_No_Eve.py`
- `Quantum_security/BB84_With_Eve.py`
- `Protocols/BB84/BB84_Simulation.py`
- Repeated BB84 logic inside `Noise_Analysis.py`, `Multirun-stats.py`, `Interactive-visualization.py`, and the attack scripts.

These scripts repeat the same steps: random bit/basis generation, Qiskit circuit preparation, optional Eve action, Bob measurement, basis comparison, check-bit extraction, and QBER computation. Because each script implements these steps slightly differently, the repository has inconsistent assumptions and no single authoritative simulation path.

Future work should extract one BB84 model with explicit configuration parameters and use it everywhere.

### 2. Fragile Qiskit usage

Several scripts import `execute` and `Aer` directly from `qiskit`:

```python
from qiskit import QuantumCircuit, execute, Aer
```

This is fragile across Qiskit versions. In many modern setups, Aer is provided by `qiskit_aer`, and legacy `execute`-based workflows may require updates. This audit environment does not currently have Qiskit installed, so runtime compatibility could not be verified.

Other Qiskit fragility:

- Several scripts choose `list(result.get_counts().keys())[0]`, which selects an arbitrary observed bitstring rather than sampling or analyzing the full distribution.
- Some scripts execute partially measured circuits inside loops, then keep mutating the same circuit.
- The bit-order convention is implicit and repeatedly handled by reversing strings with `[::-1]`.
- `shots` is sometimes set to 1024 and then only one bitstring is selected; this loses most finite-shot information.
- The simulator backend is created inside loops in some attack scripts.

### 3. No installable package and weak import structure

The repository uses top-level folders such as `Quantum_security`, `Protocols`, and `Attacks`, but none appear to be proper Python packages with `__init__.py`, packaging metadata, or a documented import strategy. Scripts rely on imports such as:

```python
from Quantum_security.utils import generate_random_bits, compare_bases, extract_key
```

This may work from the repository root but can fail when invoked from another working directory, from tests, or after packaging. File names such as `Attack_q-bits.py`, `BeamSplit-Attack.py`, `Interactive-visualization.py`, and `Multirun-stats.py` cannot be imported as normal Python modules because of hyphens.

### 4. Missing tests

No test directory or test files were found. The current project has no automated checks for:

- basis reconciliation correctness;
- QBER computation;
- key/check split behavior;
- intercept-resend expected error behavior;
- reproducible seeded runs;
- finite-shot confidence intervals;
- E91 correlation conventions;
- noise model behavior;
- CLI behavior;
- documentation examples.

A basic `python -m py_compile` check passed, but that only confirms syntax validity and does not validate imports, runtime behavior, scientific assumptions, or reproducibility.

### 5. No reproducible random seed control

`Quantum_security/utils.py` uses `secrets` for bit generation. That is a reasonable choice for cryptographic randomness in a real application, but this repository is an educational simulation lab. Reproducibility matters more than cryptographic randomness here. Experiments should accept a seed and use a controlled random generator for simulation. If a CSPRNG example is retained, it should be clearly separated from reproducible experiments.

The current mixture of `secrets`, `random.SystemRandom`, and `numpy.random` prevents exact reruns.

### 6. Hard-coded tiny parameters

Most scripts use `n = 4`, `total_qubits = 4 * n`, and fixed thresholds such as `0.05`. These values are useful for a short console demo but too small for serious finite-shot behavior. With very small check samples, QBER estimates are extremely noisy and thresholds are not meaningful in a rigorous statistical sense.

### 7. Unstructured outputs

Outputs are mostly printed to stdout or saved to fixed paths:

- `Experiments/noise_impact.png`
- `Experiments/multi_run_stats.csv`
- `Experiments/distribution.html`
- `C:/Users/` in equation plotting scripts

There is no run configuration record, seed record, schema, timestamped output directory, or machine-readable summary that would allow results to be reproduced later.

### 8. Weak naming conventions

Current names mix casing and styles:

- `Quantum_security` uses mixed case and underscore.
- `Protocols` and `Attacks` are capitalized directories.
- Some files use hyphens and cannot be imported.
- `Attack_q-bits.py` is vague.
- `PNS_Attack.py` and `BeamSplit-Attack.py` sound like real attack implementations but are only toy sketches.
- `Multirun-stats.py` and `Interactive-visualization.py` are scripts, not modules.

Future package names should be lowercase, importable, and precise.

### 9. No dependency management

The README lists installation commands, but the repository has no `pyproject.toml`, `requirements.txt`, lock file, optional dependency groups, or tested version range. This makes Qiskit/Aer compatibility especially fragile.

### 10. No result schema or experiment registry

The project currently lacks a standard result object. A serious simulation lab should record at least:

- protocol name;
- model assumptions;
- number of transmitted qubits or entangled pairs;
- basis choices distribution;
- seed;
- backend/simulator version;
- noise parameters;
- Eve/attack parameters;
- sifted-key length;
- check-bit count;
- observed QBER;
- confidence interval or uncertainty estimate;
- abort/pass decision and threshold;
- warnings about invalid or underpowered configurations.

## Main scientific and documentation problems

### 1. "Secure key" language should be softened

Several scripts print phrases such as "Secure key", "Secure key successfully exchanged", or "attack successful without detection". In an educational toy simulation, these messages are too strong unless carefully qualified. Better wording would be:

- "candidate sifted key accepted under this toy threshold";
- "toy intercept-resend disturbance not detected in this finite sample";
- "simulation accepted; this is not a real security guarantee".

The README is already more careful than some scripts. Future code output should match that caution.

### 2. Attack scripts need stronger caveats

`PNS_Attack.py`, `BeamSplit-Attack.py`, and `Attack_q-bits.py` are useful as motivation, but their names map to real QKD implementation-attack concepts. Their implementations are not full physical or adversarial models. For example:

- A photon-number-splitting attack depends on source photon-number statistics, channel loss, Eve's quantum memory assumptions, basis disclosure timing, and decoy-state countermeasures.
- A beam-splitting model should distinguish lossy optical channels, multi-photon pulses, detection probabilities, and Eve's information, not just copy states into separate circuits.
- A coherent attack sketch based on a small custom unitary is not a complete coherent attack security analysis.

These should remain explicitly labeled as toy sketches unless replaced by better-scoped models.

### 3. E91 is not yet a full E91 protocol implementation

The E91 README correctly says the current script does not implement a full CHSH/Bell-test workflow. That caveat should remain prominent. The script currently demonstrates entangled-pair preparation and matching-basis key extraction, but a rigorous E91 module would need:

- documented measurement settings;
- correlation convention and bit mapping;
- CHSH or Bell-inequality statistic if claiming E91-like security intuition;
- finite-shot uncertainty;
- acceptance criteria;
- clear distinction from BBM92-style key extraction.

### 4. Finite-shot statistics are underdeveloped

The repository mentions finite-shot behavior in README-style prose, and `Multirun-stats.py` exists, but there is no coherent statistical treatment. A serious lab should not report single-run QBER as if it were stable. It should include binomial uncertainty, confidence intervals or credible intervals, and warnings for small check-bit counts.

### 5. Noise and eavesdropping are not cleanly separated

Some scripts compare "with Eve" and "without Eve" under a simple threshold, and `Noise_Analysis.py` adds depolarizing errors. The documentation should consistently explain that observed QBER can be caused by device noise, channel noise, alignment errors, finite sampling, or adversarial disturbance. A threshold crossing is not automatically proof of Eve, and a threshold pass is not proof of absence of Eve.

### 6. Error correction and privacy amplification are described but not implemented

Documentation mentions error correction and privacy amplification as protocol steps. The current code does not implement them as real post-processing modules. This is acceptable, but future docs should consistently say the output is a candidate sifted key or toy accepted key, not a final composably secure key.

### 7. References are sparse

`Resources/references.md` lists foundational papers and introductory material. That is better than fake references, but future rigorous documentation should include precise bibliographic details and avoid citing broad documentation pages as scientific support. Any expanded reference list should be curated, not padded.

## Documentation overclaim check

The current README and most docs are generally cautious. Positive findings:

- `README.md` says the repository is educational and not production-grade security software.
- `Protocols/README.md` notes that this is not a complete secure communications stack.
- `Protocols/E91/README.md` states that no full CHSH/Bell workflow exists.
- `Attacks/README.md` says the attack scripts are exploratory and not full security analyses.
- `Docs/Quantum_Info.md` says the intuition is not a full proof.
- `Docs/Practical-limits.md` discusses deployment limitations.
- `Docs/Philosophy.md` explicitly qualifies "security from physics" as conditional.

Main remaining overclaim risks:

- Console messages in code are stronger than docs and may imply real security.
- Attack script names can imply more scientific completeness than the code provides.
- The phrase "detecting eavesdropping" should often be qualified as "detecting excess disturbance statistically under the model assumptions".
- E91 should not be presented as a full E91 security demonstration until CHSH/Bell statistics and acceptance criteria exist.
- QBER thresholds should not be treated as universal; they depend on protocol variant, finite-key analysis, noise model, and post-processing assumptions.

## Suggested target architecture

This is a proposal only. It should not be implemented until the audit has been reviewed.

```text
quantum_bb84/
  __init__.py
  __main__.py
  protocols/
    __init__.py
    bb84.py
    e91.py
  attacks/
    __init__.py
    intercept_resend.py
    photon_number_splitting.py
    beam_splitting.py
  analysis/
    __init__.py
    qber.py
    statistics.py
    key_rates.py
  visualization/
    __init__.py
    plots.py
  simulation/
    __init__.py
    runner.py
    noise.py
  utils/
    __init__.py
    random.py
    validation.py
```

### Package responsibilities

#### `quantum_bb84.protocols.bb84`

Should contain protocol-level BB84 logic that is independent of plotting or CLI concerns:

- generate Alice bits and bases;
- prepare circuits or simulate ideal basis outcomes;
- model Bob basis choices and measurements;
- perform sifting;
- partition sifted bits into key/check sets;
- return structured results.

It should distinguish:

- ideal noiseless BB84;
- finite-shot BB84;
- BB84 with explicit toy intercept-resend;
- BB84 with simple channel/device noise.

#### `quantum_bb84.protocols.e91`

Should contain entanglement-based simulation logic:

- Bell-pair preparation;
- measurement-setting selection;
- correlation extraction;
- optional key-basis extraction;
- optional CHSH statistic once scientifically reviewed.

It should avoid claiming full E91 security until Bell-test logic and finite-shot acceptance criteria are implemented.

#### `quantum_bb84.attacks.intercept_resend`

Should implement the simple attack that is already closest to the repository's current code:

- Eve chooses bases;
- Eve measures a configurable subset of transmissions;
- Eve resends according to her outcome and basis;
- result object records Eve's basis choices, intercept mask, and toy information estimate if computed.

#### `quantum_bb84.attacks.photon_number_splitting`

Should initially be marked experimental/toy. If retained, it should model assumptions explicitly:

- source photon-number distribution;
- probability of multiphoton pulse;
- channel loss assumption;
- Eve storage assumption;
- whether decoy states are absent.

#### `quantum_bb84.attacks.beam_splitting`

Should initially be marked experimental/toy. It should not imply a complete physical optics model unless implemented.

#### `quantum_bb84.analysis.qber`

Should provide pure, tested functions:

- mismatch count;
- QBER;
- handling empty check sets;
- per-basis QBER if needed;
- confidence intervals or uncertainty wrappers.

#### `quantum_bb84.analysis.statistics`

Should provide finite-shot support:

- binomial standard error;
- confidence intervals;
- repeated-run aggregation;
- warnings for low sample sizes;
- seed-aware reproducibility helpers.

#### `quantum_bb84.analysis.key_rates`

Should initially be conservative. It may include toy asymptotic estimates only if labeled as such. It should not imply deployable secret-key-rate certification.

#### `quantum_bb84.simulation.runner`

Should orchestrate protocol, attack, noise, analysis, and output serialization. This is where CLI commands should call into the package.

#### `quantum_bb84.simulation.noise`

Should hold simple noise models with explicit assumptions:

- bit-flip noise;
- basis-independent depolarizing noise;
- measurement error;
- loss placeholders if later supported.

#### `quantum_bb84.visualization.plots`

Should generate reproducible figures from structured result files, not from hidden global variables.

#### `quantum_bb84.utils.random`

Should expose seeded RNG support for reproducible simulation. If CSPRNG examples remain, they should be opt-in and documented as non-reproducible.

#### `quantum_bb84.utils.validation`

Should validate configuration ranges:

- probabilities in `[0, 1]`;
- positive qubit/pair counts;
- sufficient check-bit sizes;
- supported protocols and attacks;
- compatible combinations of protocol, attack, and noise model.

## Suggested CLI design

Proposal only:

```bash
python -m quantum_bb84 simulate bb84 --qubits 1000 --eve intercept_resend --noise 0.02 --seed 42
python -m quantum_bb84 simulate e91 --pairs 1000 --seed 42
python -m quantum_bb84 analyze qber --input results/run.json
python -m quantum_bb84 plot qber-vs-eve
```

### CLI principles

- Every simulation command should accept `--seed`.
- Every simulation command should write a structured output file by default or with `--output`.
- Console output should be a concise summary, not the only record.
- The CLI should print warnings for underpowered finite-shot configurations.
- The CLI should avoid words such as "secure" unless heavily qualified.
- Attack options should be clearly labeled as toy models unless rigorous assumptions are implemented.

### Possible command breakdown

```bash
python -m quantum_bb84 simulate bb84 \
  --qubits 1000 \
  --key-fraction 0.5 \
  --check-fraction 0.5 \
  --eve none \
  --noise 0.0 \
  --seed 42 \
  --output results/bb84_ideal_seed42.json
```

```bash
python -m quantum_bb84 simulate bb84 \
  --qubits 1000 \
  --eve intercept_resend \
  --intercept-probability 0.5 \
  --seed 42 \
  --output results/bb84_intercept_resend_seed42.json
```

```bash
python -m quantum_bb84 analyze qber \
  --input results/bb84_intercept_resend_seed42.json \
  --confidence 0.95
```

```bash
python -m quantum_bb84 plot qber-vs-eve \
  --inputs results/sweep/*.json \
  --output figures/qber_vs_eve.png
```

## Suggested experiment structure

A rigorous lab should separate source code, experiment definitions, generated results, and figures.

```text
experiments/
  bb84_intercept_resend_sweep.yaml
  bb84_noise_sweep.yaml
  e91_correlation_demo.yaml
results/
  .gitkeep
figures/
  .gitkeep
notebooks/
  exploratory/
```

Recommended policy:

- Commit experiment configuration files.
- Do not commit large generated result files by default.
- Commit small golden result fixtures only for tests.
- Every result file should include the simulation config and package version.
- Every figure should be reproducible from a named result file or experiment config.

### Suggested result schema

```json
{
  "schema_version": "0.1",
  "protocol": "bb84",
  "model_scope": "idealized_simulation",
  "seed": 42,
  "backend": {
    "name": "qiskit_aer_aer_simulator",
    "shots": 1
  },
  "configuration": {
    "transmitted_qubits": 1000,
    "eve": {
      "model": "intercept_resend_toy",
      "intercept_probability": 0.5
    },
    "noise": {
      "model": "bit_flip_toy",
      "probability": 0.02
    }
  },
  "sifting": {
    "matching_basis_count": 501,
    "check_bit_count": 250,
    "candidate_key_length": 251
  },
  "analysis": {
    "qber": 0.128,
    "qber_confidence_interval": [0.089, 0.171],
    "accepted_under_toy_threshold": false,
    "threshold": 0.05
  },
  "warnings": [
    "This is an idealized educational simulation, not a real-world security proof."
  ]
}
```

## Suggested test strategy

### Unit tests

Add tests for pure functions first:

- random basis generation shape and value range;
- `compare_bases` behavior;
- key/check split behavior;
- QBER on identical arrays, fully different arrays, and partially different arrays;
- validation of probabilities and positive counts;
- empty check-bit handling;
- bit-order conversion helpers.

### Deterministic simulation tests

After adding seeded RNG support:

- fixed seed produces identical BB84 result object;
- no-Eve/no-noise ideal BB84 has zero QBER on matching bases in a sufficiently direct simulator path;
- intercept-resend with high intercept probability increases average QBER over many seeded trials;
- noise probability sweep increases expected average QBER under the selected toy model;
- invalid configurations fail with clear errors.

### Statistical tests

Use statistical tests carefully. Avoid brittle assertions on one random run. Prefer:

- deterministic seeds;
- repeated runs with aggregate bounds;
- tolerance intervals appropriate to binomial variation;
- small fast tests for CI and optional slower experiment tests.

### Documentation tests

- Run README quick-start commands once a CLI exists.
- Ensure examples write outputs to temporary directories.
- Check that docs do not contain unqualified production-security claims.

### Compatibility checks

At minimum:

```bash
python -m py_compile $(rg --files -g '*.py')
pytest
ruff check .
python -m quantum_bb84 --help
```

Once packaging exists, add CI for a pinned supported Python/Qiskit matrix.

## Suggested documentation roadmap

### Phase 1: Make current scope explicit

- Add a project identity statement: "Quantum Key Distribution Simulation Lab".
- Keep the non-production caveat in the README.
- Replace strong console wording in scripts with qualified simulation language.
- Add `docs/AUDIT.md` as the planning baseline.

### Phase 2: Document assumptions per model

Add short model cards:

- `docs/models/bb84_ideal.md`
- `docs/models/intercept_resend_toy.md`
- `docs/models/noise_bit_flip.md`
- `docs/models/e91_entanglement_demo.md`
- `docs/models/pns_toy.md`
- `docs/models/beam_splitting_toy.md`

Each model card should include:

- what is simulated;
- what is not simulated;
- input parameters;
- expected qualitative behavior;
- known limitations;
- references if applicable.

### Phase 3: Reproducible experiments

- Add experiment configuration files.
- Add result schema documentation.
- Add instructions for regenerating figures.
- Make finite-shot uncertainty visible in plots and tables.

### Phase 4: Scientific narrative

Organize docs around the requested separation:

1. idealized simulation;
2. protocol intuition;
3. attack toy models;
4. real-world deployment limitations.

This separation should appear in the README, model cards, CLI help text, and output warnings.

## Files that should be preserved

Preserve these unless manual review finds incorrect content:

- `README.md` — good cautious project overview.
- `Docs/BB84_Protocol.md` — useful protocol overview.
- `Docs/Quantum_Physics.md` — useful conceptual physics note.
- `Docs/Quantum_Info.md` — useful information-theoretic intuition note.
- `Docs/Practical-limits.md` — important practical caveat document.
- `Docs/Philosophy.md` — optional reflective context.
- `Protocols/README.md` — useful BB84/E91 comparison with caveats.
- `Protocols/BB84/README.md` — current BB84 implementation notes.
- `Protocols/E91/README.md` — important E91 limitation statement.
- `Attacks/README.md` — already frames attack scripts as exploratory.
- `Resources/glossary.md` — useful glossary seed.
- `Resources/references.md` — useful starting reference list.
- `Quantum_security/utils.py` — reusable helper seed, though it needs redesign for reproducibility.
- `Protocols/BB84/BB84_Simulation.py` — likely best current BB84 prototype to preserve as reference during refactor.
- `Protocols/E91/E91_Simulation.py` — useful minimal entanglement demo to preserve as reference during refactor.

## Files that may need deletion, merging, or rewrite

Do not delete these immediately. Review, extract any useful behavior, then replace with tested package modules.

| File | Suggested future action | Reason |
|---|---|---|
| `Quantum_security/BB84_Simulation.py` | Merge/rewrite | Duplicates protocol BB84 script with different assumptions. |
| `Quantum_security/BB84_No_Eve.py` | Merge into parameterized BB84 | Should be a configuration, not a separate script. |
| `Quantum_security/BB84_With_Eve.py` | Merge into intercept-resend model | Should be a configuration, not a separate script. |
| `Quantum_security/Noise_Analysis.py` | Rewrite as experiment using `simulation.noise` and `analysis.qber` | Useful idea but hard-coded and non-reproducible. |
| `Quantum_security/Multirun-stats.py` | Rewrite as experiment runner | Useful idea but not seed-controlled and output schema is weak. |
| `Quantum_security/Interactive-visualization.py` | Rewrite under visualization module | Hyphenated filename and fixed output path. |
| `Attacks/PNS_Attack.py` | Rewrite or downgrade explicitly to toy sketch | Current model is not a rigorous PNS attack simulation. |
| `Attacks/BeamSplit-Attack.py` | Rewrite or downgrade explicitly to toy sketch | Current model is not a rigorous beam-splitting simulation. |
| `Attacks/Attack_q-bits.py` | Rename/rewrite | Vague name and scientifically incomplete coherent-attack sketch. |
| `Docs/Equations/scripts/model1.py` | Rewrite plotting path/output | Hard-coded Windows path. |
| `Docs/Equations/scripts/models2.py` | Rewrite plotting path/output | Hard-coded Windows path and simplified formula should be documented. |
| `Docs/Equations/scripts/models3.py` | Rewrite plotting path/output and review formulas | Simplified mutual information expressions need context and caveats. |
| `Docs/Equations/scripts/models4.py` | Rewrite as reproducible noise example | Uses random state without seed and hard-coded Windows path. |
| `Experiments/simulation.md` | Replace with reproducible experiment index | Current file is a legacy note, not a result registry. |

## Risks and manual review points

### Scientific review points

- Validate the BB84 circuit model and bit-order convention against Qiskit measurement semantics.
- Decide whether Qiskit circuits are needed for all BB84 simulations or whether some idealized steps should use direct classical sampling with documented equivalence.
- Review the E91 measurement settings, correlation conventions, and whether the script is closer to E91 or BBM92-style demonstration.
- Define exactly what "QBER" means in each context: check bits only, all sifted bits, per basis, or aggregate.
- Decide how to represent threshold decisions without implying a real finite-key security proof.
- Review all attack model names and claims against actual QKD literature.
- Avoid adding decoy-state, PNS, or coherent-attack claims unless the implemented model supports them.

### Engineering review points

- Choose supported Python and Qiskit/Aer versions.
- Add packaging metadata before reorganizing imports.
- Design a stable result dataclass or schema before adding more experiments.
- Decide whether generated figures/results belong in Git.
- Add CI only after dependencies are pinned enough to be reproducible.
- Ensure examples run from a clean checkout, not only from a local working directory.

### Documentation review points

- Keep the README sober: educational, reproducible, rigorous, not production cryptography.
- Use "candidate key" or "accepted under this toy model" instead of "secure key".
- Make real-world deployment limitations visible near every result that might otherwise look like a security guarantee.
- Cite foundational sources precisely and avoid unsupported claims.
- Keep philosophical material separate from technical claims.

## Recommended next steps

1. Review this audit and decide which current BB84 script should be treated as the reference behavior during refactoring.
2. Add a minimal test suite for `Quantum_security/utils.py` and any pure QBER helpers before changing simulation internals.
3. Introduce packaging metadata and a lowercase package skeleton without deleting legacy scripts.
4. Implement seeded RNG and structured result objects.
5. Port BB84 ideal and intercept-resend behavior into tested package modules.
6. Add CLI commands only after the package API is stable.
7. Treat PNS, beam-splitting, coherent attack, and E91 CHSH features as separate scientifically reviewed milestones.

## Audit checks performed

- Inspected repository structure with `find` and `rg --files`.
- Read top-level README, protocol docs, attack docs, physics/information/practical notes, resources, and Python scripts.
- Ran Python bytecode compilation across all Python files; syntax compilation passed.
- Checked local Qiskit import availability; Qiskit was not installed in this environment, so runtime compatibility of Qiskit scripts was not verified.
