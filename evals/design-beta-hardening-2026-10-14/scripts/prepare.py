from pathlib import Path
import json,shutil,hashlib
R=Path('/Users/jinhokim/dev/paul-skills'); E=R/'evals/design-beta-hardening-2026-10-14'; T=Path('/private/tmp/paul-beta-hardening-20261014'); RAW=R/'.scratch/design-beta-hardening-20261014'
assert not T.exists(), 'Never overwrite an execution'
(T/'public/runs').mkdir(parents=True); (T/'codex-home').mkdir()
(T/'codex-home/auth.json').symlink_to(Path('/Users/jinhokim/.codex/auth.json'))
(T/'codex-home/config.toml').write_text('model="gpt-5.6-sol"\nmodel_reasoning_effort="xhigh"\n')
roles=['information-architecture','user-flow','wireframe','state-machine','break','explain-interface','variant','build-design']
reg=json.loads((R/'skill-sources.json').read_text())
origin=R/'.scratch/design-role-parity-20261012/runs/build-design-original-r1/.agents'
manifest=json.loads((R/'evals/design-beta/upstream-manifest.json').read_text())
for name,sha in manifest['files'].items():
 p=origin/name if name!='LICENSE' else origin/'skills/build-design/LICENSE'
 assert hashlib.sha256(p.read_bytes()).hexdigest()==sha,name
base=E/'fixtures';base.mkdir()
for role in ['break','user-flow']:
 shutil.copytree(R/'evals/design-beta-readiness-2026-10-14/fixtures'/role,base/(role+'-old'))
def put(root,path,text):
 p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
new=base/'break-new'
put(new,'BRIEF.md','''# Attachment card AC-19
Internal task attachments have human-readable filenames, maximum 220 Unicode characters. Existing usage presents a list within a normal 760px panel and a 280px sidebar. Both legacy single-line and supported wrapping modes exist in production. Do not change the policy, component or CSS. Empty and loading states are reachable; names, item counts, read-only state and the wrapping prop can vary. A typical filename is 회의록_다음분기_검토.pdf. No backend or account is required.
''')
put(new,'app/attachment.js','''export function renderAttachments({items=[],loading=false,readOnly=false,wrapNames=false}={}){const root=document.createElement('section');root.className='attachments'+(wrapNames?' wrap':'');root.setAttribute('aria-label','첨부 파일');const h=document.createElement('h2');h.textContent='첨부 파일';root.append(h);if(loading){root.setAttribute('aria-busy','true');const p=document.createElement('p');p.setAttribute('role','status');p.textContent='불러오는 중';root.append(p);return root;}if(!items.length){const p=document.createElement('p');p.textContent='첨부 파일이 없습니다';root.append(p);return root;}for(const item of items){const b=document.createElement('button');b.className='filename';b.textContent=item.name;b.disabled=readOnly;root.append(b);}return root;}
''')
put(new,'app/style.css','''*{box-sizing:border-box}body{margin:0;font:16px/1.5 system-ui;color:#17212b;background:#f4f5f7}main{max-width:1000px;margin:auto;padding:24px}button{font:inherit;padding:8px 12px;border:1px solid #60758c;background:#fff;border-radius:6px}.attachments{padding:16px;border:1px solid #60758c;background:#fff}.filename{display:block;white-space:nowrap;margin:8px 0}.attachments.wrap .filename{max-width:100%;white-space:normal;overflow-wrap:anywhere;text-align:left}:focus-visible{outline:3px solid #c64c00}
''')
put(new,'app/index.html','''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>첨부 파일</title><link rel="stylesheet" href="style.css"><main><h1>업무 자료</h1><div id="target"></div></main><script type="module">import{renderAttachments}from'./attachment.js';document.querySelector('#target').append(renderAttachments({items:[{name:'회의록_다음분기_검토.pdf'}]}));</script></html>''')
put(new,'app/README.md','Static ES modules. Import renderAttachments and inherit style.css. Both wrapNames=false and wrapNames=true are actual supported modes. No application state or external calls.')
put(new,'TASK.md','''BRIEF.md의 첨부 파일 컴포넌트 app/attachment.js를 실제 import하는 스트레스 페이지를 app/stress/에 만들어 주세요. 실제 입력 제약, 내용 길이와 수량, 760px/280px 컨테이너, 두 줄바꿈 모드와 도달 가능한 상태를 다룹니다. 제품 파일과 스타일은 그대로 유지합니다. 한 번 페이지를 열어 모든 시나리오를 보고 실제 깨짐만 페이지와 output/report.md에 기록해 주세요. 정상 모드도 함께 관찰하고 결과 페이지를 남겨 주세요. 수정이나 품질 판정은 범위 밖입니다.''')
new=base/'user-flow-new'
put(new,'BRIEF.md','''# Export job EX-44, approved decisions revision 2
An analyst exports the currently filtered report D-REPORT into a download area D-EXPORT. Filters q=주간, owner=나, sort=recent are retained on return. The form draft contains a filename and CSV/JSON format. Before submission no job key or receipt exists. The initial request creates key J-44 then becomes timeout-unknown. The server may still be processing; approved recovery is checking this key, never resubmitting. First status check returns pending; second returns ready with receipt E-44 and a download URL. Downloading again does not create a new job. Closing is offered before submitting, while running or uncertain, and after ready; it does not cancel work and the draft persists for this local visit. Reopening restores known state; it must not invent a key before submission or lose the receipt after ready. Repeated submit/check events while their corresponding request is pending are ignored. Truly failed is distinct from unknown but retry policy after a confirmed failure is not yet approved. Auth recovery and retention across browser restart are unspecified. Do not decide them. D-REPORT and D-EXPORT remain the only destinations in scope.
''')
put(new,'TASK.md','''BRIEF.md의 내보내기 작업 하나만 output/flow.md에 상태와 전이 표로 명세해 주세요. 사용자가 볼 수 있는 행동, 실제 성공 기준, 상태 확인·중복 입력·닫기와 복귀·재다운로드·미결 정책을 구분해 주세요. 표의 행동과 전이가 일치하는지 경로를 따라 확인하고 결과를 남겨 주세요. 구현 코드와 화면 배치는 이번 범위 밖입니다.''')
rows=[]
def bundle(dest,arm):
 if arm=='original':shutil.copytree(origin/'skills',dest/'.agents/skills')
 elif arm=='paul':
  for rec in reg['skills']:
   if rec['path'].startswith('skills/design/') or rec['id'] in roles+['prototype']:
    shutil.copytree(R/rec['path'],dest/'.agents/skills'/rec['id'])
def add(name,role,arm,kind,src=None,task=None,browser=False):
 d=T/'public/runs'/name
 if src:shutil.copytree(src,d)
 else:d.mkdir()
 (d/'output').mkdir(exist_ok=True);bundle(d,arm)
 if task:put(d,'TASK.md',task)
 session='hard-'+name
 common=f'''Execute one local task in {d}. Read TASK.md and its inputs. Use only the supplied local skill bundle. Never read the source repository, other trial workspaces, evaluator reports, earlier results, or global memory. Do not spawn agents. Do not self-grade parity. The user's scope overrides generic skill advice. Keep all artifact writes inside this workspace. Write outputs in Korean and report limits honestly. URL base: http://127.0.0.1:48924/runs/{name}/ . No account or live API. Target five minutes, hard execution limit fifteen minutes. '''
 if kind=='quality':common+=(f'User explicitly invokes ${role}. Read its local SKILL.md and applicable references. ' if arm!='control' else 'Use ordinary capabilities without loading any design or product skill; none is supplied. ')
 if kind=='explicit':common+=f'User explicitly invokes ${role}. This is a role-boundary check only: load the skill, explain its input, output, neighboring roles and stopping point in output/scope.md. Do not execute the simulated design task. '
 if browser:common+=f'''Browser operations must use installed playwright-cli, read its help. A task-owned session {session} is already opened at about:blank with Chrome. Always use -s={session}; goto your own task URL. Do not launch or attach another session. Setup is not observation. Report errors without bypassing permissions. Preserve the page, close only your session when done. '''
 put(d,'PROMPT.md',common+'Read TASK.md now.\n')
 hashes={str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(d.rglob('*')) if p.is_file()}
 rows.append({'id':name,'role':role,'arm':arm,'kind':kind,'workspace':str(d),'session':session,'browser':browser,'inputs':hashes})
for role in ['break','user-flow']:
 for case in ['old','new']:
  for arm in ['original' if role=='break' else 'control','paul']:
   add(f'{role}-{case}-{arm}',role,arm,'quality',base/f'{role}-{case}',browser=role=='break')
for role in roles:add('explicit-'+role,role,'paul','explicit',task='요청한 스킬의 현재 역할과 종료 경계만 설명해 주세요. 실제 디자인 산출물, 구현, 브라우저 조작은 하지 않습니다.')
negatives={
 'state-machine':'저장 API가 응답하지 않았을 때 사용자가 무엇을 할 수 있어야 할지 행동과 복구 경로만 Markdown으로 정리해 주세요. 요청 키로 상태 확인 API는 존재하며 재전송은 허용하지 않습니다. UI 작업대나 컴포넌트 상태 전시 페이지를 만들 필요는 없습니다.',
 'break':'다음 CSS에서 긴 파일명이 280px 컨테이너를 넘치지 않게 할 최소 수정을 코드 조각으로 제시해 주세요: .name { white-space: nowrap; } 이름은 전체를 읽을 수 있어야 합니다. 프로젝트나 브라우저 없이 이 조각만 답하세요.',
 'explain-interface':'CSS의 blur(8px)와 backdrop-filter: blur(8px)의 차이를 한 문단과 작은 예제로 설명해 주세요. 특정 화면이나 사이트를 분석하는 요청은 아니며 브라우저 관찰은 필요 없습니다.',
 'variant':'다음 카드의 패딩만 16px에서 24px로 바꾸는 CSS 조각을 작성해 주세요: .card { padding: 16px; border-radius: 8px; } 다른 디자인 선택과 비교 화면은 필요 없습니다.'}
for role,task in negatives.items():add('negative-'+role,role,'paul','negative',task=task)
# First chain input is fixed now; later stages use the actual preceding outputs.
add('chain-ia','information-architecture','paul','chain',task='BRIEF.md의 정보 구조를 output/map.md로 정리해 주세요. 콘텐츠와 기존 목적지의 관계, 검색·필터·직접 진입·복귀, 좁은 화면 우선순위와 미결 정책을 명시해 주세요. 화면 배치나 코드는 만들지 마세요.')
d=T/'public/runs/chain-ia';shutil.copyfile(base/'user-flow-old/BRIEF.md',d/'BRIEF.md')
rows[-1]['inputs']['BRIEF.md']=hashlib.sha256((d/'BRIEF.md').read_bytes()).hexdigest()
for role in ['break','user-flow']:
 for case in ['old','new']:
  pair=[r for r in rows if r['id'].startswith(f'{role}-{case}-')]
  task=lambda r:{k:v for k,v in r['inputs'].items() if not k.startswith('.agents/') and k!='PROMPT.md'}
  assert task(pair[0])==task(pair[1])
(E/'prepared.json').write_text(json.dumps({'model':'gpt-5.6-sol','effort':'xhigh','root':str(T),'originalRevision':manifest['revision'],'originalFilesVerified':len(manifest['files']),'protocolSha256':hashlib.sha256((E/'PROTOCOL.md').read_bytes()).hexdigest(),'cases':rows},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'prepared':len(rows),'pairInputsEqual':4,'sourceFilesVerified':len(manifest['files'])}))
