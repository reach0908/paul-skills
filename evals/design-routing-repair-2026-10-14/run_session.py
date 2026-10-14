from pathlib import Path
import datetime
import json
import os
import subprocess
import sys

ATTEMPT = os.environ.get('PAUL_TRIAL_ATTEMPT', '2')
SUFFIX = '' if ATTEMPT == '1' else '-r' + ATTEMPT
ROOT = Path('/private/tmp/paul-design-routing-20261014' + SUFFIX)
OUT = Path(__file__).resolve().parents[2] / '.scratch/design-routing-repair-20261014'
if ATTEMPT != '1':
    OUT /= 'attempt-' + ATTEMPT
name=sys.argv[1]
if any((OUT / (name + suffix)).exists() for suffix in ['.events.jsonl', '.receipt.json', '.final.md']):
    raise SystemExit('Preserve completed and interrupted trials; choose a new attempt directory.')
env=dict(os.environ,CODEX_HOME=str(ROOT/'codex-home'))
workspace=ROOT/'cases'/name
cmd=['codex','exec','--json','--sandbox','workspace-write','-C',str(workspace),
     '-o',str(OUT/(name+'.final.md')),'-']
record={'name':name,'command':cmd,'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'history':'new exec, no resume, prompt contains no previous messages'}
with (OUT/(name+'.events.jsonl')).open('w') as stdout, (OUT/(name+'.stderr.log')).open('w') as stderr:
    result=subprocess.run(cmd,input=(OUT/(name+'.prompt.txt')).read_text(),text=True,
                          env=env,cwd=workspace,stdout=stdout,stderr=stderr)
record['exitCode']=result.returncode
record['completedAt']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(OUT/(name+'.receipt.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
sys.exit(result.returncode)
