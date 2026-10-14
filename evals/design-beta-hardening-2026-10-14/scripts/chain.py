from pathlib import Path
import shutil,json,hashlib,sys
R=Path('/Users/jinhokim/dev/paul-skills');E=R/'evals/design-beta-hardening-2026-10-14';T=Path('/private/tmp/paul-beta-hardening-20261014');RAW=R/'.scratch/design-beta-hardening-20261014'
stage=sys.argv[1];names={'flow':'user-flow','wire':'wireframe','build':'build-design'};role=names[stage];name='chain-'+stage;d=T/'public/runs'/name
assert not d.exists(),'Never overwrite a stage'
(d/'input').mkdir(parents=True);(d/'output').mkdir();shutil.copytree(T/'public/runs/chain-ia/.agents',d/'.agents');shutil.copytree(R/'skills/in-progress/user-flow',d/'.agents/skills/user-flow',dirs_exist_ok=True);shutil.copyfile(T/'public/runs/chain-ia/BRIEF.md',d/'BRIEF.md')
links=[]
def take(source,target):
 assert source.exists(),str(source)
 p=d/target;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,p)
 links.append({'source':str(source),'target':target,'sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
take(T/'public/runs/chain-ia/output/map.md','input/map.md')
if stage in ['wire','build']:take(T/'public/runs/chain-flow/output/flow.md','input/flow.md')
if stage=='wire':
 (d/'app').mkdir();shutil.copyfile(R/'evals/design-beta-readiness-2026-10-14/fixtures/wireframe/app/style.css',d/'app/style.css')
 task='BRIEF.md와 실제 앞 단계 산출물 input/map.md, input/flow.md를 사용해 D-ITEM의 T-SAVE를 조작 가능한 낮은 충실도의 화면으로 만들어 주세요. app/index.html 및 output/screens.md에 산출물을 남기고 기존 app/style.css의 기본 스타일과 토큰을 사용해 주세요. 목적지·상태·전이 ID와 미결 정책을 보존하고 모의 네트워크·저장 경계를 명시하세요. 닫기/복귀는 시작 전, pending, timeout-unknown, 확인 중, 완료를 모두 다루며, 확인 첫 pending·두 번째 S-72, 초안과 목록 문맥 유지, 내부 본문/출처 이동을 실제 동작으로 연결하세요. 명시적 초기화 버튼으로만 초기화합니다. 1280x900과320x700에서 상태·키보드·가로 넘침을 Playwright CLI로 관찰하고 기록하세요. 브랜드 시안이나 실제 서버 구현은 범위 밖입니다.'
if stage=='build':
 take(T/'public/runs/chain-wire/output/screens.md','input/screens.md')
 shutil.copytree(T/'public/runs/chain-wire/app',d/'app')
 for f in sorted((T/'public/runs/chain-wire/app').rglob('*')):
  if f.is_file():links.append({'source':str(f),'target':'app/'+str(f.relative_to(T/'public/runs/chain-wire/app')),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 (d/'REFERENCE.md').write_text('''# Local design specification LC-72 revision 1
This is an evaluator-approved synthetic design input, not real-user acceptance. The actual wireframe app and input/screens.md are the behavioral baseline. Preserve all controls, text, IDs, state transitions and unresolved product policies. Change only main content padding: at 1280x900 use existing --space-3 (24px); at 320x700 use existing --space-2 (16px). No new token, component or visual direction. App style.css already provides these tokens. Keep all script/HTML and other files byte-identical. Edit app/style.css only. The reference is Markdown, so report specification conformance, not pixel fidelity to an absent image. Record computed padding and captures at both widths, then replay the save/check/close/reopen and keyboard behavior from the inherited flow. Missing production API and real-user acceptance remain open.
''')
 task='REFERENCE.md의 선택된 로컬 시안을 기존 app 화면에 구현해 주세요. 실제 앞 단계 자료 input/map.md, input/flow.md, input/screens.md를 읽고 동작과 미결 정책을 보존하세요. 수정은 app/style.css만 허용합니다. 두 폭에서 렌더링된 값과 행동을 Playwright CLI로 비교해 output/report.md에 입력 버전·증거·미결 사항을 기록해 주세요. 이 테스트 시안의 변경은 선택된 상태이므로 재선택 질문 없이 진행하세요.'
# Keep all actual tasks in the user's Korean language.
if stage=='flow':task='BRIEF.md와 실제 앞 단계 산출물 input/map.md를 입력으로 T-SAVE의 사용자 행동과 제품 응답을 상태·전이 표로 output/flow.md에 명세해 주세요. 앞 단계 목적지 ID와 미결 사항을 유지하고 시작 전부터 성공 후까지의 이탈·복귀, 중복 방지, 결과가 알려지지 않은 경우와 상태 확인 경로를 다루세요. 화면 배치와 코드는 범위 밖입니다.'
(d/'TASK.md').write_text(task+'\n');session='hard-'+name;browser=stage!='flow'
prompt=f'''Execute one local task in {d}. Read TASK.md and its actual preceding artifacts. Use only supplied local skills when applicable. No source repository, other trial workspaces, evaluator reports, earlier results or global memory. Do not spawn agents. Do not self-grade. Keep writes in this workspace. Output Korean. URL base http://127.0.0.1:48924/runs/{name}/ . No live accounts or API. Soft target five minutes; hard limit fifteen minutes. '''
if browser:prompt+=f'For browser work use installed playwright-cli after its help. Task-owned session {session} is already open at about:blank; always use -s={session}, never attach another session. Preserve output page. Close only your own session. '
(d/'PROMPT.md').write_text(prompt+'Read TASK.md now.\n')
hashes={str(p.relative_to(d)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(d.rglob('*')) if p.is_file()}
p=json.loads((E/'prepared.json').read_text());p['cases'].append({'id':name,'role':role,'arm':'paul','kind':'chain','workspace':str(d),'session':session,'browser':browser,'inputs':hashes,'handoff':links})
(E/'prepared.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'id':name,'handoffFiles':len(links)},ensure_ascii=False))
