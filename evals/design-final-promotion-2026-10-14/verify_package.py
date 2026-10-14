"""Verify promotion preserves the approved candidate and invocation contracts."""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
rows = json.loads((HERE / 'approved-files.json').read_text())
registry = json.loads((ROOT / 'skill-sources.json').read_text())
manifest = json.loads((ROOT / '.claude-plugin/plugin.json').read_text())
explicit = {'state-machine', 'break', 'explain-interface', 'variant'}
assert len(rows) == 8 and len(manifest['skills']) == 44
assert len(list((ROOT / 'skills/design').glob('*/SKILL.md'))) == 17
for row in rows:
    folder = ROOT / 'skills/design' / row['id']
    actual = {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in folder.rglob('*') if p.is_file()}
    assert actual == row['files'], row['id']
    assert not (ROOT / row['path']).exists(), row['id']
    current = next(r for r in registry['skills'] if r['id'] == row['id'])
    assert current['path'] == folder.relative_to(ROOT).as_posix()
    assert current['kind'] == row['kind']
    assert [{key: origin[key] for key in ('source', 'path', 'importedRevision', 'reviewedRevision')}
            for origin in current['origins']] == row['origins']
    assert ('disable-model-invocation: true' in (folder / 'SKILL.md').read_text()) == (row['id'] in explicit)
    assert ('allow_implicit_invocation: false' in (folder / 'agents/openai.yaml').read_text()) == (row['id'] in explicit)
    doc = (ROOT / 'docs/design' / (row['id'] + '.md')).read_text()
    headings = ['What it does', 'When to reach for it', 'Common questions', "It's working if", 'Where it fits']
    positions = [doc.index('## ' + h) for h in headings]
    assert positions == sorted(positions)
    assert not re.search(r'^# ', doc, re.M) and '\u2014' not in doc
    for link in re.findall(r'\]\(([^)]+)\)', doc):
        assert link.startswith('https://'), link
        prefix = 'https://github.com/reach0908/paul-skills/blob/main/'
        if link.startswith(prefix):
            assert (ROOT / link.removeprefix(prefix).split('#')[0]).is_file(), link
    assert row['id'] in (ROOT / 'skills/engineering/ask-matt/SKILL.md').read_text()
block = (ROOT / '.agents/install-block.md').read_text().split('\n', 1)[1].strip()
assert block in (ROOT / 'README.md').read_text()
result = {'status': 'pass', 'approvedSkills': 8, 'unchangedFiles': sum(len(r['files']) for r in rows),
          'designSkills': 17, 'promotedSkills': 44, 'newDocsPages': 8,
          'implicitNewSkills': 4, 'explicitNewSkills': 4, 'sourceOriginsUnchanged': True}
print(json.dumps(result))
