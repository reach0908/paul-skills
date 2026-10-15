"""Bounded fresh-session checks of the real user-scope installations."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,shutil,signal,subprocess,time,uuid
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
RAW=REPO/'.scratch/first-impression-044-release'
ROOT=Path('/private/tmp/paul-first-impression-044-release-20261015')
def sha(b):return hashlib.sha256(b).hexdigest()
def snap(p):return {str(f.relative_to(p)):sha(f.read_bytes()) for f in sorted(p.rglob('*')) if f.is_file()}
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def events(p):
 rows=[]
 for line in p.read_text().splitlines():
  try:rows.append(json.loads(line))
  except ValueError:pass
 return rows
def run(host,case,i):
 out=RAW/host/case['id'];out.mkdir(parents=True,exist_ok=False)
 cwd=ROOT/host/f'case_{i:03d}';cwd.mkdir(parents=True,exist_ok=False)
 src=HERE/'fixtures'/case['fixture']
 if src.exists():shutil.copytree(src,cwd,dirs_exist_ok=True)
 plugin=Path.home()/f'.{host}/plugins/cache/paul-skills/paul-skills/0.4.4'
 expected=json.loads((HERE/'candidate-manifest.json').read_text())['files']
 assert all(sha((plugin/p).read_bytes())==h for p,h in expected.items()), 'Installed source differs from release'
 prompt=case['prompt'];sid=str(uuid.uuid4())
 if host=='claude':
  cmd=['claude','-p','--verbose','--output-format','stream-json','--input-format','stream-json','--replay-user-messages','--session-id',sid,'--no-session-persistence','--permission-mode','dontAsk','--tools','Skill,Read,Glob,Grep','--allowedTools','Skill,Read,Glob,Grep','--strict-mcp-config','--settings','{"disableAllHooks":true,"autoMemoryEnabled":false}','--max-budget-usd','1','--effort','low']
  payload=json.dumps({'type':'user','message':{'role':'user','content':prompt}},ensure_ascii=False)+'\n'
 else:
  prompt=prompt.replace('/paul-skills:','$paul-skills:');payload=prompt
  cmd=['codex','exec','-c','model_reasoning_effort="low"','--sandbox','read-only','--skip-git-repo-check','--json','-C',str(cwd),'-o',str(out/'final.md'),'-']
 meta={'host':host,'case_id':case['id'],'session_id':sid,'command':cmd,'prompt':prompt,'cwd':str(cwd),'plugin_root':str(plugin),'files_before':snap(cwd),'started_at':datetime.now(timezone.utc).isoformat(),'uses_global_install':True,'freeze_sha256':sha((HERE/'freeze.json').read_bytes())}
 write(out/'meta.json',meta);start=time.monotonic();timeout=False
 with (out/'events.jsonl').open('w') as stream,(out/'stderr.txt').open('w') as err:
  proc=subprocess.Popen(cmd,cwd=cwd,stdin=subprocess.PIPE,stdout=stream,stderr=err,text=True,start_new_session=True)
  try:proc.communicate(payload,timeout=240)
  except subprocess.TimeoutExpired:
   timeout=True;os.killpg(proc.pid,signal.SIGTERM)
   try:proc.wait(timeout=5)
   except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
 rows=events(out/'events.jsonl');result=next((x for x in reversed(rows) if x.get('type')=='result'),{})
 if host=='codex':
  sid=next((x['thread_id'] for x in rows if x.get('type')=='thread.started'),sid);meta['session_id']=sid
  matches=list((Path.home()/'.codex/sessions').rglob('*'+sid+'.jsonl'))
  if len(matches)==1:shutil.copyfile(matches[0],out/'transcript.jsonl')
 meta.update(exit_code=proc.returncode,timed_out=timeout,duration_seconds=round(time.monotonic()-start,3),files_after=snap(cwd),cost_usd=result.get('total_cost_usd'),result_subtype=result.get('subtype'))
 write(out/'meta.json',meta);print(json.dumps({k:meta[k] for k in ['host','case_id','exit_code','timed_out','duration_seconds','cost_usd']}),flush=True)
 return proc.returncode!=0 or timeout
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--host',required=True,choices=['codex','claude']);a=parser.parse_args()
 frozen=json.loads((HERE/'freeze.json').read_text())
 assert frozen['runner']==sha(Path(__file__).read_bytes()) and frozen['cases']==sha((HERE/'cases.json').read_bytes()) and frozen['protocol']==sha((HERE/'PROTOCOL.md').read_bytes()) and frozen['fixtures']==snap(HERE/'fixtures')
 cases=json.loads((HERE/'cases.json').read_text());failures=0
 with ThreadPoolExecutor(max_workers=2) as pool:
  for start in range(0,len(cases),2):
   spent=sum((x.get('cost_usd') if x.get('cost_usd') is not None else 1) for p in (RAW/'claude').glob('*/meta.json') for x in [json.loads(p.read_text())])
   if a.host=='claude' and spent+2.8>6:write(HERE/'claude-stop.json',{'reason':'cost_ceiling','unstarted':[c['id'] for c in cases[start:]]});break
   futures=[pool.submit(run,a.host,c,start+j+1) for j,c in enumerate(cases[start:start+2])]
   failures+=sum(bool(f.result()) for f in futures)
   if failures>=2:write(HERE/f'{a.host}-stop.json',{'reason':'two_execution_failures','unstarted':[c['id'] for c in cases[start+2:]]});break
if __name__=='__main__':main()
