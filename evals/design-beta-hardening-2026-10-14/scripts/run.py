from pathlib import Path
import subprocess,os,json,time,concurrent.futures,sys
R=Path('/Users/jinhokim/dev/paul-skills');T=Path('/private/tmp/paul-beta-hardening-20261014');RAW=R/'.scratch/design-beta-hardening-20261014';E=R/'evals/design-beta-hardening-2026-10-14'
rows=json.loads((E/'prepared.json').read_text())['cases']; wanted=sys.argv[1:]
rows=[r for r in rows if r['kind'] in wanted or r['id'] in wanted] if wanted else rows
baseenv=dict(os.environ,CODEX_HOME=str(T/'codex-home'))
def run(row):
 d=Path(row['workspace']);name=row['id'];session=row['session'];start=time.time()
 assert not (RAW/(name+'.receipt.json')).exists(), 'Do not overwrite trial '+name
 if row['browser']:
  cmd=['playwright-cli','-s='+session,'open','about:blank','--browser=chrome'];p=subprocess.run(cmd,cwd=d,text=True,capture_output=True,timeout=60)
  (RAW/(name+'.browser-setup.json')).write_text(json.dumps({'command':cmd,'exitCode':p.returncode,'stdout':p.stdout,'stderr':p.stderr},indent=2)+'\n')
 cmd=['codex','exec','-m','gpt-5.6-sol','-c','model_reasoning_effort="xhigh"','-c','sandbox_workspace_write.network_access=true','--sandbox','workspace-write','--add-dir','/Users/jinhokim/Library/Caches/ms-playwright/daemon','--skip-git-repo-check','--json','-C',str(d),'-o',str(RAW/(name+'.final.md')),'-']
 timedout=False
 with (RAW/(name+'.events.jsonl')).open('w') as output,(RAW/(name+'.stderr.log')).open('w') as errors:
  try:p=subprocess.run(cmd,env=baseenv,input=(d/'PROMPT.md').read_text(),text=True,stdout=output,stderr=errors,timeout=900);code=p.returncode
  except subprocess.TimeoutExpired:timedout=True;code=None
 result={'id':name,'exitCode':code,'timeout':timedout,'elapsedSeconds':round(time.time()-start,2),'command':cmd}
 (RAW/(name+'.receipt.json')).write_text(json.dumps(result,indent=2)+'\n')
 if row['browser']:
  close=subprocess.run(['playwright-cli','-s='+session,'close'],cwd=d,text=True,capture_output=True,timeout=60)
  (RAW/(name+'.browser-cleanup.json')).write_text(json.dumps({'exitCode':close.returncode,'stdout':close.stdout,'stderr':close.stderr},indent=2)+'\n')
 print(json.dumps(result),flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for _ in pool.map(run,rows):pass
