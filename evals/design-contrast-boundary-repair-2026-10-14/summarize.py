from pathlib import Path
import json,hashlib
E=Path(__file__).resolve().parent
P=E.parent/'design-domain-entry-repair-v4-2026-10-14'
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2).replace('\N{EM DASH}',r'\u2014')+'\n')
impact=json.loads((E/'impact-analysis.json').read_text());outcomes={};cost=0
for host in ['codex','claude']:
 rows=[json.loads(p.read_text()) for p in (E/host).glob('*.json') if p.name!='summary.json']
 outcomes[host]={'completed':len(rows),'passed':sum(r['pass'] for r in rows)}
 cost+=sum(r.get('reported_cost_usd') or 0 for r in rows)
before=json.loads((E/'global-before.json').read_text());after={}
for host,files in before.items():
 root=Path.home()/('.'+host)/'plugins/cache/paul-skills/paul-skills/0.4.1'
 after[host]={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in files}
assert before==after;write(E/'global-after.json',after)
ready=impact['carried_pass_count']==48 and all(v=={'completed':4,'passed':4} for v in outcomes.values())
write(E/'RESULTS.json',{'fresh_sessions':sum(v['completed'] for v in outcomes.values()),'fresh_outcomes':outcomes,'carried_passed_sessions':48,'release_ready':ready,'claude_reported_list_cost_usd':round(cost,7),'actual_billed_usd':None,'daily_install_unchanged':True,'global_release':'0.4.1','coverage_method':'48 unchanged dependency cases carried from candidate 8, six affected cases rerun, two new standards probes. Not a fresh full matrix.'})
print(json.dumps({'fresh':outcomes,'carried':48,'release_ready':ready}))
