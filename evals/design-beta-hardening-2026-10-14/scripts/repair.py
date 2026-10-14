from pathlib import Path
import json,shutil,hashlib
R=Path('/Users/jinhokim/dev/paul-skills');E=R/'evals/design-beta-hardening-2026-10-14';T=Path('/private/tmp/paul-beta-hardening-20261014')
p=json.loads((E/'prepared.json').read_text());by={c['id']:c for c in p['cases']}
cases=[('negative-state-machine','negative-state-machine-r2',None),('negative-state-machine','negative-state-machine-r3','업로드 작업을 시작하기 전과 완료 후에 사용자가 창을 닫았다 다시 여는 행동을 표로 정리해 주세요. 초안은 같은 방문에서 유지하며 제출 전에는 요청 키가 없습니다. 요청 중 닫기는 취소가 아니고 완료 영수증은 복귀해도 유지합니다. 제품 정책과 사용자 행동만 정하며 구현된 컴포넌트나 전시 화면은 만들지 마세요.'),('explicit-user-flow','explicit-user-flow-r2',None),('user-flow-old-paul','user-flow-old-paul-r2',None)]
for source,name,task in cases:
 old=by[source];d=T/'public/runs'/name;assert not d.exists();d.mkdir()
 for rel in old['inputs']:
  src=Path(old['workspace'])/rel;dest=d/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
 shutil.copytree(R/'skills/in-progress/user-flow',d/'.agents/skills/user-flow',dirs_exist_ok=True)
 (d/'output').mkdir()
 (d/'PROMPT.md').write_text((d/'PROMPT.md').read_text().replace(old['workspace'],str(d)).replace('/runs/'+source+'/', '/runs/'+name+'/'))
 if task:(d/'TASK.md').write_text(task+'\n')
 row={k:v for k,v in old.items() if k not in ['inputs','workspace','id','session']};row.update({'id':name,'workspace':str(d),'session':'hard-'+name,'repairOf':source,'expectedLoaded':['user-flow'],'repairReason':'Clarify direct flow-planning selection and explicit-only state-machine boundary after an observed unauthorized body read.'})
 row['inputs']={str(f.relative_to(d)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(d.rglob('*')) if f.is_file()};p['cases'].append(row)
(E/'prepared.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n')
(E/'REPAIR-1.md').write_text('''# Invocation repair 1

The initial negative-state-machine execution loaded both user-flow and state-machine without the human invoking state-machine. It then correctly declined the workbench and wrote a flow contract. The unauthorized body read still fails the fixed protocol; no workbench execution does not turn it into a pass.

The user-flow catalog description now names unanswered requests and interruption as its direct scope and explicitly excludes loading state-machine without a human invocation. Its opening paragraph reinforces that boundary. The transition procedure is unchanged from the already completed quality pairs.

Within the four-retest budget, preserve the initial failure and run: the same negative input again; a new exit/return negative input; explicit user-flow invocation; and the original PB-72 Paul quality task. The actual flow/wire/build chain uses the repaired user-flow copy and records that body hash. No original result, frozen protocol or previous input manifest entry is rewritten.
''')
print('Prepared four bounded retests')
