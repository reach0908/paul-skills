"""Validate the targeted repair against the working tree or an explicit source ref."""
from pathlib import Path
import argparse, hashlib, io, json, subprocess, tarfile
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
def tree(ref):
 data=subprocess.check_output(['git','archive',ref,'skills','.claude-plugin'],cwd=REPO)
 with tarfile.open(fileobj=io.BytesIO(data)) as archive:
  return {m.name:sha(archive.extractfile(m).read()) for m in archive if m.isfile()}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--source-ref');args=parser.parse_args()
 f=json.loads((HERE/'freeze.json').read_text())
 for k,p in [('protocol','PROTOCOL.md'),('cases','cases.json'),('runner','run_trials.py')]:assert f[k]==sha((HERE/p).read_bytes())
 assert f['arms']['baseline']==tree(f['base'])
 current=tree(args.source_ref) if args.source_ref else {p:sha((REPO/p).read_bytes()) for p in f['arms']['candidate']}
 assert f['arms']['candidate']==current
 changed={p for p in set(f['arms']['baseline'])|set(current) if f['arms']['baseline'].get(p)!=current.get(p)}
 assert changed=={'skills/design/wireframe/SKILL.md'}
 actual={str(p.relative_to(HERE/'fixtures')):sha(p.read_bytes()) for p in (HERE/'fixtures').rglob('*') if p.is_file()}
 assert actual==f['fixtures']
 rows=[json.loads(p.read_text()) for p in sorted((HERE/'receipts').glob('*.json'))]
 reviews=json.loads((HERE/'manual-review.json').read_text())
 assert len(rows)==2 and {r['arm'] for r in rows}=={'baseline','candidate'}
 expected={p.removeprefix('brand/'):h for p,h in actual.items()}
 for r in rows:
  assert r['files_before']==r['files_after']==expected
  assert r['completed'] and r['plugin_path_matches']
  assert r['freeze_sha256']==sha((HERE/'freeze.json').read_bytes())
  assert sha((HERE/r['response']).read_bytes())==r['response_sha256']==reviews[r['arm']]['response_sha256']
  calls=r['tool_calls'];owner=[i for i,c in enumerate(calls) if c['name']=='Skill' and c['input'].get('skill','').endswith(':better-layout') and c['result_received'] and not c['is_error']]
  references=[i for i,c in enumerate(calls) if c['name']=='Read' and c['input'].get('file_path','').endswith('/first-impression.md')]
  actual_invocation=bool(owner and references and min(owner)<min(references))
  assert reviews[r['arm']]['owner_invocation']==actual_invocation
  assert r['first_impression_fully_read']
 for k in ['prompt','actual_model','host_version','requested_effort']:assert rows[0][k]==rows[1][k]
 result={'integrity_pass':True,'native_completed':2,'paired_cases':1,'baseline_owner_invocation':reviews['baseline']['owner_invocation'],'candidate_owner_invocation':reviews['candidate']['owner_invocation'],'cost_usd':sum(r['cost_usd'] for r in rows),'human_three_second':'not_run'}
 assert result['cost_usd']<=3
 (HERE/'VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
