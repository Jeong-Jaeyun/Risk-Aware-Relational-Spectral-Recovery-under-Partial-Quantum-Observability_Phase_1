# Filtered References - Background-Independent Relational Spectral Recovery

The original root README was a working note that classified the uploaded
reference papers. It is kept here so the repository root can serve as the code
and manuscript entry point.

The uploaded 89 papers (`wdw/` 31 papers plus `reference/` 58 papers) were
filtered into 49 papers that align with the main text and supplementary
information.

## Selection Criteria

The filtering was based on the manuscript's core topics:

- Background-independent quantum dynamics / Wheeler-DeWitt constraint
- Page-Wootters mechanism / clock conditioning
- Spectral graph theory / weighted Laplacians
- Graph-to-quantum-state mappings
- Quantum error correction and recovery maps
- Risk-aware control / CVaR / downside risk
- Partial observability / syndrome measurement / noise modeling

## Tiers

### Tier 1 - Core References

Direct support for the method definitions and central equations.

- `A_PageWootters_Relational/`
- `B_Background_Independence/`
- `C_Spectral_Graph_Quantum_States/`
- `D_QEC_Recovery_Tools/`

### Tier 2 - Related Background

Contextual background for the introduction, related work, and discussion.

- `A_WDW_QuantumGravity/`
- `B_PageWootters_Applications/`
- `C_Quantum_Networks/`
- `D_QEC_Codes_and_Subsystems/`
- `E_Error_Mitigation_and_NoiseModeling/`
- `F_NonMarkovian_Noise/`
- `G_Uncertainty_Benchmarking_Measurement/`

### Tier 3 - Peripheral Inspiration

Optional future-work or motivation references.

- `A_AI_ML_for_QC/`
- `B_Spectral_Methods_Inspiration/`
- `C_Quantum_Control_Geometry/`
- `D_Quantum_Information_Measures/`

## Notes

- Cite QuTiP only if the final simulation code actually uses it.
- For Page-Wootters background, use a small core subset in the main text and
  leave the rest for discussion or supplementary context.
- For error mitigation, cite only the papers needed to frame the method as a
  control layer rather than a decoder replacement.
