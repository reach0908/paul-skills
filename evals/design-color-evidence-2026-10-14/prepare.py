"""Freeze native trial arms; copy private host context once, outside evidence."""
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, subprocess
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
ROOT=Path('/private/tmp/paul-design-color-evidence-20261014');RAW=REPO/'.scratch/design-color-evidence-20261014'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--arm',choices=['baseline','candidate'],required=True);arm=p.parse_args().arm
    ROOT.mkdir(mode=0o700,exist_ok=True);RAW.mkdir(parents=True,exist_ok=True)
    envfile=RAW/'environment.json';metadata=json.loads(envfile.read_text()) if envfile.exists() else {}
    assert arm not in metadata,'Preserve existing arm'
    manifest=json.loads((REPO/'.claude-plugin/plugin.json').read_text())
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only','paul-skills@0.4.2','--',*[s.removeprefix('./') for s in manifest['skills']]],cwd=REPO,text=True).splitlines()+['.claude-plugin/plugin.json']
    bundle=ROOT/arm/'marketplace/plugin';hashes={}
    for relative in paths:
        data=subprocess.check_output(['git','show','paul-skills@0.4.2:'+relative],cwd=REPO) if arm=='baseline' else (REPO/relative).read_bytes()
        target=bundle/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data);hashes[relative]=digest(target)
    (HERE/(arm+'-manifest.json')).write_text(json.dumps({'files':hashes},indent=2)+'\n')
    market=bundle.parent/'.claude-plugin';market.mkdir();(market/'marketplace.json').write_text(json.dumps({'name':'paul-color-trial','owner':{'name':'Paul Kim'},'plugins':[{'name':'paul-skills','source':'./plugin','category':'design'}]})+'\n')
    home=Path.home()/'.codex';seed=ROOT/'host-snapshot';names=['config.toml','AGENTS.md','skills','memories','plugins/cache','.tmp/marketplaces']
    if not seed.exists():
        assert arm=='baseline';seed.mkdir()
        for name in names:
            source=home/name;target=seed/name
            if source.is_file():target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
            elif source.is_dir():shutil.copytree(source,target,ignore=shutil.ignore_patterns('.git','__pycache__'))
        before={h:{r:digest(Path.home()/('.'+h)/'plugins/cache/paul-skills/paul-skills/0.4.2'/r) for r in paths} for h in ['codex','claude']}
        (HERE/'global-before.json').write_text(json.dumps(before,indent=2)+'\n')
    harness=ROOT/arm/'codex-home';shutil.copytree(seed,harness);(harness/'auth.json').symlink_to(home/'auth.json')
    config=harness/'config.toml';s,count=re.subn(r'(\[plugins\."paul-skills@paul-skills"\]\s*\nenabled\s*=\s*)true',r'\1false',config.read_text());assert count==1;config.write_text(s)
    env=dict(os.environ,CODEX_HOME=str(harness))
    for label,cmd in [('marketplace',['codex','plugin','marketplace','add',str(bundle.parent),'--json']),('install',['codex','plugin','add','paul-skills@paul-color-trial','--json']),('list',['codex','plugin','list','--json'])]:
        p=subprocess.run(cmd,env=env,capture_output=True,text=True);(RAW/(arm+'-'+label+'.json')).write_text(p.stdout)
        if p.returncode:raise RuntimeError(p.stderr)
    installed=Path(json.loads((RAW/(arm+'-install.json')).read_text())['installedPath']);assert all(digest(installed/r)==v for r,v in hashes.items())
    metadata[arm]={'plugin_root':str(installed),'codex_home':str(harness),'bundle':str(bundle)};envfile.write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps({'arm':arm,'files_verified':len(paths),'global_installs_untouched':True}))
if __name__=='__main__':main()
