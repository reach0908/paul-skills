"""Reuse pinned native receipt collectors; bind manual semantics to response hashes."""
from pathlib import Path
import importlib.util, json, sys
import run_trials as run
BASE=run.REPO/'evals/design-routing-0.4.2-release-2026-10-14'
sys.path.append(str(BASE))
def load(name):
    spec=importlib.util.spec_from_file_location(name,BASE/(name+'.py'));m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
cc=load('collect_codex');cl=load('collect_claude')
def review_matches(response,review):return bool(review.get('pass') is True and review.get('response_sha256')==run.digest(response.encode()) and review.get('reason'))
def main():
    cc.main();reviews=json.loads((run.HERE/'manual-review.json').read_text()) if (run.HERE/'manual-review.json').exists() else {}
    summaries={}
    for host in ['codex','claude']:
        out=run.HERE/host;out.mkdir(exist_ok=True);rows=[]
        for case in run.CONFIG['cases']:
            path=out/(case['id']+'.json')
            if host=='claude':
                r=cl.collect_case(case)
                if not r:continue
                r['checks'].pop('daily_global_install',None)
                meta=json.loads((run.RAW/host/(case['id']+'.meta.json')).read_text())
                r['checks']['isolated_plugin_override']='--plugin-dir' in meta['command'] and meta['uses_daily_global_install'] is False
            else:
                if not path.exists():continue
                r=json.loads(path.read_text())
                r['checks'].pop('daily_global_install',None)
                meta=json.loads((run.RAW/host/(case['id']+'.meta.json')).read_text())
                r['checks']['isolated_plugin_install']=meta.get('codex_home_override') is True and meta['uses_daily_global_install'] is False
            review=reviews.get('codex' if host=='codex' else 'cases',{}).get(case['id'],{})
            r['response_sha256']=run.digest(r['final_response'].encode())
            r['checks']['semantic_review_pass']=review_matches(r['final_response'],review)
            if case['mode']!='boundary':
                meta=json.loads((run.RAW/host/(case['id']+'.meta.json')).read_text());trace=run.read_events(run.RAW/host/(case['id']+'.transcript.jsonl'))
                root=Path(meta['plugin_root'])/'skills/design/better-colors';p=root/'contrast.md';body=p.read_text().strip()
                if host=='codex':
                    proof=cc.trace_read_evidence(trace,p,body)
                    if not proof:
                        events=run.read_events(run.RAW/host/(case['id']+'.jsonl'))
                        cmds=[e['item'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='command_execution']
                        c=next((c for c in cmds if str(p) in c['command'] and cc.command_succeeded(c) and cc.exact_body_observed(c,body)),None)
                        if c:proof={'output_sha256':run.digest(c.get('aggregated_output','').encode()),'full_body_equal':True}
                else:
                    calls={};results={}
                    for e in trace:
                        blocks=e.get('message',{}).get('content',[])
                        if not isinstance(blocks,list):continue
                        for b in blocks:
                            if b.get('type')=='tool_use' and b.get('name')=='Read':calls[b['id']]=b['input']
                            elif b.get('type')=='tool_result':results[b['tool_use_id']]=b
                    proof=None
                    for cid,inp in calls.items():
                        result=results.get(cid,{});value=result.get('content','')
                        if not isinstance(value,str):value='\n'.join(b.get('text','') for b in value if isinstance(b,dict))
                        if inp.get('file_path')==str(p) and not result.get('is_error') and body in cl.strip_line_numbers(value):proof={'call_id':cid,'output_sha256':run.digest(value.encode()),'full_body_equal':True}
                r['contrast_reference']=dict(proof or {},source_sha256=run.digest(p.read_bytes()),full_body_equal=bool(proof))
                if case['id'].endswith('-resolved'):r['checks']['contrast_reference_fully_read']=bool(proof)
            r['pass']=all(r['checks'].values());cc.write(path,r);rows.append(r)
        summaries[host]={'planned':len(run.CONFIG['cases']),'completed':len(rows),'by_arm':{a:{'completed':sum(r['arm']==a for r in rows),'passed':sum(r['arm']==a and r['pass'] for r in rows)} for a in ['baseline','candidate']},'failures':{r['case_id']:[k for k,v in r['checks'].items() if not v] for r in rows if not r['pass']},'cost_usd':sum(r.get('reported_cost_usd') or 0 for r in rows) if host=='claude' else None}
        cc.write(out/'summary.json',summaries[host])
    cc.write(run.HERE/'RESULTS.json',summaries);print(json.dumps(summaries))
if __name__=='__main__':main()
