#!/usr/bin/env python3
"""Check catalog/package/provenance relationships; not a behavior evaluation."""
import json
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
assert (root / 'AGENTS.md').is_file(), 'Maintainer instructions missing'
assert (root / '.claude/CLAUDE.md').read_text().strip() == '@../AGENTS.md', 'Claude context pointer drift'
registry = json.loads((root / 'skill-sources.json').read_text())
plugin = json.loads((root / '.claude-plugin/plugin.json').read_text())
paths = {p.parent.relative_to(root).as_posix() for p in (root / 'skills').rglob('SKILL.md')}
promoted = {p for p in paths if p.split('/')[1] in ('engineering', 'productivity', 'product-management', 'design')}
assert promoted == {p.removeprefix('./') for p in plugin['skills']}, 'Plugin differs from promoted set'
assert len(plugin['skills']) == len(promoted), 'Duplicate plugin entry'
rows = registry['skills']
assert len(rows) == len(paths) == len({r['id'] for r in rows}), 'Duplicate or absent inventory row'
assert {r['path'] for r in rows} == paths, 'Provenance coverage differs from skill tree'
sha = re.compile(r'^[0-9a-f]{40}$')
for row in rows:
    p = root / row['path']
    text = (p / 'SKILL.md').read_text()
    assert re.search(r'^name: ' + re.escape(row['id']) + r'$', text, re.M), row['id']
    assert 'metadata:\n' in text and '  provenance: ' in text, f'Missing source pointer: {p}'
    assert '—' not in text, f'Em dash: {p}'
    explicit = '\ndisable-model-invocation: true\n' in text
    policy = (p / 'agents/openai.yaml').read_text()
    assert explicit == ('allow_implicit_invocation: false' in policy), f'Invocation mismatch: {p}'
    assert row['kind'] in ('forked', 'adapted', 'composite', 'original')
    assert (row['kind'] == 'original') == (not row['origins']), f'Origin kind mismatch: {p}'
    for origin in row['origins']:
        assert origin['source'] in registry['sources']
        assert sha.fullmatch(origin['importedRevision']) and sha.fullmatch(origin['reviewedRevision'])
        assert re.fullmatch(r'sha256:[0-9a-f]{64}', origin['localDigest'])
        for name in ['path', 'reviewPath']:
            value = origin.get(name)
            if value is not None:
                assert value and not Path(value).is_absolute() and '..' not in Path(value).parts
    for influence in row.get('influences', []):
        assert influence['source'] in registry['sources'] and sha.fullmatch(influence['revision'])
    if row['path'] in promoted:
        assert (root / row['path'].replace('skills/', 'docs/', 1)).with_suffix('.md').exists(), f'Missing docs: {p}'
        assert row['path'] + '/SKILL.md' in (root / 'README.md').read_text(), f'Missing index: {p}'
    else:
        assert row['path'] + '/SKILL.md' not in (root / 'README.md').read_text(), f'Unpromoted skill in root index: {p}'
    assert './' + row['id'] + '/SKILL.md' in (p.parent / 'README.md').read_text(), f'Missing bucket entry: {p}'
print(f'{len(paths)} skill records; {len(promoted)} promoted paths; provenance and invocation consistent')
