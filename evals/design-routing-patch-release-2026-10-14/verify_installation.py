"""Compare installed promoted files with the immutable release tag."""
from pathlib import Path
import hashlib,json,subprocess
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
RAW=REPO/'.scratch/design-routing-patch-release-20261014'
TAG='paul-skills@0.4.1'
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def sha(data):return hashlib.sha256(data).hexdigest()
manifest_bytes=git('show',TAG+':.claude-plugin/plugin.json');manifest=json.loads(manifest_bytes)
assert manifest['version']=='0.4.1' and len(manifest['skills'])==44
codex=next(p for p in json.loads((RAW/'codex-plugin-list.json').read_text())['installed'] if p['pluginId']=='paul-skills@paul-skills')
claude=next(p for p in json.loads((RAW/'claude-plugin-list.json').read_text()) if p['id']=='paul-skills@paul-skills' and p['scope']=='user')
assert codex['version']==claude['version']=='0.4.1'
assert codex['enabled'] and claude['enabled']
paths=[p.decode() for p in git('ls-tree','-r','--name-only','-z',TAG,'--',*[p.removeprefix('./') for p in manifest['skills']]).split(b'\0') if p]
files={p:sha(git('show',TAG+':'+p)) for p in ['.claude-plugin/plugin.json']+paths}
hosts={}
for name,cache in [('codex',Path(json.loads((RAW/'codex-plugin-add.json').read_text())['installedPath'])),('claude',Path(claude['installPath']))]:
    for p,digest in files.items():assert sha((cache/p).read_bytes())==digest,(name,p)
    hosts[name]={'version':'0.4.1','enabled':True,'scope':'user','cache':str(cache).replace(str(Path.home()),'$HOME'),'manifest_equal':True,'all_promoted_files_equal':True,'skill_file_count':len(paths)}
result={'release_tag':TAG,'release_commit':git('rev-parse',TAG+'^{}').decode().strip(),'hosts':hosts,'promoted_skills':44,'files':files}
(HERE/'installation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'hosts':hosts,'promoted_skills':44}))
