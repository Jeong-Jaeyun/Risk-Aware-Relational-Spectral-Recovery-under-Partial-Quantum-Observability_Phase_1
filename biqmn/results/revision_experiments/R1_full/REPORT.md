# R1: finite-clock identifiability experiment

Run type: FULL GRID. Physical/representation qualification passed: True.

This is multi-copy state estimation with a known engineered logical Hamiltonian. The tilted Hamiltonian includes a three-body logical Pauli term. It is not the submitted H_S=0 model, not a physical-noise recovery channel, and not a C3R efficacy experiment.

## Physical checks

- Max null-constraint residual: 1.5781e-16.
- Max conditional-evolution density gap: 1.0081e-15.
- Adjacent clock geometry minimum: 0.14644661.
- POVM completeness error: 1.2578e-16.
- Measurement-design ranks: aligned 1; tilted 3. The clock labels are nonorthogonal POVM outcomes, not eight orthogonal ticks.
- Maximum test/reference fidelity: 0.99912678; no test state is in the bank.

## Fixed display slice: all 8 labels, zero readout error

All grid cells, intervals, q05 fidelity and resource counts are in summary.json. These are initial-state fidelities; known unitary evolution preserves this fidelity for the corresponding trajectories.

| Code | Dynamics | Copies | Raw mixed LS [95% CI] | Occupation spectral LS | Raw pure LS | Raw nearest | Legacy spectral nearest |
|---|---|---:|---|---:|---:|---:|---:|
| bitflip | aligned | 128 | 0.681874 [0.629138, 0.737564] | 0.681874 | 0.681874 | 0.707299 | 0.500000 |
| bitflip | aligned | 512 | 0.681249 [0.628726, 0.736983] | 0.681249 | 0.681249 | 0.715651 | 0.500000 |
| bitflip | aligned | 2048 | 0.681384 [0.628784, 0.737428] | 0.681384 | 0.681384 | 0.707225 | 0.500000 |
| bitflip | tilted | 128 | 0.976273 [0.972899, 0.979356] | 0.976273 | 0.990124 | 0.967869 | 0.500000 |
| bitflip | tilted | 512 | 0.989782 [0.988252, 0.991209] | 0.989782 | 0.997562 | 0.974657 | 0.500000 |
| bitflip | tilted | 2048 | 0.995088 [0.994288, 0.995833] | 0.995088 | 0.999398 | 0.976106 | 0.500000 |
| phaseflip | aligned | 128 | 0.681874 [0.629138, 0.737564] | 0.681874 | 0.681874 | 0.707299 | 0.500000 |
| phaseflip | aligned | 512 | 0.681249 [0.628726, 0.736983] | 0.681249 | 0.681249 | 0.715651 | 0.500000 |
| phaseflip | aligned | 2048 | 0.681384 [0.628784, 0.737428] | 0.681384 | 0.681384 | 0.707225 | 0.500000 |
| phaseflip | tilted | 128 | 0.976273 [0.972899, 0.979356] | 0.976273 | 0.990124 | 0.967869 | 0.500000 |
| phaseflip | tilted | 512 | 0.989782 [0.988252, 0.991209] | 0.989782 | 0.997562 | 0.974657 | 0.500000 |
| phaseflip | tilted | 2048 | 0.995088 [0.994288, 0.995833] | 0.995088 | 0.999398 | 0.976106 | 0.500000 |

## What this can and cannot establish

The original mutual-information/coherence-absolute representations lose the antipodal sign. Under the declared complementary-shot coupling, their pair-averaged fidelity is exactly 0.5. The zero-width interval here is a constructed identifiability control, not a population-risk guarantee.

Occupation spectrum is an invertible encoding of the same signed population data, and must agree with raw mixed LS. Its benefit over legacy features is not a spectral advantage over equal-information estimation. Pure LS additionally uses the known-pure-state prior, so any advantage of that method must not be attributed to spectral processing.

Confidence intervals resample 32 independent target pairs after averaging the fixed measurement seeds. The two codes are basis-equivalent coupled checks, not independent replication. Prepared-copy cost includes all clock-label erasures. Rank-deficient and zero-count cases are retained.

A successful R1 qualifies a physical/observation model for a later recovery study; it does not repair the original spectral gate or validate C3R. No threshold was tuned on these test targets.

Design references: [Page–Wootters constraints and conditioning](https://www.nature.com/articles/s41467-021-21782-4), [reduced-state identifiability](https://arxiv.org/abs/quant-ph/0207109). Numerical findings and the finite-clock construction above are from this local experiment.
