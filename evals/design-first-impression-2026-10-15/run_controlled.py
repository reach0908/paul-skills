"""Run frozen read-only tasks with session-local plugins; retain every attempt."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import argparse, hashlib, json, os, shutil, signal, subprocess, time, uuid

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
ROOT=Path('/private/tmp/paul-first-impression-controlled-20261015')
RAW=REPO/'.scratch/first-impression-controlled-runs'
BASE='154c1a615fa973cefaf7a046fa074082417e91d5'

def sha(data): return hashlib.sha256(data).hexdigest()
def snapshot(path): return {str(p.relative_to(path)):sha(p.read_bytes()) for p in sorted(path.rglob('*')) if p.is_file()}
def write(path,data): path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def prepare():
 assert not ROOT.exists(),'Preserve previous trial root'
 ROOT.mkdir();RAW.mkdir(parents=True,exist_ok=False)
 a=ROOT/'bundle-a';a.mkdir()
 archive=subprocess.check_output(['git','archive',BASE,'skills','.claude-plugin'],cwd=REPO)
 subprocess.run(['tar','-x','-C',str(a)],input=archive,check=True)
 b=ROOT/'bundle-b';b.mkdir()
 for name in ['skills','.claude-plugin']:shutil.copytree(REPO/name,b/name)
 frozen={'base':BASE,'created_at':datetime.now(timezone.utc).isoformat(),'protocol':sha((HERE/'CONTROLLED-PROTOCOL.md').read_bytes()),'cases':sha((HERE/'controlled-cases.json').read_bytes()),'runner':sha(Path(__file__).read_bytes()),'fixtures':snapshot(HERE/'fixtures'),'arms':{'baseline':snapshot(a),'candidate':snapshot(b)}}
 write(HERE/'controlled-freeze.json',frozen)
 settings=Path.home()/'.claude/settings.json'
 data=json.loads(settings.read_text()) if settings.exists() else {}
 write(HERE/'controlled-environment.json',{'host':subprocess.check_output(['claude','--version'],text=True).strip(),'configured_model':data.get('model'),'configured_effort':data.get('effortLevel'),'user_settings_sha256':sha(settings.read_bytes()) if settings.exists() else None,'model_override':False,'effort_override':'high','daily_plugin_changed':False,'tools':['Skill','Read','Glob','Grep']})

def events(path):
 out=[]
 for line in path.read_text().splitlines():
  try:out.append(json.loads(line))
  except json.JSONDecodeError:pass
 return out

def run(case,arm,number):
 out=RAW/f'{arm}-{case["id"]}';out.mkdir(exist_ok=False)
 cwd=ROOT/f'case_{number:03d}';cwd.mkdir(exist_ok=False)
 src=HERE/'fixtures'/case['fixture']
 if src.exists():shutil.copytree(src,cwd,dirs_exist_ok=True)
 bundle=ROOT/('bundle-a' if arm=='baseline' else 'bundle-b')
 sid=str(uuid.uuid4())
 cmd=['claude','-p','--verbose','--output-format','stream-json','--input-format','stream-json','--replay-user-messages','--session-id',sid,'--no-session-persistence','--permission-mode','dontAsk','--tools','Skill,Read,Glob,Grep','--allowedTools','Skill,Read,Glob,Grep','--strict-mcp-config','--settings','{"disableAllHooks":true,"autoMemoryEnabled":false}','--max-budget-usd','0.75','--effort','high','--plugin-dir',str(bundle),'--add-dir',str(bundle)]
 payload=json.dumps({'type':'user','message':{'role':'user','content':case['prompt']}},ensure_ascii=False)+'\n'
 meta={'arm':arm,'case_id':case['id'],'session_id':sid,'command':cmd,'cwd':str(cwd),'bundle':str(bundle),'prompt':case['prompt'],'files_before':snapshot(cwd),'started_at':datetime.now(timezone.utc).isoformat(),'freeze_sha256':sha((HERE/'controlled-freeze.json').read_bytes())}
 write(out/'meta.json',meta);start=time.monotonic();timeout=False
 with (out/'events.jsonl').open('w') as stream,(out/'stderr.txt').open('w') as err:
  p=subprocess.Popen(cmd,cwd=cwd,stdin=subprocess.PIPE,stdout=stream,stderr=err,text=True,start_new_session=True)
  try:p.communicate(payload,timeout=360)
  except subprocess.TimeoutExpired:
   timeout=True;os.killpg(p.pid,signal.SIGTERM)
   try:p.wait(timeout=5)
   except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
 rows=events(out/'events.jsonl');result=next((x for x in reversed(rows) if x.get('type')=='result'),{})
 init=next((x for x in rows if x.get('type')=='system' and x.get('subtype')=='init'),{})
 meta.update(exit_code=p.returncode,timed_out=timeout,duration_seconds=round(time.monotonic()-start,3),files_after=snapshot(cwd),cost_usd=result.get('total_cost_usd'),result_subtype=result.get('subtype'),actual_model=init.get('model'),usage=result.get('usage'),model_usage=result.get('modelUsage'))
 write(out/'meta.json',meta)
 print(json.dumps({k:meta[k] for k in ['arm','case_id','exit_code','duration_seconds','cost_usd','actual_model','result_subtype']}),flush=True)
 return p.returncode!=0 or timeout

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--prepare',action='store_true');parser.add_argument('--start',type=int,default=0);parser.add_argument('--count',type=int,default=10);args=parser.parse_args()
 if args.prepare:prepare();return
 frozen=json.loads((HERE/'controlled-freeze.json').read_text())
 assert frozen['runner']==sha(Path(__file__).read_bytes())
 assert frozen['protocol']==sha((HERE/'CONTROLLED-PROTOCOL.md').read_bytes()) and frozen['cases']==sha((HERE/'controlled-cases.json').read_bytes())
 assert frozen['fixtures']==snapshot(HERE/'fixtures')
 for arm,name in [('baseline','bundle-a'),('candidate','bundle-b')]:assert frozen['arms'][arm]==snapshot(ROOT/name)
 cases=json.loads((HERE/'controlled-cases.json').read_text());failures=0
 with ThreadPoolExecutor(max_workers=2) as pool:
  for i in range(args.start,min(len(cases),args.start+args.count)):
   prior=REPO/'.scratch/first-impression-runs'
   spent=sum((x.get('cost_usd') if x.get('cost_usd') is not None else cap) for folder,cap in [(prior,1.0),(RAW,0.75)] for p in folder.glob('*/meta.json') for x in [json.loads(p.read_text())])
   if spent+1.5>12:
    write(HERE/'controlled-stop.json',{'reason':'cost_ceiling','reserved_cost_usd':spent,'unstarted_cases':[c['id'] for c in cases[i:]]});break
   arms=['baseline','candidate'] if i%2==0 else ['candidate','baseline']
   pending=[pool.submit(run,cases[i],arm,2*i+j+1) for j,arm in enumerate(arms)]
   failures+=sum(bool(f.result()) for f in pending)
   if failures>=2:
    write(HERE/'controlled-stop.json',{'reason':'two_execution_failures','unstarted_cases':[c['id'] for c in cases[i+1:]]});break

if __name__=='__main__':main()
