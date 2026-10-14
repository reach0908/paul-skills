from pathlib import Path
import json,hashlib,subprocess,importlib.util
E=Path(__file__).resolve().parent;R=E.parents[1];RAW=R/'.scratch/design-domain-entry-repair-20261014'
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2).replace('\N{EM DASH}',r'\u2014')+'\n')
facts={};outcomes={};cost=0
for host in ['codex','claude']:
 facts[host]={}
 for p in sorted((RAW/host).glob('*.meta.json')):
  m=json.loads(p.read_text());cwd=Path(m['cwd'])
  if not (cwd/'.git').exists():continue
  def git(*args):return subprocess.check_output(['git',*args],cwd=cwd,text=True).strip()
  fact={'main':git('rev-parse','main'),'head':git('rev-parse','HEAD'),'main_lacks_name':'aria-label' not in git('show','main:src/Panel.html'),'head_has_name':'aria-label' in git('show','HEAD:src/Panel.html'),'index_lacks_name':'aria-label' not in git('show',':src/Panel.html'),'working_has_name':'aria-label' in (cwd/'src/Panel.html').read_text(),'index_diff_files':git('diff','--cached','HEAD','--name-only').splitlines(),'working_diff_files':git('diff','HEAD','--name-only').splitlines(),'untracked':git('ls-files','--others','--exclude-standard').splitlines()}
  facts[host][m['case_id']]=fact
 rows=[json.loads(p.read_text()) for p in (E/host).glob('*.json') if p.name!='summary.json']
 outcomes[host]={'completed':len(rows),'passed':sum(r['pass'] for r in rows)}
 cost+=sum(r.get('reported_cost_usd') or 0 for r in rows)
write(E/'fixture-facts.json',facts)
before=json.loads((E/'global-before.json').read_text());after={}
for host,files in before.items():
 root=Path.home()/('.'+host)/'plugins/cache/paul-skills/paul-skills/0.4.1'
 after[host]={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in files}
assert before==after;write(E/'global-after.json',after)
write(E/'RESULTS.json',{'planned_sessions':54,'unique_sessions':sum(c['completed'] for c in outcomes.values()),'outcomes':outcomes,'claude_reported_list_cost_usd':round(cost,7),'actual_billed_usd':None,'release_ready':all(c=={'completed':27,'passed':27} for c in outcomes.values()),'global_release':'0.4.1','daily_install_unchanged':True})
print(json.dumps(outcomes))
