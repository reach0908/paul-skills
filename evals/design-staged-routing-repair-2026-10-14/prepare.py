"""Freeze both plugin arms and prepare private cloned Codex homes."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
ROOT=Path('/private/tmp/paul-design-staged-routing-20261014')
RAW=REPO/'.scratch/design-staged-routing-repair-20261014'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def merge_missing(source,target):
    target.mkdir(parents=True,exist_ok=True)
    for item in source.iterdir():
        if item.name in {'.git','__pycache__'}:continue
        dest=target/item.name
        if item.is_dir():merge_missing(item,dest)
        elif not dest.exists():shutil.copy2(item,dest)

def main():
    assert not (RAW/'environment.json').exists(),'Experiment already prepared'
    assert not any(RAW.glob('*/*.meta.json')),'Preserve running experiment'
    ROOT.mkdir(mode=0o700,exist_ok=True);RAW.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((REPO/'.claude-plugin/plugin.json').read_text())
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only','paul-skills@0.4.1','--',*[s.removeprefix('./') for s in manifest['skills']]],cwd=REPO,text=True).splitlines()+['.claude-plugin/plugin.json']
    snapshots={}
    for arm in ['baseline','candidate']:
        bundle=ROOT/arm/'marketplace/plugin';hashes={}
        for relative in paths:
            data=(subprocess.check_output(['git','show','paul-skills@0.4.1:'+relative],cwd=REPO) if arm=='baseline' else (REPO/relative).read_bytes())
            target=bundle/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
            hashes[relative]=hashlib.sha256(data).hexdigest()
        snapshots[arm]={'files':hashes}
        (HERE/(arm+'-manifest.json')).write_text(json.dumps(snapshots[arm],indent=2)+'\n')
        market=bundle.parent/'.claude-plugin';market.mkdir(exist_ok=True)
        (market/'marketplace.json').write_text(json.dumps({'name':'paul-staged-trial','owner':{'name':'Paul Kim'},'plugins':[{'name':'paul-skills','source':'./plugin','category':'design'}]})+'\n')
    # Clone user context once, then copy the identical snapshot for each arm.
    home=Path.home()/'.codex';seed=ROOT/'host-snapshot';seed.mkdir(exist_ok=True)
    for name in ['config.toml','AGENTS.md']:
        if (home/name).exists():shutil.copy2(home/name,seed/name)
    for name in ['skills','memories','plugins/cache','.tmp/marketplaces']:
        if (home/name).exists() and not (seed/name).exists():shutil.copytree(home/name,seed/name,ignore=shutil.ignore_patterns('.git','__pycache__'))
    metadata={}
    for arm in ['baseline','candidate']:
        harness=ROOT/arm/'codex-home';harness.mkdir(exist_ok=True)
        for relative in ['config.toml','AGENTS.md','skills','memories','plugins/cache','.tmp/marketplaces']:
            source=seed/relative;target=harness/relative
            if source.is_file():shutil.copy2(source,target)
            elif source.is_dir():merge_missing(source,target)
        if not (harness/'auth.json').exists():(harness/'auth.json').symlink_to(home/'auth.json')
        config=harness/'config.toml';s=config.read_text()
        import re
        s,count=re.subn(r'(\[plugins\."paul-skills@paul-skills"\]\s*\nenabled\s*=\s*)true',r'\1false',s)
        assert count==1,'Expected one daily Paul plugin setting'
        config.write_text(s)
        env=dict(os.environ,CODEX_HOME=str(harness))
        for label,cmd in [('marketplace',['codex','plugin','marketplace','add',str(ROOT/arm/'marketplace'),'--json']),('install',['codex','plugin','add','paul-skills@paul-staged-trial','--json']),('list',['codex','plugin','list','--json'])]:
            p=subprocess.run(cmd,env=env,text=True,capture_output=True)
            (RAW/(arm+'-'+label+'.json')).write_text(p.stdout)
            if p.returncode:raise RuntimeError(p.stderr)
        install=json.loads((RAW/(arm+'-install.json')).read_text())
        installed=Path(install['installedPath'])
        assert all(digest(installed/p)==d for p,d in snapshots[arm]['files'].items())
        metadata[arm]={'plugin_root':str(installed),'codex_home':str(harness),'bundle':str(ROOT/arm/'marketplace/plugin')}
    (RAW/'environment.json').write_text(json.dumps(metadata,indent=2)+'\n')
    before={}
    for host in ['codex','claude']:
        cache=Path.home()/('.'+host)/'plugins/cache/paul-skills/paul-skills/0.4.1'
        before[host]={p:digest(cache/p) for p in paths}
    (HERE/'global-before.json').write_text(json.dumps(before,indent=2)+'\n')
    changed=[p for p in paths if snapshots['baseline']['files'][p]!=snapshots['candidate']['files'][p]]
    print(json.dumps({'arms':2,'files_each':len(paths),'changed':changed,'global_plugin_untouched':True}))
if __name__=='__main__':main()
