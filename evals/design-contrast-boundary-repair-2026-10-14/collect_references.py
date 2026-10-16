"""Record completed native color-reference reads, not filename mentions."""
from pathlib import Path
import json,re
import run_trials as run
from collect_codex import exact_body_observed, trace_read_evidence, command_succeeded, write
from collect_claude import strip_line_numbers

def relative_reference_evidence(trace, path, body):
    calls={e['payload'].get('call_id'):e['payload'] for e in trace if e.get('payload',{}).get('type')=='custom_tool_call'}
    for event in trace:
        result=event.get('payload',{})
        if result.get('type')!='custom_tool_call_output':continue
        code=calls.get(result.get('call_id'),{}).get('input','')
        if not re.search(r'["\']?workdir["\']?\s*:\s*["\']'+re.escape(str(path.parent))+r'["\']',code) or path.name not in code:continue
        output=result.get('output','')
        chunks=[output] if isinstance(output,str) else [b.get('text','') for b in output if isinstance(b,dict)]
        if any(body in chunk for chunk in chunks):return {'call_id':result.get('call_id'),'resolved_relative_path':True,'output_sha256':run.digest(json.dumps(output,sort_keys=True).encode())}
    return None

def main():
    evidence={}
    for host in ['codex','claude']:
        evidence[host]={}
        for case in run.CONFIG['cases']:
            if not case['id'].startswith('normal-better-colors'):continue
            name=case['id'];base=run.RAW/host;mp=base/(name+'.meta.json');tp=base/(name+'.transcript.jsonl')
            if not mp.exists() or not tp.exists():continue
            meta=json.loads(mp.read_text());root=Path(meta['plugin_root'])/'skills/design/better-colors'
            trace=run.read_events(tp);proofs={}
            if host=='codex':
                events=run.read_events(base/(name+'.jsonl'))
                commands=[e['item'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='command_execution']
                for p in sorted(root.glob('*.md')):
                    if p.name=='SKILL.md':continue
                    body=p.read_text().strip()
                    c=next((c for c in commands if str(p) in c['command'] and command_succeeded(c) and exact_body_observed(c,body)),None)
                    proof=({'command_sha256':run.digest(c['command'].encode()),'output_sha256':run.digest(c.get('aggregated_output','').encode())} if c else (trace_read_evidence(trace,p,body) or relative_reference_evidence(trace,p,body)))
                    if proof:proofs[p.name]={'source_sha256':run.digest(p.read_bytes()),'full_body_equal':True,**proof}
            else:
                calls={};results={}
                for e in trace:
                    blocks=e.get('message',{}).get('content',[])
                    if not isinstance(blocks,list):continue
                    for b in blocks:
                        if b.get('type')=='tool_use' and b.get('name')=='Read':calls[b['id']]=b['input']
                        elif b.get('type')=='tool_result':results[b['tool_use_id']]=b
                for call_id,call in calls.items():
                    p=Path(call.get('file_path',''));result=results.get(call_id,{})
                    if p.parent!=root or p.name=='SKILL.md' or result.get('is_error') or not p.is_file():continue
                    content=result.get('content','')
                    if not isinstance(content,str):content='\n'.join(b.get('text','') for b in content if isinstance(b,dict))
                    if p.read_text().strip() in strip_line_numbers(content):
                        proofs[p.name]={'tool_use_id':call_id,'source_sha256':run.digest(p.read_bytes()),'full_body_equal':True,'output_sha256':run.digest(content.encode())}
            evidence[host][name]={'session_id':meta['session_id'],'completed_full_reads':proofs,'count':len(proofs)}
    write(run.HERE/'reference-reads.json',evidence)
    print(json.dumps({h:{c:r['count'] for c,r in rows.items()} for h,rows in evidence.items()}))
if __name__=='__main__':main()
