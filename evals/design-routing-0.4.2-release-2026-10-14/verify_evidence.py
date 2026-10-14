"""Verify immutable release, installed-source receipts, and fresh session outcomes."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def main():
 p=argparse.ArgumentParser();p.add_argument('--write-manifest',action='store_true');p.add_argument('--live-install',action='store_true');args=p.parse_args()
 release=read(HERE/'release.json');tag=release['tag'];commit=git('rev-parse',tag+'^{}').decode().strip()
 assert commit==release['release_commit']==release['version_pr']['mergeCommit']['oid']==release['release_workflow']['headSha']
 assert release['release_workflow']['conclusion']=='success' and release['source_pr']['state']==release['version_pr']['state']=='MERGED'
 install=read(HERE/'installation.json');files=install['files'];assert len(files)==175
 assert install['release_commit']==commit and read(HERE/'candidate-manifest.json')['files']==files
 prior=read(HERE.parent/'design-contrast-reference-proof-2026-10-14/candidate-manifest.json')['files']
 for rel,digest in files.items():
  assert sha(git('show',tag+':'+rel))==digest,rel
  if rel!='.claude-plugin/plugin.json':assert prior[rel]==digest,rel
 for host,data in install['hosts'].items():
  assert data['version']=='0.4.2' and data['enabled'] and data['scope']=='user' and data['skill_file_count']==174
  if args.live_install:
   root=Path(data['cache'].replace('$HOME',str(Path.home())))
   for rel,digest in files.items():assert sha((root/rel).read_bytes())==digest,(host,rel)
 amendment=read(HERE/'grader-amendment.json')
 for rel,digest in read(HERE/'harness-manifest.json')['files'].items():
  if rel in amendment['before']:
   assert digest==amendment['before'][rel]==sha((HERE/'initial-grader'/rel).read_bytes())
   assert sha((HERE/rel).read_bytes())==amendment['after'][rel]
  else:assert sha((HERE/rel).read_bytes())==digest,rel
 for rel,digest in amendment['after'].items():assert sha((HERE/rel).read_bytes())==digest,rel
 cases={c['id']:c for c in read(HERE/'cases.json')['cases']};assert len(cases)==18
 manual=read(HERE/'manual-review.json');refs=read(HERE/'reference-reads.json');sessions=set();counts={};cost=0;rows_by_host={}
 for host in ['codex','claude']:
  rows=[read(p) for p in (HERE/host).glob('*.json') if p.name!='summary.json'];assert {r['case_id'] for r in rows}==set(cases)
  rows_by_host[host]=rows
  for r in rows:
   name=r['case_id'];assert r['session_id'] not in sessions;sessions.add(r['session_id'])
   assert r['protocol_sha256']==sha((HERE/'PROTOCOL.md').read_bytes()) and r['cases_sha256']==sha((HERE/'cases.json').read_bytes())
   assert r['bundle_manifest_sha256']==sha((HERE/'candidate-manifest.json').read_bytes())
   expected_prompt=cases[name]['prompt']
   if host=='codex':expected_prompt=expected_prompt.replace('/paul-skills:','$paul-skills:')
   elif cases[name]['mode']=='handoff':expected_prompt+='\n파일과 참조 문서는 Read/Glob/Grep으로 읽고, Git 조회는 허용된 읽기 전용 git 하위 명령을 각각 하나의 Bash 호출로 실행해. 셸 연결이나 파이프, cd, git -C 없이 현재 폴더에서 조회해.'
   assert r['prompt']==expected_prompt
   if host=='claude':assert r['host_protocol_sha256']==sha((HERE/'CLAUDE-PROTOCOL.md').read_bytes())
   assert r['pass']==all(r['checks'].values()) and r['checks']['daily_global_install']
   m=manual['codex' if host=='codex' else 'cases'][name]
   assert m['response_sha256']==sha(r['final_response'].encode()) and m['pass']==r['checks']['semantic_review_pass']
   hashes=r.get('loaded_file_hashes',{b['name']:b['file_sha256'] for b in r.get('full_body_loads',[])})
   for skill,digest in hashes.items():assert files['skills/design/'+skill+'/SKILL.md']==digest
   cost+=r.get('reported_cost_usd') or 0
  proof=refs[host]['normal-better-colors-thresholds']['completed_full_reads']['contrast.md']
  assert proof['full_body_equal'] and proof['source_sha256']==files['skills/design/better-colors/contrast.md']
  counts[host]={'completed':len(rows),'passed':sum(r['pass'] for r in rows)}
  assert read(HERE/host/'summary.json')['by_arm']['candidate']==counts[host]
 result=read(HERE/'RESULTS.json');assert result['outcomes']==counts and result['unique_sessions']==len(sessions)==36
 assert result['claude_reported_list_cost_usd']==round(cost,7)
 assert result['full_sample_passed']==all(c=={'completed':18,'passed':18} for c in counts.values())
 all_rows=[r for rows in rows_by_host.values() for r in rows]
 assert result['source_application_verified']==all(all(v for k,v in r['checks'].items() if k!='semantic_review_pass') for r in all_rows)
 assert result['failures']=={h:{r['case_id']:[k for k,v in r['checks'].items() if not v] for r in rows if not r['pass']} for h,rows in rows_by_host.items()}
 catalog=read(HERE/'catalog.json');assert catalog['all_promoted']==44 and catalog['design_total']==len(catalog['design'])==17
 inventory={str(p.relative_to(HERE)):sha(p.read_bytes()) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
 for rel in inventory:
  content=(HERE/rel).read_text();assert '\N{EM DASH}' not in content,rel
  assert not re.search(r'/Users/[A-Za-z0-9_-]+/|sk-ant-[a-z0-9_-]{10,}|gh[pousr]_[A-Za-z0-9]{20,}',content),rel
 if args.write_manifest:(HERE/'MANIFEST.json').write_text(json.dumps({'files':inventory},indent=2)+'\n')
 assert read(HERE/'MANIFEST.json')['files']==inventory
 print(json.dumps({'integrity':'pass','outcomes':counts,'unique_sessions':len(sessions),'full_sample_passed':result['full_sample_passed'],'source_application_verified':result['source_application_verified'],'promoted_files_per_host':len(files),'receipt_files':len(inventory)}))
if __name__=='__main__':main()
