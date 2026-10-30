"""Fixed-policy R4 sensitivity to absolute harm margins; preserve original R4."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import traceback

import numpy as np

from . import revision_r4_rate_matched as r4
from .common import REPO_ROOT
from .revision_audit import sha256

MARGINS = (1e-12, .001, .005, .01)
MARGIN_KEYS = ('1e-12', '0.001', '0.005', '0.01')
PROTOCOL = REPO_ROOT.parent / 'manuscript/revision_r4_sensitivity_protocol.md'


def harm_labels(a, b):
    return (b[:, None] < a[:, None] - np.asarray(MARGINS)[None, :]).astype(float)


def ranked_outcomes(score, proposed, fraction, weights, outcomes):
    """Exactly matched expected mass with outcome-independent boundary ties."""
    selected = np.flatnonzero(proposed)
    order = selected[np.argsort(np.round(score[selected], 12), kind='stable')]
    values, inverse = np.unique(np.round(score[order], 12), return_inverse=True)
    del values
    starts = np.r_[0, np.flatnonzero(np.diff(inverse)) + 1]
    group_mass = np.add.reduceat(weights[:, order], starts, axis=1)
    before = np.cumsum(group_mass, axis=1) - group_mass
    target = fraction * weights[:, selected].sum(axis=1)
    probability = np.divide(target[:, None] - before, group_mass,
                            out=np.zeros_like(group_mass), where=group_mass > 0)
    weighted_selection = weights[:, order] * np.clip(probability, 0, 1)[:, inverse]
    totals = weighted_selection @ outcomes[order]
    np.testing.assert_allclose(weighted_selection.sum(axis=1), target, atol=1e-10, rtol=0)
    return target, totals


def encode(arrays):
    result = {}
    for name, metrics in arrays.items():
        prefix = name.split('_', 1)[0]
        record = {key: r4.interval(metrics[key]) for key in ('mean_fidelity', 'switch_rate')}
        record['margins'] = {}
        for idx, key in enumerate(MARGIN_KEYS):
            record['margins'][key] = {metric: r4.interval(metrics[metric][:, idx])
                                       for metric in ('conditional_harm', 'harmful_rate')}
        record['differences'] = {}
        for reference in ('random', 'U'):
            ref = arrays[prefix+'_'+reference]
            comparison = {'mean_fidelity': r4.interval(metrics['mean_fidelity']-ref['mean_fidelity']),
                          'switch_rate': r4.interval(metrics['switch_rate']-ref['switch_rate']),
                          'margins': {}}
            for idx, key in enumerate(MARGIN_KEYS):
                comparison['margins'][key] = {
                    metric: r4.interval(metrics[metric][:, idx]-ref[metric][:, idx])
                    for metric in ('conditional_harm', 'harmful_rate')}
            record['differences'][reference] = comparison
        result[name] = record
    return result


def cell_arrays(records, thresholds, weights):
    records.sort(key=lambda row: (row['measurement_seed'], row['pair_id'], -row['sign']))
    assert len(records) == 768
    a = np.array([row['fidelity_a'] for row in records])
    b = np.array([row['fidelity_b'] for row in records])
    outcomes = np.column_stack((b-a, harm_labels(a,b)))
    base = weights @ a / 768
    proposed = np.array([row['decision']['c2_score'] for row in records])
    arrays = {}

    def add(name, mass, totals):
        arrays[name] = {'mean_fidelity': base+totals[:, 0]/768,
                        'switch_rate': mass/768,
                        'harmful_rate': totals[:, 1:]/768,
                        'conditional_harm': np.divide(totals[:, 1:],mass[:, None],
                            out=np.full_like(totals[:, 1:],np.nan),where=mass[:, None]>0)}

    original = {name: np.array([row['decision'][key] for row in records],dtype=float)
                for name,key in [('random','c2_score'),('U','u_uncertainty'),
                                 ('H','h_holdout_residual'),('C3R','c3r')]}
    common = weights @ original['C3R']
    for name, switched in original.items():
        mass = weights @ switched
        factor = np.divide(common,mass,out=np.zeros_like(common),where=mass>0)
        add('fixed_'+name,common,((weights*switched) @ outcomes)*factor[:, None])
    scores = {'score': np.array([row['score'] for row in records]),
              'U': np.array([row['uncertainty'] for row in records])/thresholds['uncertainty_max'],
              'H': np.array([row['holdout_residual'] for row in records])/thresholds['holdout_residual_max']}
    scores['C3R'] = np.maximum(scores['U'],scores['H'])
    for fraction in r4.RATES:
        prefix = f'q{int(fraction*100)}_'
        add(prefix+'random',fraction*(weights@proposed),fraction*((weights*proposed)@outcomes))
        for name,score in scores.items():
            mass,totals = ranked_outcomes(score,proposed,fraction,weights,outcomes)
            add(prefix+name,mass,totals)
    return arrays


def check_original(policies, original):
    errors = []
    for name, p in policies.items():
        pairs = [(p['mean_fidelity'],original[name]['mean_fidelity']),
                 (p['switch_rate'],original[name]['switch_rate']),
                 (p['margins']['1e-12']['conditional_harm'],original[name]['conditional_harm']),
                 (p['margins']['1e-12']['harmful_rate'],original[name]['harmful_rate'])]
        for reference in ('random','U'):
            pairs.extend((p['differences'][reference][metric],original[name]['differences'][reference][metric])
                         for metric in ('mean_fidelity','switch_rate'))
        for new,old in pairs:
            if new['estimate'] is None or old['estimate'] is None:
                assert new == old
            else:
                errors.extend([abs(new['estimate']-old['estimate']),
                               *np.abs(np.asarray(new['ci95'])-old['ci95'])])
    maximum = max(errors,default=0.)
    assert maximum < 1e-9, maximum
    return maximum


def run_stream(task):
    stream, output, draws = task
    root = REPO_ROOT/'results/revision_experiments'
    old = json.loads((root/'R4_rate_matched'/f'stream_{stream}.json').read_text())
    raw_dir = root/r4.RUNS[stream]
    thresholds = json.loads((raw_dir/'thresholds.json').read_text())
    for name,expected in old['input_hashes'].items():
        assert sha256(raw_dir/name) == expected, name
    grouped = {}
    for job in json.loads((raw_dir/'results.json').read_text()):
        key = tuple(job[name] for name in ('code','copies','physical_noise','readout_flip'))
        grouped.setdefault(key,[]).extend({**row,'measurement_seed':job['measurement_seed']} for row in job['records'])
    reference = {tuple(cell[name] for name in ('code','copies','physical_noise','readout_flip')):cell
                 for cell in old['cells']}
    weights = r4.resample_weights(draws,np.random.default_rng(2026102900+stream))
    cells, all_arrays = [],[]
    maximum = 0.
    for key,records in sorted(grouped.items()):
        arrays = cell_arrays(records,thresholds,weights)
        policies = encode(arrays)
        maximum = max(maximum,check_original(policies,reference[key]['policies']))
        cells.append({'code':key[0],'copies':key[1],'physical_noise':key[2],
                      'readout_flip':key[3],'policies':policies})
        all_arrays.append(arrays)
    aggregate_arrays = {
        name: {metric: np.nanmean(np.stack([cell[name][metric] for cell in all_arrays]),axis=0)
               for metric in all_arrays[0][name]} for name in all_arrays[0]}
    aggregate = encode(aggregate_arrays)
    maximum = max(maximum,check_original(aggregate,old['aggregate']['policies']))
    result = {'stream':stream,'margins':MARGINS,'cells':cells,'aggregate':{'policies':aggregate},
              'input_hashes':old['input_hashes'],'records':sum(len(rows) for rows in grouped.values()),
              'max_original_r4_reproduction_error':maximum}
    (Path(output)/f'stream_{stream}.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(f'stream {stream} complete; baseline reproduction error {maximum:.3g}',flush=True)
    return result


def report(data):
    lines = ['# R4 harm-margin sensitivity', '',
             'Same records and fixed selection rules; all intervals pointwise, paired, and conditional.',
             'Margins classify harm only; full signed fidelity differences remain unchanged.', '',
             '| Stream | Harm margin | H minus U conditional harm at 50%, pp [95% CI] |',
             '|---|---:|---|']
    def fmt(value,scale,digits):
        return f"{scale*value['estimate']:+.{digits}f} [{scale*value['ci95'][0]:+.{digits}f}, {scale*value['ci95'][1]:+.{digits}f}]"
    for stream in data:
        p = stream['aggregate']['policies']['q50_H']['differences']['U']
        for key in MARGIN_KEYS:
            lines.append(f"| {stream['stream']} | {key} | {fmt(p['margins'][key]['conditional_harm'],100,3)} |")
    lines += ['', '| Stream | Retention | H minus U mean fidelity [95% CI] |','|---|---:|---|']
    for stream in data:
        for q in (25,50,75):
            value = stream['aggregate']['policies'][f'q{q}_H']['differences']['U']['mean_fidelity']
            lines.append(f"| {stream['stream']} | {q}% | {fmt(value,1,6)} |")
    return '\n'.join(lines)+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--workers',type=int,default=4,choices=range(1,7))
    args = parser.parse_args()
    if args.output.exists(): parser.error('output exists; preserve previous results')
    args.output.mkdir(parents=True)
    started = time.perf_counter()
    old_manifest = json.loads((REPO_ROOT/'results/revision_experiments/R4_rate_matched/manifest.json').read_text())
    assert old_manifest['source_sha256'] == sha256(Path(r4.__file__))
    assert old_manifest['protocol_sha256'] == sha256(r4.PROTOCOL)
    manifest = {'created_utc':datetime.now(timezone.utc).isoformat(),'draws':5000,'workers':args.workers,
                'margins':MARGINS,'source_sha256':sha256(Path(__file__)),
                'protocol_sha256':sha256(PROTOCOL),'original_r4_manifest':old_manifest,
                'analysis_type':'secondary_harm_margin_sensitivity','new_count_realizations':0}
    (args.output/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    try:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            data = list(executor.map(run_stream,[(i,args.output,5000) for i in range(4)]))
        (args.output/'summary.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
        (args.output/'REPORT.md').write_text(report(data),encoding='utf-8')
        (args.output/'DONE.json').write_text(json.dumps({'state':'success','seconds':time.perf_counter()-started}),encoding='utf-8')
    except Exception:
        (args.output/'FAILED.json').write_text(json.dumps({'traceback':traceback.format_exc()}),encoding='utf-8')
        raise


if __name__=='__main__': main()
