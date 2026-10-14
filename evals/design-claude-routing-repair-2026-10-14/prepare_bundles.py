#!/usr/bin/env python3
"""Reconstruct both frozen promoted bundles without touching global installs."""
import hashlib
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
TRIAL = Path('/private/tmp/paul-design-claude-routing-repair-20261014')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare(manifest_path, destination, original=False):
    files = json.loads(manifest_path.read_text())['files']
    sources = {}
    for relative, expected in files.items():
        source = REPO / relative
        if relative == '.claude-plugin/plugin.json':
            source = HERE / 'diagnostics/plugin-0.4.0.json'
        if original and relative == 'skills/design/better-interface/SKILL.md':
            source = HERE / 'diagnostics/candidate-1-better-interface.txt'
        if sha(source) != expected:
            raise RuntimeError(f'Source drift: {relative}')
        sources[relative] = source
    if destination.exists():
        actual = {str(p.relative_to(destination)): sha(p) for p in destination.rglob('*') if p.is_file()}
        if actual != files:
            raise RuntimeError(f'Existing bundle differs: {destination.name}')
    else:
        for relative, source in sources.items():
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    return {'bundle': destination.name, 'files': len(files), 'equal': True}


if __name__ == '__main__':
    print(json.dumps([
        prepare(HERE / 'bundle-manifest.json', TRIAL / 'bundle', original=True),
        prepare(HERE / 'recovery/bundle-manifest.json', TRIAL / 'bundle-final')]))
