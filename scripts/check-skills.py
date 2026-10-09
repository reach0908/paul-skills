#!/usr/bin/env python3
"""Check catalog/package/provenance relationships; not a behavior evaluation."""
import json
import hashlib
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
content_digest = re.compile(r'^sha256:[0-9a-f]{64}$')
local_sources = registry.get('localSources', {})
for source_id, source in local_sources.items():
    assert source_id not in registry['sources'], f'Ambiguous source: {source_id}'
    assert source['locator'].startswith('local-skill:') and source['permission'], source_id
    assert 'license' in source and source['files'], source_id
    for filename, value in source['files'].items():
        assert filename and not Path(filename).is_absolute() and '..' not in Path(filename).parts
        assert content_digest.fullmatch(value), source_id
    payload = json.dumps(sorted(source['files'].items()), separators=(',', ':'), ensure_ascii=True)
    assert source['digest'] == 'sha256:' + hashlib.sha256(payload.encode()).hexdigest(), source_id
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
    assert (row['kind'] == 'original') == (not row['origins'] and not row.get('localOrigins')), f'Origin kind mismatch: {p}'
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
    for origin in row.get('localOrigins', []):
        assert origin['source'] in local_sources, row['id']
        assert content_digest.fullmatch(origin['importedDigest']), row['id']
        assert origin['reviewedDigest'] == local_sources[origin['source']]['digest'], row['id']
        assert row['kind'] in ('adapted', 'composite'), row['id']
    if row['path'] in promoted:
        assert (root / row['path'].replace('skills/', 'docs/', 1)).with_suffix('.md').exists(), f'Missing docs: {p}'
        assert row['path'] + '/SKILL.md' in (root / 'README.md').read_text(), f'Missing index: {p}'
    else:
        assert row['path'] + '/SKILL.md' not in (root / 'README.md').read_text(), f'Unpromoted skill in root index: {p}'
    assert './' + row['id'] + '/SKILL.md' in (p.parent / 'README.md').read_text(), f'Missing bucket entry: {p}'
print(f'{len(paths)} skill records; {len(promoted)} promoted paths; provenance and invocation consistent')
