"""Create synthetic, public development fixtures. Never overwrite trial receipts."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
CSS = '''*{box-sizing:border-box}body{margin:0;background:#f5f5f2;color:#18242c;font:18px/1.6 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo",sans-serif}main{max-width:1080px;margin:auto;padding:40px}h1{font-size:38px;line-height:1.25}h2{font-size:25px}p{max-width:70ch}button,a{font:inherit}button{padding:10px 18px;background:white;color:#18242c;border:1px solid #78858e;border-radius:7px;min-height:44px}button:focus-visible,a:focus-visible{outline:3px solid #1849be;outline-offset:4px}.primary{background:#193e7c;color:white}.row{display:flex;gap:12px;flex-wrap:wrap}.panel{border:1px solid #c4ccd0;border-radius:8px;padding:20px;background:white;margin-block:20px}.badge{background:#efd637;padding:24px;font-size:46px;font-weight:800}.muted{color:#445666}.warning{border-inline-start:6px solid #9b2e24;background:#fff0eb;padding:18px}table{border-collapse:collapse;width:100%}th,td{text-align:left;border-bottom:1px solid #bdc6cb;padding:12px}a{color:#174a84}nav{display:flex;gap:20px}@media(max-width:600px){main{padding:20px}h1{font-size:30px}.badge{font-size:34px}}
'''
SCREENS = {
 'landing': ('<nav><b>모아</b><a href="#price">요금</a><a href="#security">보안</a></nav><div class="badge">NEW · AI POWERED · 1위</div><h1 style="font-size:24px">팀 회의록을 한곳에서 정리하세요</h1><p>녹음 파일을 올리면 회의록 초안을 만들고 팀과 확인할 수 있습니다.</p><button class="primary">회의록 만들기</button><div class="row panel"><b>혁신</b><b>빠름</b><b>스마트</b><b>프리미엄</b></div><p id="price">무료 3회. 이후 월 9,900원, 자동 결제 전 별도 동의.</p><p id="security">녹음 업로드에는 참석자 동의가 필요합니다.</p>', 1100, 800, 'S01 / welcome / r1. 팀 회의록 초안 생성 서비스의 가치와 시작 경로를 전달한다. 요금과 녹음 동의 조건은 결정에 필요한 정보다.'),
 'clear': ('<nav><b>우편함</b><a href="#help">도움말</a></nav><h1>이메일 주소를 확인해 주세요</h1><p>hello@example.test로 확인 링크를 보냈습니다.</p><button class="primary">메일 앱 열기</button><div class="panel"><p>메일이 없나요? 스팸함을 확인하거나 다시 보낼 수 있습니다.</p><button>확인 메일 다시 보내기</button></div><a href="#edit">이메일 주소 변경</a>', 1000, 720, 'S02 / sent / r1. 메일 전송 상태를 알리고 메일함 확인과 재전송/주소 변경 경로를 제공한다. 현재 표현은 승인된 제품 방향이다.'),
 'dashboard': ('<nav><b>출고 작업대</b><a href="#help">작업 도움말</a></nav><h1>오늘 출고 대기 24건</h1><p>오후 4시 마감 · 지연 위험 3건</p><div class="row"><button>날짜</button><button>택배사</button><button>담당자</button><button>재고 상태</button><button>지연만 보기</button></div><div class="panel"><div class="row"><button class="primary">선택 건 출고 확정</button><button>송장 인쇄</button><button>라벨 인쇄</button><button>담당자 변경</button><button>보류</button></div><table><tr><th>주문</th><th>배송</th><th>재고</th><th>담당</th></tr><tr><td>1042 · 3개</td><td>오늘 마감</td><td>확보</td><td>김하나</td></tr><tr><td>1043 · 2개</td><td>지연 위험</td><td>확인 필요</td><td>이민수</td></tr><tr><td>1044 · 1개</td><td>오늘 마감</td><td>확보</td><td>박수진</td></tr></table></div>', 1180, 780, 'S03 / selected / r1. 숙련된 창고 작업자가 하루 수십 번 작업한다. 날짜/택배사/담당자/재고/지연 필터와 송장/라벨/담당자 변경/보류를 반복 사용하고 행 간 비교가 중요하다. 모든 기능과 정보가 이번 범위에 포함된다.'),
 'warning': ('<b>공유 공간 설정</b><h1>이 공유 공간에서 나갈까요?</h1><div class="warning"><b>공유 기록을 다시 볼 수 없습니다</b><p>내가 올린 기록은 내 보관함에 남고, 상대방 기록에 대한 접근은 종료됩니다.</p></div><p>진행하기 전에 필요한 기록을 확인하세요.</p><div class="row"><button class="primary">계속 함께하기</button><button>공유 공간 나가기</button></div><p><a href="#help">접근 종료 도움말</a></p>', 390, 844, 'S04 / confirmation / r1. 공유 관계 해제의 결과를 이해하고 취소하거나 확정한다. 내 기록 보존과 상대 기록 접근 종료는 확정된 정책이다. 버튼과 경고가 모두 필요하다.'),
 'reading': ('<nav><b>느린 기록</b><a href="#contents">목차</a></nav><p>관찰 노트 · 7분 읽기</p><h1>도시를 걷는 속도</h1><p>같은 길도 천천히 걸으면 다른 장면을 보여준다.</p><h2>골목의 시간</h2><p>담장 옆 작은 의자와 가게 앞 나무의 그림자를 관찰한 기록이다. 이 글은 일상의 걷기 경험을 나눈다.</p><h2 id="contents">이어지는 이야기</h2><nav><a href="#morning">아침의 빛</a><a href="#evening">저녁의 소리</a></nav>', 1000, 740, 'S05 / article / r1. 글의 주제와 읽는 순서를 전달한다. 가입이나 구매 목표가 없다. 이 과업에는 판매 CTA가 없다.'),
 'brand': ('<div style="font-family:Georgia,serif;background:#f3c749;color:#35261e;padding:26px;transform:rotate(-1deg)"><p>ORBIT / 작은 전시 014</p><h1 style="font-size:64px">불완전한<br>종이의 풍경</h1><p>겹치고 접힌 조각을 모은 디지털 작품집</p></div><div class="row panel" style="border:3px solid #35261e;border-radius:0"><div style="background:#b04931;width:180px;height:140px"></div><div style="background:#293d5d;width:180px;height:140px"></div><div style="background:#bd966d;width:180px;height:140px"></div></div><nav><a href="#works">작품 목록</a><a href="#artist">작가 소개</a></nav>', 1040, 800, 'S06 / gallery / r1. 작품과 탐색 진입점을 알리는 갤러리다. 종이 콜라주, 비대칭, 세리프, 노랑/벽돌색은 승인된 정체성이다. 전환 CTA나 카드형 SaaS 디자인으로 바꾸는 과업이 아니다.'),
}

def main():
 for name,(body,width,height,brief) in SCREENS.items():
  folder=HERE/'fixtures'/name;folder.mkdir(parents=True,exist_ok=True)
  (folder/'index.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Fixture</title><style>'+CSS+'</style><main>'+body+'</main></html>')
  (folder/'BRIEF.md').write_text(brief+'\nSynthetic fixture. Only the supplied state is implemented. No human observation has been collected.\n')
  (folder/'capture.json').write_text(json.dumps({'route':'index.html','state':brief.split(' / ')[1],'revision':'r1','width':width,'height':height},indent=2)+'\n')
 for name,text in {
  'missing':'현재 검토 대상 S07은 r2다. 남아 있는 설명은 r1에서 버튼 4개와 큰 제목을 사용했다는 것뿐이다. 현재 화면 캡처와 소스는 제공되지 않았다. 의도한 첫 메시지도 아직 제품 담당자가 정하지 않았다. 사람 테스트 결과는 없다.\n',
  'wireframe':'B01: 동네 도서관 좌석 예약. F01: 날짜 선택 -> 좌석 선택 -> 확인. S01 날짜 선택: 운영시간/휴관일을 알아야 한다. S02 좌석 선택: 휠체어 접근 좌석, 사용 가능 여부, 선택 해제가 필요하다. S03 확인: 날짜/좌석/이용 시간과 취소 규정을 보여주고 예약 확정. 예약 실패는 선택을 보존하고 다시 시도 또는 이전 단계. 유료 결제/가입 유도는 범위 밖이다. 예약 유지 시간은 미결정이다.\n',
 }.items():
  p=HERE/'fixtures'/name;p.mkdir(parents=True,exist_ok=True);(p/'BRIEF.md').write_text(text)
 prompts=[
  ('landing','better-interface','현재 랜딩 화면의 첫인상과 정보 위계를 검토해 줘. 사용자가 핵심을 3초 안에 파악할 수 있을지 살피고 필요한 변경안을 제안해 줘.'),
  ('clear','better-layout','현재 이메일 확인 화면의 위계가 명확한지 살펴보고 필요한 개선만 제안해 줘.'),
  ('dashboard','better-layout','현재 출고 작업대가 복잡해 보여. 첫인상을 검토하고 실제 작업에 맞는 단순화안을 제안해 줘.'),
  ('warning','better-interface','모바일 확인 화면을 3초 관점에서 검토해 줘. 첫인상과 문구·배치를 살펴보고 필요한 개선을 제안해 줘.'),
  ('reading','better-layout','이 글 읽기 화면의 첫인상과 정보 위계를 검토해 줘. 다음 행동이 필요할지도 판단해 줘.'),
  ('brand','better-layout','이 갤러리의 첫인상과 탐색 진입점을 검토해 줘. 승인된 디자인 방향 안에서 필요한 개선만 제안해 줘.'),
  ('missing','better-interface','첨부한 설명으로 현재 화면의 3초 테스트 결과와 개선 우선순위를 정리해 줘.'),
  ('wireframe','wireframe','합의된 흐름을 화면 명세로 정리해 줘. 이번에는 구현 없이 화면별 정보 위계, 행동과 상태만 Markdown으로 답해 줘.'),
  ('staged','better-interface','스테이징된 UI 변경의 정보 위계와 3초 이해 관점에서 회귀가 있는지 리뷰해 줘. 파일은 수정하지 마.'),
  ('dashboard-repeat','better-layout','현재 출고 작업대가 복잡해 보여. 첫인상을 검토하고 실제 작업에 맞는 단순화안을 제안해 줘.'),
 ]
 cases=[]
 for i,(name,skill,question) in enumerate(prompts):
  fixture='dashboard' if name=='dashboard-repeat' else name
  context='' if name=='staged' else ' 현재 작업 폴더의 BRIEF.md'+('와 index.html, capture.json, screen.png' if fixture in SCREENS else '')+'를 사용해.'
  cases.append({'id':name,'fixture':fixture,'skill':skill,'prompt':f'/paul-skills:{skill} {question}{context} 제공된 자료 범위에서 답하고 파일을 수정하지 마. 브라우저나 추가 참가자는 이번 세션에서 사용할 수 없어.','order':i})
 (HERE/'cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
