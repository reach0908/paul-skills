"""Summarize already-recorded browser and handoff evidence without new model runs."""
from pathlib import Path
import hashlib,json,struct
E=Path(__file__).resolve().parents[1];R=E.parents[1]
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=read(E/'prepared.json');runs=read(E/'run-integrity.json')['runs'];by={c['id']:c for c in p['cases']}
rows=[]
for stage in ['chain-wire','chain-build']:
 data=read(E/'evidence'/(stage+'-r1.json'))
 assert data['expectedCombinations']==data['actualCombinations']==2 and not data['pageErrors']
 for row in data['rows']:
  assert row['status']=='pass' and row['expectedFocusable']==row['observedFocusable']==14
  assert len(row['states'])==9 and len(row['captures'])==4
  assert all(s['overflow']['document']<=1 and not s['overflow']['elements'] for s in row['states'])
  expected={('chain-wire',1280):'16px',('chain-wire',320):'12px',('chain-build',1280):'24px',('chain-build',320):'16px'}[(stage,row['width'])]
  assert all(s['padding']==expected for s in row['states'])
  rows.append({'id':row['id'],'width':row['width'],'height':row['height'],'padding':expected,'stateObservations':len(row['states']),'keyboardControls':row['observedFocusable'],'capturePaths':len(row['captures'])})
wire=Path(by['chain-wire']['workspace'])/'app';build=Path(by['chain-build']['workspace'])/'app'
assert sha(wire/'index.html')==sha(build/'index.html')
assert (build/'style.css').read_text().startswith((wire/'style.css').read_text())
links=[{'stage':c['id'],**h,'sourceStillMatches':sha(Path(h['source']))==h['sha256']} for c in p['cases'] for h in c.get('handoff',[])]
assert len(links)==8 and all(h['sourceStillMatches'] for h in links)
(E/'evidence/handoff-check.json').write_text(json.dumps({'status':'pass','stages':4,'transferredFileInstances':8,'inputHashes':links,'htmlAndScriptByteIdentical':True,'browserCombinations':rows,'stateObservations':sum(r['stateObservations'] for r in rows),'sourceLinkLimit':'The evaluator inspected the external destination; no internal source-section transition was claimed.'},ensure_ascii=False,indent=2)+'\n')
# File counts are capture inventory, not test-case counts. Duplicates are identified.
captures=[]
for f in sorted(E.rglob('*.png')):
 raw=f.read_bytes();assert raw[:8]==b'\x89PNG\r\n\x1a\n' and len(raw)>24
 width,height=struct.unpack('>II',raw[16:24]);captures.append({'path':str(f.relative_to(E)),'sha256':sha(f),'bytes':len(raw),'width':width,'height':height})
(E/'evidence/captures.json').write_text(json.dumps({'paths':len(captures),'uniqueImages':len({c['sha256'] for c in captures}),'captures':captures},ensure_ascii=False,indent=2)+'\n')
summary={'completedContexts':len(runs),'qualityContexts':sum(r['kind']=='quality' for r in runs),'explicitContexts':sum(r['kind']=='explicit' for r in runs),'negativeContexts':sum(r['kind']=='negative' for r in runs),'chainContexts':sum(r['kind']=='chain' for r in runs),'capturePaths':len(captures),'uniqueImages':len({c['sha256'] for c in captures}),'allExitedZero':all(r['receipt']['exitCode']==0 for r in runs),'historicalBoundaryFailureCount':1,'laterNegativeRetests':2,'model':'gpt-5.6-sol','effort':'xhigh','billingCost':None,'efficiencyComparison':'not measured'}
(E/'evidence/summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
