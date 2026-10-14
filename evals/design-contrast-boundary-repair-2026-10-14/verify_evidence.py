"""Verify the bounded retest and unchanged-dependency evidence separately."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
E=Path(__file__).resolve().parent;R=E.parents[1];P=E.parent/'design-domain-entry-repair-v4-2026-10-14'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--write-manifest',action='store_true');parser.add_argument('--live-source',action='store_true');parser.add_argument('--live-install',action='store_true');args=parser.parse_args()
 subprocess.run(['python3',str(P/'verify_evidence.py')],check=True)
 old=read(P/'candidate-manifest.json')['files'];new=read(E/'candidate-manifest.json')['files'];assert len(new)==175
 changed=[p for p in sorted(old.keys()|new.keys()) if old.get(p)!=new.get(p)]
 assert changed==['skills/design/better-colors/contrast.md']
 for rel,digest in new.items():
  snap=E/'candidate-sources'/rel
  data=snap.read_bytes() if snap.exists() else subprocess.check_output(['git','show','paul-skills@0.4.1:'+rel],cwd=R)
  assert sha(data)==digest,rel
  if args.live_source:assert sha((R/rel).read_bytes())==digest,rel
 cat=read(E/'catalog.json');assert cat['selected']==len(cat['entries'])==44
 for row in cat['entries']:assert row['enabled'] and new[row['relative_path']]==row['file_sha256']
 assert cat==read(P/'catalog.json'),'entry catalog changed'
 impact=read(E/'impact-analysis.json');assert impact['changed_bundle_files']==changed and impact['unchanged_bundle_files']==174
 assert len(impact['rows'])==54 and impact['carried_pass_count']==48
 old_sessions=set();carried=0
 for entry in impact['rows']:
  file=E.parent/entry['source_receipt'];assert sha(file.read_bytes())==entry['receipt_sha256']
  row=read(file);assert row['session_id']==entry['session_id'];old_sessions.add(row['session_id'])
  if entry['eligible_carried_pass']:
   assert row['pass'] and not entry['read_changed_reference'] and not entry['evidence_methods'];carried+=1
  else:assert entry['read_changed_reference'] and entry['evidence_methods'] and entry['case_id'].startswith('normal-better-colors')
 assert carried==48 and len(old_sessions)==54
 cases={c['id']:c for c in read(E/'cases.json')['cases']};assert len(cases)==4
 old_cases={c['id']:c for c in read(P/'cases.json')['cases']}
 for name in cases:
  if name in old_cases:assert cases[name]==old_cases[name]
 manual=read(E/'manual-review.json');references=read(E/'reference-reads.json');sessions=set();counts={};cost=0
 for host in ['codex','claude']:
  rows=[read(p) for p in (E/host).glob('*.json') if p.name!='summary.json'];assert {r['case_id'] for r in rows}==set(cases)
  for row in rows:
   name=row['case_id'];assert row['session_id'] not in old_sessions|sessions;sessions.add(row['session_id'])
   assert row['pass']==all(row['checks'].values())
   assert row['protocol_sha256']==sha((E/'PROTOCOL.md').read_bytes()) and row['cases_sha256']==sha((E/'cases.json').read_bytes())
   assert row['bundle_manifest_sha256']==sha((E/'candidate-manifest.json').read_bytes())
   assert row['prompt']==cases[name]['prompt']
   review=manual['codex' if host=='codex' else 'cases'][name]
   assert review['response_sha256']==sha(row['final_response'].encode()) and review['pass']==row['checks']['semantic_review_pass']
   loads=row.get('loaded_file_hashes',{b['name']:b['file_sha256'] for b in row.get('full_body_loads',[])})
   for skill,digest in loads.items():assert new['skills/design/'+skill+'/SKILL.md']==digest
   record=references[host][name];assert record['session_id']==row['session_id'] and record['count']==len(record['completed_full_reads'])
   proof=record['completed_full_reads'].get('contrast.md')
   if proof:assert proof['full_body_equal'] and proof['source_sha256']==new[changed[0]]
   cost+=row.get('reported_cost_usd') or 0
  counts[host]={'completed':len(rows),'passed':sum(r['pass'] for r in rows)}
  assert read(E/host/'summary.json')['by_arm']['candidate']==counts[host]
 results=read(E/'RESULTS.json');assert results['fresh_outcomes']==counts and results['fresh_sessions']==8 and results['carried_passed_sessions']==48
 assert results['release_ready']==all(v=={'completed':4,'passed':4} for v in counts.values())
 assert results['claude_reported_list_cost_usd']==round(cost,7)
 before=read(E/'global-before.json');assert before==read(E/'global-after.json')==read(P/'global-after.json')
 if args.live_install:
  for host,files in before.items():
   for rel,digest in files.items():assert sha((Path.home()/('.'+host)/'plugins/cache/paul-skills/paul-skills/0.4.1'/rel).read_bytes())==digest
 files={str(p.relative_to(E)):sha(p.read_bytes()) for p in sorted(E.rglob('*')) if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
 for rel in files:
  text=(E/rel).read_text();assert '\N{EM DASH}' not in text,rel
  assert not re.search(r'/Users/[A-Za-z0-9_-]+/|sk-ant-[a-z0-9_-]{10,}|gh[pousr]_[A-Za-z0-9]{20,}',text),rel
 if args.write_manifest:(E/'MANIFEST.json').write_text(json.dumps({'files':files},indent=2)+'\n')
 assert read(E/'MANIFEST.json')['files']==files
 print(json.dumps({'integrity':'pass','fresh_outcomes':counts,'carried_passes':48,'files':len(files),'daily_install_unchanged':True}))
if __name__=='__main__':main()
