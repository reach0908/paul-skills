"""Check artifact integrity separately from model or semantic success."""
from pathlib import Path
import hashlib,json
from collect import HERE

def sha(data):return hashlib.sha256(data).hexdigest()
def checked_response(receipt,root):
 path=root/receipt['response']
 assert path.resolve().is_relative_to(root.resolve()),'Response path escaped evidence root'
 assert sha(path.read_bytes())==receipt['response_sha256'],'Response changed after collection'
 return receipt['response_sha256']
def check_review(receipt,review):
 assert receipt['response_sha256']==review['response_sha256'],'Semantic judgment is stale'
 assert review['status'] in ['reviewed','not_assessed']
 if not receipt['completed']:assert review['status']=='not_assessed','Incomplete trial counted as judged completion'
 if review['status']=='reviewed':assert review['evidence'] and review['criteria'],'Missing review evidence'

def main():
 frozen=json.loads((HERE/'freeze.json').read_text())
 assert sha((HERE/'PROTOCOL.md').read_bytes())==frozen['protocol']
 assert sha((HERE/'cases.json').read_bytes())==frozen['cases']
 assert sha((HERE/'run_trials.py').read_bytes())==frozen['runner']
 actual={str(p.relative_to(HERE/'fixtures')):sha(p.read_bytes()) for p in sorted((HERE/'fixtures').rglob('*')) if p.is_file()}
 assert actual==frozen['fixtures'],'Input artifact changed'
 changed={p for p in set(frozen['arms']['baseline'])|set(frozen['arms']['candidate']) if frozen['arms']['baseline'].get(p)!=frozen['arms']['candidate'].get(p)}
 expected={'skills/design/wireframe/SKILL.md','skills/design/better-layout/SKILL.md','skills/design/better-layout/first-impression.md','skills/design/better-interface/audit-procedure.md','skills/design/better-interface/review-format.md'}
 assert changed==expected,'Behavioral change scope drift'
 repo=HERE.parents[1]
 for path,value in frozen['arms']['candidate'].items():assert sha((repo/path).read_bytes())==value, f'Candidate no longer equals tested source: {path}'
 reviews=json.loads((HERE/'manual-review.json').read_text())
 receipts=[json.loads(p.read_text()) for p in sorted((HERE/'receipts').glob('*.json'))]
 key=lambda r:(r['phase']+'-' if r['phase']!='initial' else '')+r['arm']+'-'+r['case_id']
 ids={key(r) for r in receipts}
 assert len(ids)==len(receipts),'Trial identity mismatch'
 assert set(reviews)==ids,'Review coverage mismatch'
 for r in receipts:
  checked_response(r,HERE);check_review(r,reviews[key(r)])
  freeze_path=HERE/(r['phase']+'-freeze.json' if r['phase']!='initial' else 'freeze.json')
  assert r['freeze_sha256']==sha(freeze_path.read_bytes())
  assert r['inputs_unchanged']==(r['files_before']==r['files_after'])
 controlled=json.loads((HERE/'controlled-freeze.json').read_text())
 for key_name,file_name in [('protocol','CONTROLLED-PROTOCOL.md'),('cases','controlled-cases.json'),('runner','run_controlled.py')]:assert controlled[key_name]==sha((HERE/file_name).read_bytes())
 assert controlled['fixtures']==frozen['fixtures'] and controlled['arms']==frozen['arms']
 bounded=json.loads((HERE/'bounded-freeze.json').read_text())
 for key_name,file_name in [('protocol','BOUNDED-PROTOCOL.md'),('cases','bounded-cases.json'),('runner','run_bounded.py')]:assert bounded[key_name]==sha((HERE/file_name).read_bytes())
 assert bounded['fixtures']==frozen['fixtures'] and bounded['arms']==frozen['arms']
 paired={};unstarted={}
 for phase,stop_file,case_file in [('initial','initial-stop.json','cases.json'),('controlled','controlled-stop.json','controlled-cases.json'),('bounded','bounded-stop.json','bounded-cases.json')]:
  stop=json.loads((HERE/stop_file).read_text()) if (HERE/stop_file).exists() else {}
  unstarted[phase]=stop.get('unstarted_cases',[]);paired[phase]=[]
  expected_cases={c['id'] for c in json.loads((HERE/case_file).read_text())}-set(unstarted[phase])
  actual_cases={r['case_id'] for r in receipts if r['phase']==phase}
  assert actual_cases==expected_cases, 'Missing attempts without a stop record'
  for case_id in expected_cases:
   pair=[r for r in receipts if r['case_id']==case_id and r['phase']==phase];assert len(pair)==2
   assert pair[0]['prompt']==pair[1]['prompt'] and pair[0]['files_before']==pair[1]['files_before']
   assert pair[0]['actual_model']==pair[1]['actual_model'] and pair[0]['host_version']==pair[1]['host_version']
   if all(r['completed'] and r['inputs_unchanged'] and r['plugin_path_matches'] for r in pair):paired[phase].append(case_id)
  paired[phase].sort()
 reserved=sum(r['cost_usd'] if r['cost_usd'] is not None else ({'initial':1.0,'controlled':0.75,'bounded':0.4}[r['phase']]) for r in receipts)
 assert reserved<=12, 'Combined budget ceiling exceeded'
 result={'integrity_pass':True,'attempts':len(receipts),'completed':sum(r['completed'] for r in receipts),'valid_pairs_by_phase':paired,'unstarted_cases_by_phase':unstarted,'reported_cost_usd':sum(r['cost_usd'] for r in receipts if r['cost_usd'] is not None),'cost_unknown_attempts':[key(r) for r in receipts if r['cost_usd'] is None],'cost_with_timeout_reserves_usd':reserved,'human_three_second_test':'not_run','automatic_discovery':'not_run','implementation_retest':'not_run','semantic_success_is_separate':True}
 (HERE/'VERIFICATION.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
