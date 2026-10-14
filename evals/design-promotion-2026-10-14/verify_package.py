"""Check the promoted package against the exact user-approved skill files."""
from pathlib import Path
import hashlib
import json
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
files=json.loads((HERE/'approved-files.json').read_text())
names={row['skill'] for row in files}
adjustments=json.loads((HERE/'reviewed-adjustments.json').read_text())
assert len(adjustments)==1
assert {(r['skill'],r['path']) for r in adjustments}=={('design-browser','references/aside.md')}
by_path={(r['skill'],r['path']):r for r in adjustments}
manifest=json.loads((ROOT/'.claude-plugin/plugin.json').read_text())
registry=json.loads((ROOT/'skill-sources.json').read_text())
assert len(names)==9 and len(files)==61
assert len(manifest['skills'])==36
for row in files:
    current=ROOT/'skills/design'/row['skill']/row['path']
    adjustment=by_path.get((row['skill'],row['path']))
    if adjustment:
        assert adjustment['beforeSha256']==row['sha256']
    expected=adjustment['afterSha256'] if adjustment else row['sha256']
    assert current.is_file() and hashlib.sha256(current.read_bytes()).hexdigest()==expected,current
for name in names:
    assert not (ROOT/'skills/in-progress'/name).exists()
    assert './skills/design/'+name in manifest['skills']
    record=next(r for r in registry['skills'] if r['id']==name)
    assert record['path']=='skills/design/'+name
    doc=(ROOT/'docs/design'/f'{name}.md').read_text()
    assert not re.search(r'^# ',doc,re.M)
    sections=['What it does','When to reach for it','Common questions',"It's working if",'Where it fits']
    positions=[doc.index('## '+section) for section in sections]
    assert positions==sorted(positions)
    assert all(link.startswith('https://') for link in re.findall(r'\]\(([^)]+)\)',doc))
    assert '\u2014' not in doc
    assert name in (ROOT/'skills/engineering/ask-matt/SKILL.md').read_text()
block=(ROOT/'.agents/install-block.md').read_text().split('\n',1)[1].strip()
assert block in (ROOT/'README.md').read_text()
print(json.dumps({'approvedFilesUnchanged':60,'reviewedAdjustments':1,'designSkills':9,'promotedSkills':36,'docsPages':9,'status':'pass'}))
