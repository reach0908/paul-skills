"""Verify archived trial integrity and observed invocation, not semantic quality."""
from pathlib import Path
import json,hashlib
R=Path('/Users/jinhokim/dev/paul-skills');E=R/'evals/design-beta-hardening-2026-10-14'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=read(E/'prepared.json');r=read(E/'run-integrity.json');runs={x['id']:x for x in r['runs']};errors=[]
def check(ok,label):
 if not ok:errors.append(label)
check(r['protocolUnchanged'],'Protocol changed')
check(len(p['cases'])==28 and len(runs)==28,'Expected initial 24 contexts and four bounded retests')
explicit={'state-machine','break','explain-interface','variant'};implicit={'information-architecture','user-flow','wireframe','build-design'}
for c in p['cases']:
 x=runs.get(c['id'])
 if x is None:continue
 check(x['receipt']['exitCode']==0 and x['turnCompleted'] and not x['receipt']['timeout'],c['id']+' incomplete')
 check(x['model']=='gpt-5.6-sol' and x['effort']=='xhigh',c['id']+' model mismatch')
 check(not x['inputMissing'],c['id']+' missing input')
 allowed={'app/style.css'} if c['id'] in ['chain-wire','chain-build'] else set()
 check(set(x['inputChanges'])<=allowed,c['id']+' unexpected input edits')
 check(not (set(x['automaticallyAvailable'])&explicit),c['id']+' explicit-only in automatic catalog')
 if c['arm']=='paul':check(implicit<=set(x['automaticallyAvailable']),c['id']+' implicit catalog missing')
 if c['kind'] in ['explicit','chain']:check(c['role'] in x['loadedSkills'],c['id']+' target body not loaded')
 if c['kind'] in ['negative','chain']:
  if c['id']=='negative-state-machine':check(set(x['loadedSkills']) & explicit == {'state-machine'},'Historical boundary failure not preserved')
  else:check(not (set(x['loadedSkills'])&explicit),c['id']+' forbidden implicit body load')
 for expected in c.get('expectedLoaded',[]):check(expected in x['loadedSkills'],c['id']+' expected replacement not loaded')
 if c['arm']=='control':check(not x['loadedSkills'],c['id']+' control loaded skill')
 for entry in x['hostInjectedBodies']:check(entry['fullLocalBodyMatches'],c['id']+' injected body mismatch')
 for h in c.get('handoff',[]):
  check(sha(Path(h['source']))==h['sha256'],c['id']+' source handoff changed '+h['target'])
  if c['id']=='chain-build' and h['target']=='app/style.css':continue
  check(sha(Path(c['workspace'])/h['target'])==h['sha256'],c['id']+' handoff input changed '+h['target'])
for role in ['break','user-flow']:
 for case in ['old','new']:
  rows=[c for c in p['cases'] if c['id'].startswith(role+'-'+case+'-') and not c.get('repairOf')]
  task=lambda row:{k:v for k,v in row['inputs'].items() if k!='PROMPT.md' and not k.startswith('.agents/')}
  check(len(rows)==2 and task(rows[0])==task(rows[1]),role+' '+case+' pair input mismatch')
for role in explicit|implicit:
 path=R/'skills/in-progress'/role
 fm=(path/'SKILL.md').read_text().split('---',2)[1];yaml=(path/'agents/openai.yaml').read_text()
 check(('disable-model-invocation: true' in fm)==(role in explicit),role+' Claude policy mismatch')
 check(('allow_implicit_invocation: false' in yaml)==(role in explicit),role+' Codex policy mismatch')
old=read(R/'evals/design-beta-readiness-2026-10-14/prepared.json')
unchanged=[]
for role in (explicit|implicit)-{'break','user-flow'}:
 c=next(c for c in old['cases'] if c['role']==role and c['arm']=='paul');prefix='.agents/skills/'+role+'/'
 files={k[len(prefix):]:v for k,v in c['inputs'].items() if k.startswith(prefix)}
 check(all(sha(R/'skills/in-progress'/role/k)==v for k,v in files.items()),role+' historical skill changed')
 unchanged.append(role)
out={'status':'pass' if not errors else 'fail','errors':errors,'contexts':len(runs),'explicitCases':sum(x['kind']=='explicit' for x in runs.values()),'negativeCases':sum(x['kind']=='negative' for x in runs.values()),'naturalChainStages':sum(x['kind']=='chain' for x in runs.values()),'unchangedHistoricalSkills':sorted(unchanged),'historicalBoundaryFailure':'negative-state-machine remains FAIL; it is not included as a passing boundary case.','note':'Semantic quality and user acceptance are separate from these integrity assertions.'}
(E/'evidence/integrity-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False));raise SystemExit(bool(errors))
