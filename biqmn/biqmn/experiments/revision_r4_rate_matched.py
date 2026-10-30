"""Reviewer-prompted R3 replay, equal-coverage audit, and convex controls."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import time
import traceback

import numpy as np
from scipy.optimize import brentq

from . import revision_r2_recovery as r2
from . import revision_r3_holdout_recovery as r3
from .common import REPO_ROOT
from .revision_audit import sha256
from .revision_identifiability import AXES

RUNS = ('R3_corrected_r0', 'R3_independent_r1', 'R3_independent_r2', 'R3_independent_r3')
PROTOCOL = REPO_ROOT.parent / 'manuscript' / 'revision_r4_protocol.md'
RATES = (0.25, 0.5, 0.75)
POLICIES = ('random', 'score', 'U', 'H', 'C3R')


def constrained_wls(means, weights, design):
    """Global least-squares minimizer over the Euclidean unit ball."""
    gram = design.T @ (weights[:, None] * design)
    rhs = design.T @ (weights * means)
    eigenvalues, vectors = np.linalg.eigh(gram)
    eigenvalues = np.maximum(eigenvalues, 0.)
    rotated = vectors.T @ rhs
    tolerance = max(float(eigenvalues.max()), 1.) * 1e-12
    unconstrained = np.divide(rotated, eigenvalues, out=np.zeros(3), where=eigenvalues > tolerance)
    lagrange = 0.
    if np.linalg.norm(unconstrained) > 1.:
        def norm_residual(value):
            return np.sum((rotated / (eigenvalues + value)) ** 2) - 1.
        upper = max(float(np.linalg.norm(rhs)), 1.)
        while norm_residual(upper) > 0:
            upper *= 2
        lagrange = brentq(norm_residual, 1e-14, upper, xtol=1e-12)
        unconstrained = rotated / (eigenvalues + lagrange)
    candidate = vectors @ unconstrained
    kkt = np.linalg.norm(gram @ candidate + lagrange * candidate - rhs) / max(np.linalg.norm(rhs), 1.)
    return candidate, float(kkt)


def reconstruct_job(job, dataset, thresholds):
    """Replay observations and assert agreement with every archived R3 record."""
    design = r2.physical_measurement_design(job['code'], AXES['tilted'], job['physical_noise'])
    bank = np.asarray(dataset['bank'])
    archived = {(row['pair_id'], row['sign']): row for row in job['records']}
    records = []
    checks = {'records': 0, 'max_replay_error': 0., 'max_kkt_residual': 0.,
              'max_norm': 0., 'max_loss_excess': 0.}
    for pair_id, pair in enumerate(dataset['test_pairs']):
        seed = [dataset['test_measurement_seed'], 0 if job['code'] == 'bitflip' else 1,
                job['copies'], int(100 * job['physical_noise']), int(100 * job['readout_flip']),
                job['measurement_seed'], pair_id]
        rng = np.random.default_rng(np.random.SeedSequence(seed))
        counts = rng.multinomial(job['copies'], np.full(8, 1 / 8))
        fitting = np.zeros(8, dtype=bool)
        fitting[rng.choice(8, size=4, replace=False)] = True
        target = np.asarray(pair[0])
        attenuation = 1 - 2 * job['readout_flip']
        successes = rng.binomial(counts, np.clip((1 + attenuation * (design @ target)) / 2, 0, 1))
        means = np.divide(2 * successes, counts, out=np.zeros(8), where=counts > 0) - 1
        means = np.clip(means / attenuation, -1, 1)
        fit_weights, val_weights = counts * fitting, counts * ~fitting
        a, loss_a = r2._fit(means, fit_weights, design)
        b, bank_index, loss_b = r2._nearest_template(means, fit_weights, design, bank)
        aopt, kkt_fit = constrained_wls(means, fit_weights, design)
        aall, kkt_all = constrained_wls(means, counts, design)
        loss_opt = r3._weighted_loss(means, fit_weights, design, aopt)
        excess = loss_opt - loss_a
        if excess > 1e-9 or max(np.linalg.norm(aopt), np.linalg.norm(aall)) > 1 + 1e-9:
            raise AssertionError('convex optimizer feasibility or optimality failure')
        if max(kkt_fit, kkt_all) > 1e-8:
            raise AssertionError('convex optimizer KKT failure')
        uncertainty = np.sqrt(np.trace(np.linalg.pinv(design.T @ (fit_weights[:, None] * design), rcond=1e-12)))
        residual = r3._weighted_loss(means, val_weights, design, b) - r3._weighted_loss(means, val_weights, design, a)
        # Antipodal partners have identical diagnostics and fidelities by symmetry.
        for sign in (1, -1):
            old = archived[(pair_id, sign)]
            if old['counts'] != counts.tolist() or old['fit_mask'] != fitting.tolist():
                raise AssertionError('R3 count/split replay mismatch')
            values = {'score': loss_b - loss_a, 'uncertainty': float(uncertainty),
                      'holdout_residual': residual, 'fidelity_a': float((1 + a @ target) / 2),
                      'fidelity_b': float((1 + b @ target) / 2)}
            error = max(abs(values[key] - old[key]) for key in values)
            if error > 1e-9:
                raise AssertionError(f'R3 numerical replay mismatch: {error}')
            s, u, h = old['score'], old['uncertainty'], old['holdout_residual']
            expected = {'c2_score': s <= thresholds['score_max'],
                        'u_uncertainty': s <= thresholds['score_max'] and u <= thresholds['uncertainty_max'],
                        'h_holdout_residual': s <= thresholds['score_max'] and h <= thresholds['holdout_residual_max'],
                        'c3r': s <= thresholds['score_max'] and u <= thresholds['uncertainty_max'] and h <= thresholds['holdout_residual_max']}
            if any(old['decision'][key] != value for key, value in expected.items()):
                raise AssertionError('R3 gate replay mismatch')
            records.append({**old, 'measurement_seed': job['measurement_seed'],
                            'fidelity_aopt_fit': float((1 + aopt @ target) / 2),
                            'fidelity_aopt_all': float((1 + aall @ target) / 2)})
            checks['records'] += 1
            checks['max_replay_error'] = max(checks['max_replay_error'], error)
        checks['max_kkt_residual'] = max(checks['max_kkt_residual'], kkt_fit, kkt_all)
        checks['max_norm'] = max(checks['max_norm'], float(np.linalg.norm(aopt)), float(np.linalg.norm(aall)))
        checks['max_loss_excess'] = max(checks['max_loss_excess'], excess)
    return records, checks


def resample_weights(draws, rng):
    seed_counts = np.stack([np.bincount(x, minlength=12) for x in rng.integers(12, size=(draws, 12))])
    pair_counts = np.stack([np.bincount(x, minlength=32) for x in rng.integers(32, size=(draws, 32))])
    weights = (seed_counts[:, :, None, None] * pair_counts[:, None, :, None] * np.ones((1, 1, 1, 2))).reshape(draws, -1)
    return np.vstack([np.ones(768), weights])


def ranked_probabilities(scores, proposed, fraction):
    """Uniform boundary-tie randomization at exactly the requested expected mass."""
    result = np.zeros(len(scores))
    selected = np.flatnonzero(proposed)
    values, inverse, sizes = np.unique(np.round(scores[selected], 12), return_inverse=True, return_counts=True)
    del values
    before = np.r_[0., np.cumsum(sizes)[:-1]]
    probabilities = np.clip((fraction * len(selected) - before) / sizes, 0., 1.)
    result[selected] = probabilities[inverse]
    return result


def ranked_totals(scores, proposed, fraction, weights, delta, harmful):
    selected = np.flatnonzero(proposed)
    order = selected[np.argsort(np.round(scores[selected], 12), kind='stable')]
    values = np.round(scores[order], 12)
    starts = np.r_[0, np.flatnonzero(np.diff(values)) + 1]
    group_mass = np.add.reduceat(weights[:, order], starts, axis=1)
    before = np.cumsum(group_mass, axis=1) - group_mass
    target = fraction * weights[:, selected].sum(axis=1)
    probabilities = np.divide(target[:, None] - before, group_mass,
                              out=np.zeros_like(group_mass), where=group_mass > 0)
    probabilities = np.clip(probabilities, 0., 1.)
    gain = (np.add.reduceat(weights[:, order] * delta[order], starts, axis=1) * probabilities).sum(axis=1)
    bad = (np.add.reduceat(weights[:, order] * harmful[order], starts, axis=1) * probabilities).sum(axis=1)
    return target, gain, bad


def interval(values):
    values = np.asarray(values)
    finite = values[1:][np.isfinite(values[1:])]
    return {'estimate': float(values[0]) if np.isfinite(values[0]) else None,
            'ci95': np.quantile(finite, [.025, .975]).tolist() if len(finite) else None}


def tails(a, b, probability):
    values = np.r_[a, b]
    mass = np.r_[1 - probability, probability]
    order = np.argsort(values)
    values, mass = values[order], mass[order]
    cumulative = np.cumsum(mass)
    threshold = .05 * mass.sum()
    q05 = values[np.searchsorted(cumulative, threshold)]
    included = np.clip(threshold - np.r_[0., cumulative[:-1]], 0., mass)
    return {'q05_per_record': float(q05), 'cvar05_per_record_exact_mass': float(included @ values / threshold)}


def summarize_cell(records, thresholds, weights):
    records.sort(key=lambda x: (x['measurement_seed'], x['pair_id'], -x['sign']))
    if len(records) != 768:
        raise AssertionError('incomplete R3 cell')
    a = np.array([x['fidelity_a'] for x in records])
    b = np.array([x['fidelity_b'] for x in records])
    opt = np.array([x['fidelity_aopt_fit'] for x in records])
    all_opt = np.array([x['fidelity_aopt_all'] for x in records])
    delta, harmful = b - a, (b < a - 1e-12).astype(float)
    proposed = np.array([x['decision']['c2_score'] for x in records])
    base = weights @ a / 768
    opt_mean, all_mean = weights @ opt / 768, weights @ all_opt / 768
    policy_arrays = {}
    policies = {}

    def store(name, mass, gain, bad, probability):
        mean = base + gain / 768
        conditional = np.divide(bad, mass, out=np.full_like(bad, np.nan), where=mass > 0)
        arr = {'mean_fidelity': mean, 'conditional_harm': conditional,
               'harmful_rate': bad / 768, 'switch_rate': mass / 768,
               'gain_vs_a': mean - base, 'gain_vs_aopt_fit': mean - opt_mean,
               'gain_vs_aopt_all': mean - all_mean}
        policy_arrays[name] = arr
        policies[name] = {key: interval(value) for key, value in arr.items()}
        policies[name].update(tails(a, b, probability))

    originals = {name: np.array([x['decision'][key] for x in records], dtype=float)
                 for name, key in [('random', 'c2_score'), ('U', 'u_uncertainty'),
                                   ('H', 'h_holdout_residual'), ('C3R', 'c3r')]}
    common = weights @ originals['C3R']
    for name, switched in originals.items():
        mass = weights @ switched
        factor = np.divide(common, mass, out=np.zeros_like(common), where=mass > 0)
        probability = switched * factor[0]
        store('fixed_' + name, common, (weights @ (switched * delta)) * factor,
              (weights @ (switched * harmful)) * factor, probability)

    scores = {'score': np.array([x['score'] for x in records]),
              'U': np.array([x['uncertainty'] for x in records]) / thresholds['uncertainty_max'],
              'H': np.array([x['holdout_residual'] for x in records]) / thresholds['holdout_residual_max']}
    scores['C3R'] = np.maximum(scores['U'], scores['H'])
    for fraction in RATES:
        tag = f'q{int(100 * fraction):02d}'
        store(tag + '_random', fraction * (weights @ proposed),
              fraction * (weights @ (proposed * delta)), fraction * (weights @ (proposed * harmful)),
              fraction * proposed)
        for name, score in scores.items():
            mass, gain, bad = ranked_totals(score, proposed, fraction, weights, delta, harmful)
            store(tag + '_' + name, mass, gain, bad, ranked_probabilities(score, proposed, fraction))

    for name in policies:
        prefix, policy = name.split('_', 1)
        comparisons = {}
        for reference in ('random', 'U'):
            ref_name = prefix + '_' + reference
            comparisons[reference] = {
                metric: interval(policy_arrays[name][metric] - policy_arrays[ref_name][metric])
                for metric in ('mean_fidelity', 'conditional_harm', 'switch_rate')
            }
        policies[name]['differences'] = comparisons
    controls = {name: interval(value) for name, value in (
        ('a', base), ('aopt_fit', opt_mean), ('aopt_all', all_mean),
        ('aopt_fit_minus_a', opt_mean - base), ('aopt_all_minus_a', all_mean - base))}
    return {'proposal_rate': float(proposed.mean()), 'common_rate': float(common[0] / 768),
            'policies': policies, 'continuous': controls}, policy_arrays, (base, opt_mean, all_mean)


def run_stream(task):
    stream, root, output, draws = task
    run = Path(root) / RUNS[stream]
    output = Path(output)
    dataset = json.loads((run / 'dataset.json').read_text())
    thresholds = json.loads((run / 'thresholds.json').read_text())
    jobs = json.loads((run / 'results.json').read_text())
    # R3 thresholds must be strictly positive for the combined scaling family.
    if min(thresholds['uncertainty_max'], thresholds['holdout_residual_max']) <= 0:
        raise AssertionError('nonpositive threshold normalization')
    grouped = {}
    audits = []
    for job in jobs:
        key = tuple(job[k] for k in ('code', 'copies', 'physical_noise', 'readout_flip'))
        recs, checks = reconstruct_job(job, dataset, thresholds)
        grouped.setdefault(key, []).extend(recs)
        audits.append(checks)
    rng = np.random.default_rng(2026102900 + stream)
    weights = resample_weights(draws, rng)
    summaries, all_arrays, all_controls = [], [], []
    for key, records in sorted(grouped.items()):
        summary, arrays, controls = summarize_cell(records, thresholds, weights)
        summaries.append({'stream': stream, 'code': key[0], 'copies': key[1],
                          'physical_noise': key[2], 'readout_flip': key[3], **summary})
        all_arrays.append(arrays)
        all_controls.append(controls)
    aggregate = {'stream': stream, 'informative_fixed_cells': sum(x['common_rate'] > 0 for x in summaries),
                 'policies': {}, 'continuous': {}}
    for name in all_arrays[0]:
        # Macro-averages of conditional harm use only nonzero-coverage cells.
        arrays = {metric: np.nanmean(np.stack([arr[name][metric] for arr in all_arrays]), axis=0)
                  for metric in all_arrays[0][name]}
        aggregate['policies'][name] = {metric: interval(value) for metric, value in arrays.items()}
        prefix, policy = name.split('_', 1)
        aggregate['policies'][name]['differences'] = {}
        for ref in ('random', 'U'):
            aggregate['policies'][name]['differences'][ref] = {
                metric: interval(np.nanmean(np.stack([
                    arr[name][metric] - arr[prefix + '_' + ref][metric] for arr in all_arrays
                ]), axis=0)) for metric in ('mean_fidelity', 'conditional_harm', 'switch_rate')}
    for idx, name in enumerate(('a', 'aopt_fit', 'aopt_all')):
        aggregate['continuous'][name] = interval(np.mean([x[idx] for x in all_controls], axis=0))
    audit = {key: sum(x[key] for x in audits) if key == 'records' else max(x[key] for x in audits)
             for key in audits[0]}
    payload = {'stream': stream, 'cells': summaries, 'aggregate': aggregate, 'audit': audit,
               'input_hashes': {name: sha256(run / name) for name in ('dataset.json', 'thresholds.json', 'results.json')}}
    (output / f'stream_{stream}.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')
    print(f'stream {stream} complete: {audit}', flush=True)
    return payload


def make_report(streams):
    lines = ['# R4 equal-coverage and continuous-estimator audit', '',
             'Reviewer-prompted secondary analysis of the existing R3 streams. No new count realizations.', '',
             'Intervals are pointwise paired two-way cluster bootstrap intervals, conditional on the R3 banks and thresholds.', '',
             '## Stream aggregate at 50% of C2 proposals', '',
             '| Stream | Policy | Harm among accepted | Mean fidelity | Gain vs A*_all [95% CI] |',
             '|---|---|---:|---:|---|']
    for stream in streams:
        agg = stream['aggregate']
        for policy in POLICIES:
            p = agg['policies']['q50_' + policy]
            gain = p['gain_vs_aopt_all']
            lines.append(f"| {agg['stream']} | {policy} | {100*p['conditional_harm']['estimate']:.3f}% | "
                         f"{p['mean_fidelity']['estimate']:.6f} | {gain['estimate']:+.6f} "
                         f"[{gain['ci95'][0]:+.6f}, {gain['ci95'][1]:+.6f}] |")
    lines += ['', '## Original fixed gates at common expected coverage', '',
              '| Stream | Informative cells | H minus random harm [95% CI], pp | C3R minus U harm [95% CI], pp |',
              '|---|---:|---|---|']
    for stream in streams:
        agg = stream['aggregate']
        def fmt(policy, ref):
            value = agg['policies'][policy]['differences'][ref]['conditional_harm']
            return f"{100*value['estimate']:+.3f} [{100*value['ci95'][0]:+.3f}, {100*value['ci95'][1]:+.3f}]"
        lines.append(f"| {agg['stream']} | {agg['informative_fixed_cells']}/24 | {fmt('fixed_H','random')} | {fmt('fixed_C3R','U')} |")
    lines += ['', 'Full cell results, all three retention levels, controls, tails, intervals, and replay checks are in summary.json.',
              'The ranking curves use observed batch diagnostics without target outcomes. They are not calibration-only deployment rules.',
              'Tail summaries use per-record mixtures; R3 tail metrics use a different seed-averaged unit.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--input-root', type=Path, default=REPO_ROOT / 'results' / 'revision_experiments')
    parser.add_argument('--workers', type=int, default=4, choices=range(1, 7))
    parser.add_argument('--draws', type=int, default=5000)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output exists; R4 never overwrites an analysis')
    args.output.mkdir(parents=True)
    started = time.perf_counter()
    manifest = {'created_utc': datetime.now(timezone.utc).isoformat(), 'draws': args.draws,
                'workers': args.workers, 'protocol_sha256': sha256(PROTOCOL),
                'source_sha256': sha256(Path(__file__)), 'numpy': np.__version__,
                'analysis_type': 'reviewer_prompted_secondary_analysis', 'new_count_realizations': 0}
    (args.output / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    try:
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            streams = list(executor.map(run_stream, [(i, args.input_root, args.output, args.draws) for i in range(4)]))
        (args.output / 'summary.json').write_text(json.dumps(streams, indent=2), encoding='utf-8')
        (args.output / 'REPORT.md').write_text(make_report(streams), encoding='utf-8')
        (args.output / 'DONE.json').write_text(json.dumps({'state': 'success', 'seconds': time.perf_counter()-started}), encoding='utf-8')
    except Exception:
        (args.output / 'FAILED.json').write_text(json.dumps({'state': 'failed', 'traceback': traceback.format_exc()}), encoding='utf-8')
        raise


if __name__ == '__main__':
    main()
