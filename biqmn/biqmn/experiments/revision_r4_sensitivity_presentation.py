"""Render every declared margin and direct paired fidelity contrast for the SI."""
from __future__ import annotations

import json

from .common import REPO_ROOT
from .revision_r4_presentation import ci, table
from .revision_r4_harm_sensitivity import MARGIN_KEYS


def main():
    data = json.loads((REPO_ROOT/'results/revision_experiments/R4_harm_sensitivity/summary.json').read_text())
    harm, fidelity = [],[]
    for stream in data:
        policies = stream['aggregate']['policies']
        h = policies['q50_H']
        u = policies['q50_U']
        for key in MARGIN_KEYS:
            harm.append(' & '.join([
                f"r{stream['stream']}", '$10^{-12}$' if key=='1e-12' else key,
                f"{100*h['margins'][key]['conditional_harm']['estimate']:.2f}",
                f"{100*u['margins'][key]['conditional_harm']['estimate']:.2f}",
                ci(h['differences']['U']['margins'][key]['conditional_harm'],100,2)]))
        for q in (25,50,75):
            h = policies[f'q{q}_H']
            u = policies[f'q{q}_U']
            fidelity.append(' & '.join([
                f"r{stream['stream']}", str(q), f"{h['mean_fidelity']['estimate']:.6f}",
                f"{u['mean_fidelity']['estimate']:.6f}",ci(h['differences']['U']['mean_fidelity'],1,5)]))
    tex = table(
        'Harm-margin sensitivity at 50\\% retention of the original $C_2$ proposals. '
        'A switch is harmful when $F_B<F_A-\\varepsilon$. H and U are the unchanged '
        'batch-ranking rules, with the same expected switching rate in each cell. '
        'Harm columns are percentages among accepted switches, equally averaged over all 24 cells; '
        'the last column is H minus U in percentage points with a paired pointwise 95\\% interval. '
        'The positive margins are sensitivity choices in absolute fidelity units, not validated utility thresholds.',
        'tab:r4-harm-sensitivity', 'llrrl',
        r'Stream & $\varepsilon$ & H harm (\%) & U harm (\%) & $H-U$: harm [95\% CI]', harm)
    tex += table(
        'Direct paired H-minus-U overall mean-fidelity comparison at equal expected switching rates. '
        'Retention $q$ is relative to the original $C_2$ proposal set. Each stream equally averages all '
        '24 cells. These are batch rankings using observed diagnostics without target outcomes, '
        'not calibration-only deployment policies. Signed fidelity differences retain every gain and '
        'loss and are unaffected by the harm margin. Brackets are paired pointwise two-way 95\\% intervals.',
        'tab:r4-h-u-fidelity', 'lrrrl',
        r'Stream & $q$ (\%) & $F_H$ & $F_U$ & $H-U$: $\Delta F$ [95\% CI]', fidelity)
    output = REPO_ROOT.parent/'manuscript/generated/r4/r4_sensitivity_tables.tex'
    output.write_text(tex,encoding='utf-8')
    print(output)


if __name__=='__main__': main()
