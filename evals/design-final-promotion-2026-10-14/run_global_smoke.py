"""Run the bounded global release checks from the repository root."""
from pathlib import Path
import json,subprocess,os,hashlib,time,sys
from concurrent.futures import ThreadPoolExecutor
repo=Path.cwd();raw=repo/'.scratch/design-final-release-20261014';base=Path('/private/tmp/paul-design-final-release-20261014');base.mkdir(exist_ok=True)
common='\n이번 턴은 준비 단계만 한다. 관련 지침과 제공 파일을 읽고 적용 범위, 필요한 입력, 완료 조건을 짧게 설명한 뒤 멈춰라. 파일 수정, 구현, 브라우저 실행은 다음 턴이다.'
prompts={
'implicit-ia': '기획이 끝난 자료 보관함의 정보 구조를 정리하려고 한다. BRIEF.md를 기준으로 콘텐츠가 어디에 속하고 사용자가 어떻게 찾는지, 목적지와 탐색 구조를 잡아줘.'+common,
'implicit-flow':'자료 저장 작업의 사용자 흐름을 정의하려고 한다. BRIEF.md를 기준으로 요청 전, 처리 중, 결과 불명, 성공 상태의 행동과 복구 경로를 정리해줘. 패널 닫기와 다시 열기를 포함해줘.'+common,
'implicit-wire':'FLOW.md의 합의한 동작을 바탕으로 로컬에서 조작할 수 있는 저충실도 와이어프레임과 Markdown 화면 명세를 만들려고 한다. 모바일 정보 순서와 주요 행동 배치를 잡아줘.'+common,
'implicit-build':'DESIGN.md는 승인된 로컬 화면 명세다. 기존 index.html의 기능은 보존하고 styles.css의 기존 토큰으로 명세대로 구현하려고 한다.'+common,
}
for n in ['state-machine','break','explain-interface','variant']:
 prompts['explicit-'+n]='$paul-skills:'+n+'\n설치된 이 스킬의 역할과 입력, 완료 조건, 이웃 역할과의 차이만 설명해줘. 이번에는 실제 구현, 조사, 브라우저 조작이나 파일 변경은 하지 마.'
prompts['explicit-router']='$paul-skills:ask-matt\n기획이 끝난 제품을 로컬 정보구조, 흐름, 화면, 승인 시안 구현까지 넘기는 스킬 순서와 기존 컴포넌트 상태 작업대와의 경계를 안내해줘. 지금은 추천만 하고 다른 작업을 실행하지 마.'
fixtures={'BRIEF.md':'# Approved local brief, revision P-84\n자료 목록 D-LIST, 자료 상세 D-ITEM, 저장함 D-SAVED. 상세로 이동했다가 목록의 검색과 필터를 유지해서 돌아온다. 저장 패널은 저장 요청 전 초안을 보존한다. 닫기는 취소가 아니다. 요청 중 또는 결과 불명에서 재전송하지 않는다. 상태 조회 성공 시 receipt S-84를 보여준다. 완료 후 다시 열면 그 receipt를 유지한다. 권한 정책은 미정이다.\n', 'FLOW.md':'# Agreed flow, revision F-84\nD-LIST에서 자료를 열면 D-ITEM. 검색 문맥은 뒤로가기에 보존. 저장 패널 V-OPEN/V-CLOSED는 작업 상태와 독립. T-READY는 초안만, T-PENDING/T-UNKNOWN은 request K-84와 초안, T-DONE은 S-84를 보존한다. 확인 조회만 성공을 확정하며 미정 권한 경로는 구현하지 않는다.\n', 'DESIGN.md':'# Approved design, revision V-84\nindex.html 구조와 상태는 그대로. main padding은 1280px에서 --space-6, 320px에서 --space-4. 새 토큰이나 컴포넌트를 추가하지 않는다. Markdown 전용 기준이므로 픽셀 원본은 없다.\n', 'index.html':'<!doctype html><html lang="ko"><head><link rel="stylesheet" href="styles.css"></head><body><main><h1>자료 보관함</h1><label>검색 <input type="search"></label><button type="button">저장</button></main></body></html>\n','styles.css':':root { --space-4: 16px; --space-6: 24px; } main { padding: 12px; }\n'}


def hashes(w):return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in w.iterdir() if p.is_file()}
def run(name):
 w=base/name;w.mkdir(exist_ok=True)
 selected={'implicit-ia':['BRIEF.md'], 'implicit-flow':['BRIEF.md','FLOW.md'], 'implicit-wire':['BRIEF.md','FLOW.md','index.html','styles.css'], 'implicit-build':['DESIGN.md','index.html','styles.css']}.get(name,[])
 for file in selected:(w/file).write_text(fixtures[file])
 prompt=prompts[name];(raw/(name+'.prompt.txt')).write_text(prompt)
 before=hashes(w);cmd=['codex','exec','-m','gpt-5.6-sol','-c','model_reasoning_effort="xhigh"','--sandbox','read-only','--skip-git-repo-check','--json','-C',str(w),'-o',str(raw/(name+'.final.md')),'-']
 started=time.time()
 with (raw/(name+'.events.jsonl')).open('w') as out,(raw/(name+'.stderr.log')).open('w') as err:
  p=subprocess.run(cmd,input=prompt,text=True,stdout=out,stderr=err,env=dict(os.environ))
 record={'case':name,'exitCode':p.returncode,'seconds':round(time.time()-started,2),'command':cmd,'before':before,'after':hashes(w),'promptSha256':hashlib.sha256(prompt.encode()).hexdigest()}
 (raw/(name+'.receipt.json')).write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'case':name,'exit':p.returncode}),flush=True)
 return p.returncode
with ThreadPoolExecutor(max_workers=3) as pool: results=list(pool.map(run,list(prompts)))
sys.exit(int(any(results)))
