"""Check final dependency-scoped release evidence without rewriting prior failures."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
E=Path(__file__).resolve().parent;R=E.parents[1];P=E.parent/'design-contrast-boundary-repair-2026-10-14'
def read(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--write-manifest',action='store_true');parser.add_argument('--live-source',action='store_true');parser.add_argument('--live-install',action='store_true');args=parser.parse_args()
 subprocess.run(['python3',str(P/'verify_evidence.py')],check=True)
 manifest=read(E/'candidate-manifest.json')['files'];assert manifest==read(P/'candidate-manifest.json')['files'] and len(manifest)==175
 for rel,digest in manifest.items():
  snap=E/'candidate-sources'/rel;data=snap.read_bytes() if snap.exists() else subprocess.check_output(['git','show','paul-skills@0.4.1:'+rel],cwd=R)
  assert sha(data)==digest,rel
  if args.live_source:assert sha((R/rel).read_bytes())==digest,rel
 assert read(E/'catalog.json')==read(P/'catalog.json')
 cases={c['id']:c for c in read(E/'cases.json')['cases']};assert len(cases)==2 and all(c['mode']=='explicit' for c in cases.values())
 manual=read(E/'manual-review.json');refs=read(E/'reference-reads.json');sessions=set();counts={};cost=0;prior_sessions=set()
 for folder in [P,E.parent/'design-domain-entry-repair-v4-2026-10-14']:
  for host in ['codex','claude']:
   for f in (folder/host).glob('*.json'):
    if f.name!='summary.json':prior_sessions.add(read(f)['session_id'])
 for host in ['codex','claude']:
  rows=[read(p) for p in (E/host).glob('*.json') if p.name!='summary.json'];assert {r['case_id'] for r in rows}==set(cases)
  for row in rows:
   name=row['case_id'];assert row['session_id'] not in sessions|prior_sessions;sessions.add(row['session_id'])
   assert row['pass']==all(row['checks'].values())
   assert row['protocol_sha256']==sha((E/'PROTOCOL.md').read_bytes()) and row['cases_sha256']==sha((E/'cases.json').read_bytes())
   assert row['bundle_manifest_sha256']==sha((E/'candidate-manifest.json').read_bytes())
   prompt=cases[name]['prompt'].replace('/paul-skills:','$paul-skills:') if host=='codex' else cases[name]['prompt'];assert row['prompt']==prompt
   review=manual['codex' if host=='codex' else 'cases'][name];assert review['response_sha256']==sha(row['final_response'].encode()) and review['pass']==row['checks']['semantic_review_pass']
   record=refs[host][name];assert record['session_id']==row['session_id'] and record['count']==len(record['completed_full_reads'])
   proof=record['completed_full_reads']['contrast.md'];assert proof['full_body_equal'] and proof['source_sha256']==manifest['skills/design/better-colors/contrast.md']
   loads=row.get('loaded_file_hashes',{b['name']:b['file_sha256'] for b in row.get('full_body_loads',[])})
   assert loads['better-colors']==manifest['skills/design/better-colors/SKILL.md']
   for skill,digest in loads.items():assert digest==manifest['skills/design/'+skill+'/SKILL.md']
   cost+=row.get('reported_cost_usd') or 0
  counts[host]={'completed':len(rows),'passed':sum(r['pass'] for r in rows)};assert read(E/host/'summary.json')['by_arm']['candidate']==counts[host]
  for name in ['normal-better-colors','normal-better-colors-2','normal-better-colors-3']:assert read(P/host/(name+'.json'))['pass']
 assert read(P/'impact-analysis.json')['carried_pass_count']==48
 results=read(E/'RESULTS.json');assert results['fresh_outcomes']==counts and results['fresh_sessions']==4
 assert results['release_ready']==all(v=={'completed':2,'passed':2} for v in counts.values())
 assert results['unchanged_carried_passes']==48 and results['same_source_normal_entry_passes']==6
 assert results['prior_automatic_probe_failure_preserved'] and not read(P/'RESULTS.json')['release_ready']
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
 print(json.dumps({'integrity':'pass','fresh_outcomes':counts,'same_source_normal_entries':6,'unchanged_carried_passes':48,'release_ready':results['release_ready'],'files':len(files)}))
if __name__=='__main__':main()
