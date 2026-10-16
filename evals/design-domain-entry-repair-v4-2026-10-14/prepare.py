"""Install the domain-entry candidate in another private host clone."""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
BASE=Path('/private/tmp/paul-design-staged-routing-20261014');ROOT=Path('/private/tmp/paul-design-domain-entry-v4-20261014')
RAW=REPO/'.scratch/design-domain-entry-repair-v4-20261014'
def main():
    assert not ROOT.exists(),'Preserve this attempt'
    ROOT.mkdir();RAW.mkdir(parents=True,exist_ok=True)
    bundle=ROOT/'candidate/marketplace/plugin';hashes={}
    for relative in list(json.loads((REPO/'evals/design-staged-routing-repair-2026-10-14/baseline-manifest.json').read_text())['files'])+['skills/design/better-interface/audit-procedure.md']:
        source=REPO/relative;target=bundle/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes());hashes[relative]=hashlib.sha256(source.read_bytes()).hexdigest()
    (HERE/'candidate-manifest.json').write_text(json.dumps({'files':hashes},indent=2)+'\n')
    market=bundle.parent/'.claude-plugin';market.mkdir()
    (market/'marketplace.json').write_text(json.dumps({'name':'paul-staged-trial','owner':{'name':'Paul Kim'},'plugins':[{'name':'paul-skills','source':'./plugin','category':'design'}]})+'\n')
    home=ROOT/'candidate/codex-home';shutil.copytree(BASE/'host-snapshot',home,ignore=shutil.ignore_patterns('.git','__pycache__'));(home/'auth.json').symlink_to(Path.home()/'.codex/auth.json')
    p=home/'config.toml';s,count=re.subn(r'(\[plugins\."paul-skills@paul-skills"\]\s*\nenabled\s*=\s*)true',r'\1false',p.read_text());assert count==1;p.write_text(s)
    env=dict(os.environ,CODEX_HOME=str(home))
    for label,cmd in [('marketplace',['codex','plugin','marketplace','add',str(bundle.parent),'--json']),('install',['codex','plugin','add','paul-skills@paul-staged-trial','--json']),('list',['codex','plugin','list','--json'])]:
        p=subprocess.run(cmd,env=env,capture_output=True,text=True);(RAW/(label+'.json')).write_text(p.stdout)
        if p.returncode:raise RuntimeError(p.stderr)
    installed=Path(json.loads((RAW/'install.json').read_text())['installedPath'])
    assert all(hashlib.sha256((installed/p).read_bytes()).hexdigest()==d for p,d in hashes.items())
    (RAW/'environment.json').write_text(json.dumps({'candidate':{'plugin_root':str(installed),'codex_home':str(home),'bundle':str(bundle)}},indent=2)+'\n')
    print(json.dumps({'candidate':8,'verified_files':len(hashes)}))
if __name__=='__main__':main()
