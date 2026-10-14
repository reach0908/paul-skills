"""Run six fresh read-only Codex sessions against the global installation."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, os, signal, subprocess, time
import run_trials as common
HERE=Path(__file__).resolve().parent
RAW=HERE.parents[1]/'.scratch/design-routing-patch-release-20261014/codex'
BASE=Path('/private/tmp/paul-design-routing-patch-release-20261014/codex')
MODEL_OVERRIDE=None
PROTOCOL=HERE/'PROTOCOL.md'

def run(pair):
    number,case=pair
    name=case['id']; meta=RAW/(name+'.meta.json')
    if meta.exists(): raise RuntimeError('Refusing rerun: '+name)
    cwd=BASE/f'case_{number:03d}';cwd.mkdir(parents=True,exist_ok=False)
    if case.get('fixture')=='git': common.prepare_fixture(cwd)
    prompt=case['prompt'].replace('/paul-skills:','$paul-skills:')
    command=['codex','exec','--sandbox','read-only','--skip-git-repo-check','--json','-C',str(cwd),'-o',str(RAW/(name+'.final.md')),'-']
    if MODEL_OVERRIDE:command[2:2]=['-m',MODEL_OVERRIDE]
    record={'case_id':name,'prompt':prompt,'command':command,'cwd':str(cwd),'before':common.snapshot(cwd),'protocol_sha256':common.digest(PROTOCOL.read_bytes()),'cases_sha256':common.digest((HERE/'cases.json').read_bytes())}
    meta.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    start=time.monotonic();timed_out=False
    with (RAW/(name+'.jsonl')).open('w') as out,(RAW/(name+'.stderr')).open('w') as err:
        p=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=out,stderr=err,text=True,start_new_session=True)
        try:p.communicate(prompt,timeout=360)
        except subprocess.TimeoutExpired:
            timed_out=True;os.killpg(p.pid,signal.SIGTERM)
            try:p.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
    record.update(exit_code=p.returncode,timed_out=timed_out,seconds=round(time.monotonic()-start,3),after=common.snapshot(cwd))
    meta.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'case':name,'exit':p.returncode,'seconds':record['seconds']}),flush=True)
    return p.returncode or timed_out

def main():
    RAW.mkdir(parents=True,exist_ok=True)
    cases=json.loads((HERE/'cases.json').read_text())['cases']
    # Two sessions at a time; do not launch further cases after repeated environment failure.
    failures=0
    with ThreadPoolExecutor(max_workers=2) as pool:
        for offset in range(0,len(cases),2):
            failures+=sum(pool.map(run,list(enumerate(cases,1))[offset:offset+2]))
            if failures>=2: raise RuntimeError('Repeated environment failure')

if __name__=='__main__':main()
