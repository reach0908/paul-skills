"""Run frozen cases in fresh native host processes; preserve every attempt."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
import argparse,hashlib,json,os,signal,shutil,subprocess,time,uuid
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
ROOT=Path('/private/tmp/paul-design-domain-entry-20261014');RAW=REPO/'.scratch/design-domain-entry-repair-20261014'
CONFIG=json.loads((HERE/'cases.json').read_text())
ENV=json.loads((RAW/'environment.json').read_text()) if (RAW/'environment.json').exists() else {}
CACHE=Path.home()/'.claude/plugins/cache/paul-skills/paul-skills/0.4.1';BUNDLE=ROOT/'candidate/marketplace/plugin'
def digest(data):return hashlib.sha256(data).hexdigest()
def read_events(path):
    rows=[]
    for line in path.read_text().splitlines():
        try:rows.append(json.loads(line))
        except json.JSONDecodeError:pass
    return rows
def snapshot(path):return {str(p.relative_to(path)):digest(p.read_bytes()) for p in sorted(path.rglob('*')) if p.is_file()}
def prepare_fixture(cwd,kind='git'):
    def git(*args):return subprocess.check_output(['git','-c','core.hooksPath=/dev/null',*args],cwd=cwd,stderr=subprocess.STDOUT)
    def commit(message):git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','-c','commit.gpgsign=false','commit','-qm',message)
    git('init','-q','-b','main');(cwd/'src').mkdir()
    fixtures=REPO/'evals/design-claude-routing-repair-2026-10-14/fixtures'
    before=(fixtures/'before.html').read_bytes();after=(fixtures/'after.html').read_bytes()
    (cwd/'src/Panel.html').write_bytes(after);git('add','src/Panel.html');commit('Initial screen')
    git('switch','-qc','feature/checkout')
    (cwd/'src/Panel.html').write_bytes(before);git('add','src/Panel.html');commit('Name the close control')
    assert git('rev-parse','main')!=git('rev-parse','HEAD')
    (cwd/'src/Panel.html').write_bytes(after);git('add','src/Panel.html')
    if kind=='index-divergent':
        (cwd/'src/Panel.html').write_bytes(before)
        (cwd/'src/New.html').write_text('<button id="new-action"><svg aria-hidden="true"></svg></button>\n')
        assert git('diff','HEAD')==b''
        assert b'aria-label' in git('diff','--cached','HEAD')
        assert b'New.html' in git('ls-files','--others','--exclude-standard')
def run(case,host,number):
    arm=case['arm'];name=case['id'];out=RAW/host;out.mkdir(exist_ok=True)
    meta_path=out/(name+'.meta.json');assert not meta_path.exists(),'Preserve existing run'
    cwd=ROOT/'cases'/host/f'case_{number:03d}';cwd.mkdir(parents=True,exist_ok=False)
    if case.get('fixture')in {'git','index-divergent'} or case['mode']=='handoff':prepare_fixture(cwd,case.get('fixture','git'))
    sid=str(uuid.uuid4());prompt=case['prompt'];env=dict(os.environ)
    plugin=Path(ENV[arm]['plugin_root']) if host=='codex' else BUNDLE
    if host=='claude':
        cmd=['claude','-p','--verbose','--output-format','stream-json','--input-format','stream-json','--replay-user-messages','--session-id',sid,'--permission-mode','dontAsk','--tools','Skill,Read,Glob,Grep','--allowedTools','Skill,Read,Glob,Grep','--strict-mcp-config','--settings','{"disableAllHooks":true}','--max-budget-usd',str(4 if case['mode']=='handoff' else 1),'--plugin-dir',str(plugin)]
        if case['mode']=='handoff':
            cmd[cmd.index('--tools')+1]+=',Bash'
            cmd[cmd.index('--allowedTools')+1]+=','+','.join('Bash(git '+v+' *)' for v in ['status','diff','show','rev-parse','log','ls-files','blame','remote','branch','merge-base','symbolic-ref','grep'])
        if case['mode']=='handoff':prompt+='\n파일과 참조 문서는 Read/Glob/Grep으로 읽고, Git 조회는 허용된 읽기 전용 git 하위 명령을 각각 하나의 Bash 호출로 실행해. 셸 연결이나 파이프, cd, git -C 없이 현재 폴더에서 조회해.'
        payload=json.dumps({'type':'user','message':{'role':'user','content':prompt}})+'\n'
    else:
        prompt=prompt.replace('/paul-skills:','$paul-skills:');payload=prompt;env['CODEX_HOME']=ENV[arm]['codex_home']
        cmd=['codex','exec','-m','gpt-5.6-sol','--sandbox','read-only','--skip-git-repo-check','--json','-C',str(cwd),'-o',str(out/(name+'.final.md')),'-']
    meta={'host':host,'arm':arm,'case_id':name,'session_id':sid,'command':cmd,'plugin_root':str(plugin),'cwd':str(cwd),'prompt':prompt,'files_before':snapshot(cwd),'started_at':datetime.now(timezone.utc).isoformat(),'protocol_sha256':digest((HERE/'PROTOCOL.md').read_bytes()),'cases_sha256':digest((HERE/'cases.json').read_bytes()),'bundle_manifest_sha256':digest((HERE/(arm+'-manifest.json')).read_bytes())}
    if host=='claude':meta['host_protocol_sha256']=digest((HERE/'CLAUDE-PROTOCOL.md').read_bytes())
    meta_path.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');start=time.monotonic();timed_out=False
    with (out/(name+'.jsonl')).open('w') as stream,(out/(name+'.stderr')).open('w') as err:
        p=subprocess.Popen(cmd,cwd=cwd,env=env,stdin=subprocess.PIPE,stdout=stream,stderr=err,text=True,start_new_session=True)
        try:p.communicate(payload,timeout=360)
        except subprocess.TimeoutExpired:
            timed_out=True;os.killpg(p.pid,signal.SIGTERM)
            try:p.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
    events=read_events(out/(name+'.jsonl'))
    if host=='claude':traces=list((Path.home()/'.claude/projects').glob(f'*/{sid}.jsonl'))
    else:
        sid=next((e['thread_id'] for e in events if e.get('type')=='thread.started'),sid);meta['session_id']=sid
        traces=list((Path(env['CODEX_HOME'])/'sessions').rglob('*'+sid+'.jsonl'))
    if len(traces)==1:shutil.copyfile(traces[0],out/(name+'.transcript.jsonl'))
    result=next((e for e in reversed(events) if e.get('type')=='result'),{})
    meta.update(exit_code=p.returncode,timed_out=timed_out,duration_seconds=round(time.monotonic()-start,3),files_after=snapshot(cwd),total_cost_usd=result.get('total_cost_usd'),result_subtype=result.get('subtype'))
    meta_path.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:meta[k] for k in ['host','case_id','exit_code','duration_seconds','total_cost_usd']}),flush=True)
    return int(p.returncode!=0 or timed_out)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--host',choices=['codex','claude'],required=True);parser.add_argument('--phase',choices=['pilot','remaining','all'],default='all');args=parser.parse_args()
    cases=[]
    if args.host=='codex' and CONFIG.get('codex_baseline_repeats',0):
        for i in range(3):
            base=dict(CONFIG['cases'][i],id='baseline-staged-'+str(i+1),arm='baseline');cases.extend([base,CONFIG['cases'][i]])
        cases+=CONFIG['cases'][3:]
    else:cases=CONFIG['cases']
    selected=[(c,i+1) for i,c in enumerate(cases) if (args.phase=='all' or (c['id'] in {'staged-type-color','staged-type-color-2','staged-type-color-3','normal-better-colors','normal-better-colors-2','normal-better-colors-3'})==(args.phase=='pilot')) and not (RAW/args.host/(c['id']+'.meta.json')).exists()]
    failures=0
    with ThreadPoolExecutor(max_workers=2) as pool:
        for offset in range(0,len(selected),2):
            cost=sum(json.loads(p.read_text()).get('total_cost_usd') or 0 for p in (RAW/'claude').glob('*.meta.json'))
            if cost>=20:raise RuntimeError('Claude cost stop')
            futures=[pool.submit(run,c,args.host,i) for c,i in selected[offset:offset+2]]
            failures+=sum(f.result() for f in futures)
            if failures>=2:raise RuntimeError('Repeated environment failure')
if __name__=='__main__':main()
