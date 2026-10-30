"""Render transparent R4 summaries; no choices are tuned to cell outcomes."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from .common import REPO_ROOT


def value(item, scale=1, digits=3):
    return f"{scale*item['estimate']:+.{digits}f}"


def ci(item, scale=1, digits=3):
    lo, hi = item['ci95']
    return f"${scale*item['estimate']:+.{digits}f}\\ [{scale*lo:+.{digits}f},{scale*hi:+.{digits}f}]$"


def table(caption, label, columns, header, rows):
    return '\n'.join([
        r'\begin{table}[ht]', r'\centering', r'\scriptsize', r'\setlength{\tabcolsep}{3pt}',
        '\\caption{' + caption + '}', '\\label{' + label + '}',
        '\\begin{tabular}{@{}' + columns + '@{}}', r'\toprule', header + r' \\',
        r'\midrule', *[row + r' \\' for row in rows], r'\bottomrule',
        r'\end{tabular}', r'\end{table}', ''])


def main():
    root = REPO_ROOT.parent
    output = root / 'manuscript' / 'generated' / 'r4'
    output.mkdir(parents=True, exist_ok=True)
    data = json.loads((REPO_ROOT / 'results/revision_experiments/R4_rate_matched/summary.json').read_text())
    fixed, ranking, fidelity = [], [], []
    numbers = []
    for stream in data:
        a = stream['aggregate']
        p = a['policies']
        fixed.append(' & '.join([
            f"r{a['stream']}", f"{a['informative_fixed_cells']}/24",
            ci(p['fixed_H']['differences']['random']['conditional_harm'],100,2),
            ci(p['fixed_C3R']['differences']['U']['conditional_harm'],100,2),
            ci(p['fixed_C3R']['differences']['U']['mean_fidelity'],1,5)]))
        controls = a['continuous']
        fidelity.append(' & '.join([
            f"r{a['stream']}", f"{controls['a']['estimate']:.6f}",
            f"{controls['aopt_fit']['estimate']:.6f}", f"{controls['aopt_all']['estimate']:.6f}",
            ci(p['q50_H']['gain_vs_aopt_fit'],1,5), ci(p['q50_H']['gain_vs_aopt_all'],1,5)]))
        for q in (25,50,75):
            h, u, c, random = [p[f'q{q}_{k}'] for k in ('H','U','C3R','random')]
            ranking.append(' & '.join([
                f"r{a['stream']}", str(q), f"{100*random['conditional_harm']['estimate']:.2f}",
                f"{100*u['conditional_harm']['estimate']:.2f}", f"{100*h['conditional_harm']['estimate']:.2f}",
                f"{100*c['conditional_harm']['estimate']:.2f}",
                ci(h['differences']['U']['conditional_harm'],100,2)]))
        numbers.append({'stream':a['stream'], 'fixed_H_random':p['fixed_H']['differences']['random']['conditional_harm'],
                        'fixed_C3R_U':p['fixed_C3R']['differences']['U']['conditional_harm'],
                        'q50_H_U':p['q50_H']['differences']['U']['conditional_harm'],
                        'q50_H_Aall':p['q50_H']['gain_vs_aopt_all']})
    tex = table(
        'Original fixed gates after analytic random thinning to the common expected switching rate of '
        '$C_3^{\\mathrm R}$. Conditional-harm differences are percentage points and are equally averaged '
        'over the 12 positive-coverage cells (all 1,024-copy cells). Mean-fidelity differences average all '
        '24 cells, including zero interventions at 256 copies. Brackets are pointwise paired two-way 95\\% intervals.',
        'tab:r4-fixed', 'lrlll',
        r'Stream & Active & $H-R$: harm & $C_3^{\mathrm R}-U$: harm & $C_3^{\mathrm R}-U$: $\Delta F$', fixed)
    tex += table(
        'Equal-retention batch rankings. Retention $q$ is the percentage of original $C_2$ proposals accepted '
        'in expectation. R denotes uniform random retention. Harm is the percentage of accepted switches '
        'with $F_B<F_A-10^{-12}$, equally averaged across all 24 cells per stream. All rankings have the '
        'same expected switching rate in each cell and bootstrap sample; cutoffs use observed diagnostics '
        'without target outcomes. The last column is a paired pointwise 95\\% interval in percentage points.',
        'tab:r4-ranking', 'lrrrrrl',
        r'Stream & $q$ & R harm & U harm & H harm & Combined harm & $H-U$: harm', ranking)
    tex += table(
        'Continuous controls and the 50\\%-retention H ranking, averaged equally across the 24 cells. '
        '$A$ is the original radial projection; $A^*_{\\rm fit}$ globally minimizes the fitting-label '
        'weighted loss over the Bloch ball; $A^*_{\\rm all}$ uses the entire prepared-copy budget. '
        'The two right columns are paired H-minus-control mean-fidelity differences with pointwise 95\\% intervals. '
        'The optimized-loss estimators are not oracle fidelity optimizers.',
        'tab:r4-continuous', 'lrrrll',
        r'Stream & $F_A$ & $F_{A^*_{\rm fit}}$ & $F_{A^*_{\rm all}}$ & H minus $A^*_{\rm fit}$ & H minus $A^*_{\rm all}$', fidelity)
    (output / 'r4_supplementary_tables.tex').write_text(tex, encoding='utf-8')
    (output / 'r4_key_numbers.json').write_text(json.dumps(numbers,indent=2),encoding='utf-8')
    colors = {'random':'#7b7b7b','score':'#c57916','U':'#2876ac','H':'#13764c','C3R':'#9b4e97'}
    labels = {'random':'Random','score':'Fitting score','U':'Uncertainty','H':'Held-out residual','C3R':'Combined'}
    with plt.rc_context({'font.size':9, 'axes.spines.top':False, 'axes.spines.right':False}):
        fig, axes = plt.subplots(2,2,figsize=(7.15,5.2),sharex=True,sharey=True)
        for stream, ax in zip(data, axes.flat):
            a=stream['aggregate']
            for name in ('random','score','U','C3R','H'):
                ys=[100*a['policies'][f'q{q}_{name}']['conditional_harm']['estimate'] for q in (25,50,75)]
                ax.plot([25,50,75],ys,marker='o',ms=3.5,lw=1.6,color=colors[name],label=labels[name])
            ax.set_title(f"Stream {a['stream']}",loc='left',fontsize=10)
            ax.set_xticks([25,50,75]);ax.set_ylim(10,75);ax.grid(axis='y',alpha=.18)
        for ax in axes[-1,:]:ax.set_xlabel('C2 proposals retained (%)')
        fig.supylabel('Harm among accepted switches (%)', fontsize=9, x=.012)
        handles, legend_labels=axes[0,0].get_legend_handles_labels()
        fig.legend(handles,legend_labels,loc='upper center',ncol=3,frameon=False,bbox_to_anchor=(.53,1.02))
        fig.tight_layout(rect=(.025,0,1,.91))
        fig.savefig(output/'r4_rate_matched.png',dpi=240,facecolor='white')
        plt.close(fig)
    print(output)


if __name__=='__main__':
    main()
