"""Verify the public release inventory and frozen analysis/input provenance."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT/'biqmn/results/revision_experiments'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    inventory = json.loads((ROOT/'RELEASE_MANIFEST.json').read_text(encoding='utf-8'))
    for relative, expected in inventory['files'].items():
        path = ROOT/relative
        assert path.is_file(), relative
        assert digest(path) == expected['sha256'], f'Byte mismatch: {relative}'
    sources = (
        ('R4_rate_matched','revision_r4_rate_matched.py','revision_r4_protocol.md'),
        ('R4_harm_sensitivity','revision_r4_harm_sensitivity.py','revision_r4_sensitivity_protocol.md'),
    )
    for folder,source,protocol in sources:
        run = RESULTS/folder
        manifest = json.loads((run/'manifest.json').read_text())
        assert manifest['source_sha256']==digest(ROOT/'biqmn/biqmn/experiments'/source)
        assert manifest['protocol_sha256']==digest(ROOT/'manuscript'/protocol)
        assert json.loads((run/'DONE.json').read_text())['state']=='success'
    for stream,run in enumerate(('R3_corrected_r0','R3_independent_r1','R3_independent_r2','R3_independent_r3')):
        for analysis in ('R4_rate_matched','R4_harm_sensitivity'):
            record=json.loads((RESULTS/analysis/f'stream_{stream}.json').read_text())
            for name, expected in record['input_hashes'].items():
                assert digest(RESULTS/run/name)==expected, f'{analysis} input mismatch: {run}/{name}'
    frozen=ROOT/'manuscript/protocol_archive/revision_r3_protocol_frozen_9354f1f.md'
    expected='90c2941f4f1a7a64a7c8a40fc2c50141d6132aee1b4767d5bb32fefe9f6a1644'
    assert digest(frozen)==expected
    for run in ('R3_corrected_r0','R3_independent_r1','R3_independent_r2','R3_independent_r3'):
        manifest=json.loads((RESULTS/run/'manifest.json').read_text())
        assert manifest['protocol_sha256']==expected
        assert manifest['source_sha256']==digest(ROOT/'biqmn/biqmn/experiments/revision_r3_holdout_recovery.py')
    print(f"Verified {len(inventory['files'])} release files, both R4 source/protocol hashes, and all four R3 input streams.")


if __name__=='__main__': main()
