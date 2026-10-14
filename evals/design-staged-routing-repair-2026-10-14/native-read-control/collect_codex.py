"""Check exact native loads and route order against frozen source arms."""
from pathlib import Path
import hashlib,json,re
import run_trials as run
HERE=run.HERE;RAW=run.RAW/'codex';OUT=HERE/'codex';ROOT=run.ROOT
CFG=run.CONFIG;USER_ONLY=set(CFG['user_only']);NAMES={p.name for p in (run.REPO/'skills/design').iterdir() if (p/'SKILL.md').exists()};AUTO=NAMES-USER_ONLY
DOMAINS={'better-accessibility','better-layout','better-writing','better-typography','better-colors','better-ui'}
def redact(value,cwd):
    if isinstance(value,str):return value.replace(cwd,'$TRIAL').replace(str(ROOT),'$EXPERIMENT').replace(str(run.REPO),'$REPO').replace(str(Path.home()),'$HOME')
    if isinstance(value,list):return [redact(x,cwd) for x in value]
    if isinstance(value,dict):return {k:redact(v,cwd) for k,v in value.items()}
    return value
def write(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False).replace('\N{EM DASH}',r'\u2014')+'\n')
def permitted_route_command(command,plugin,allowed):
    # A skill-path substring cannot excuse a chained status or repository search.
    if any(str(plugin/'skills/design'/n/'SKILL.md') in command for n in DOMAINS-allowed):return False
    if re.search(r'\bgit\s+(status|diff|ls-files|show|log)|\brg\s+--files|\bfind\s|\bpwd\b|\bls\s',command):return False
    if any(str(plugin/'skills/design'/n/'SKILL.md') in command for n in allowed):return True
    return 'memories/MEMORY.md' in command

def exact_body_observed(command,body):
    output=command.get('aggregated_output','')
    if body in output:return True
    if not re.search(r'\bgit\s+diff\s+--no-index\s+(?:--\s+)?/dev/null\s+',command.get('command','')):return False
    # Git prefixes every added line. Require the whole reconstructed file.
    reconstructed='\n'.join(line[1:] for line in output.splitlines() if line.startswith('+') and not line.startswith('+++ ')).strip()
    return reconstructed==body

def source_path_observed(commands,trace,expected,body):
    if any(str(expected) in c['command'] and exact_body_observed(c,body) for c in commands):return True
    # exec streams omit cwd; the native trace retains it. Require both cwd and
    # a relative SKILL.md read, plus the exact full body in completed output.
    for e in trace:
        payload=e.get('payload',{})
        source=payload.get('input','') if payload.get('type')=='custom_tool_call' else ''
        if re.search(r'workdir\s*:\s*[\"\']'+re.escape(str(expected.parent))+r'[\"\']',source) and re.search(r'\b(cat|sed)\b[^\n]*SKILL\.md',source):
            return any(exact_body_observed(c,body) for c in commands)
    return False

def main():
    OUT.mkdir(exist_ok=True);reviews=json.loads((HERE/'manual-review.json').read_text()) if (HERE/'manual-review.json').exists() else {};cases=list(CFG['cases'])
    cases+=[dict(CFG['cases'][i],id='baseline-staged-'+str(i+1),arm='baseline') for i in range(CFG.get('codex_baseline_repeats',0))]
    rows=[]
    for case in cases:
        name=case['id'];mp=RAW/(name+'.meta.json')
        if not mp.exists():continue
        meta=json.loads(mp.read_text());tp=RAW/(name+'.transcript.jsonl')
        if 'exit_code' not in meta or not tp.exists():continue
        plugin=Path(meta['plugin_root']);bodies={n:(plugin/'skills/design'/n/'SKILL.md').read_text().strip() for n in NAMES}
        events=run.read_events(RAW/(name+'.jsonl'));trace=run.read_events(tp);ctx=next(e['payload'] for e in trace if e.get('type')=='turn_context')
        commands=[e['item'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='command_execution']
        loaded=set();injected=[];available=set()
        for c in commands:loaded.update(n for n,b in bodies.items() if exact_body_observed(c,b))
        for e in trace:
            if e.get('type')!='response_item':continue
            payload=e.get('payload',{})
            for part in payload.get('content',[]):
                text=part.get('text','') if isinstance(part,dict) else ''
                if payload.get('role')=='developer' and '### Available skills' in text:available.update(re.findall(r'^- paul-skills:([^:\n]+): ',text,re.M))
                if payload.get('role')=='user' and text.startswith('<skill>'):
                    match=re.search(r'<path>([^<]+)</path>',text)
                    if match and str(plugin) in match[1]:
                        n=Path(match[1]).parent.name
                        assert bodies[n] in text
                        loaded.add(n);injected.append({'name':n,'file_sha256':run.digest(Path(match[1]).read_bytes()),'full_body_equal':True})
        fp=RAW/(name+'.final.md');final=fp.read_text() if fp.exists() else '';explicit=case['mode'] in {'explicit','handoff'} or case.get('entry')=='explicit'
        checks={'completed':meta['exit_code']==0 and not meta['timed_out'] and any(e.get('type')=='turn.completed' for e in events),'inputs_unchanged':meta['files_before']==meta['files_after'],'automatic_design_catalog_exact_12':available & NAMES==AUTO,'target_body_equal':case['expected'] in loaded,'no_failed_commands':all(c.get('exit_code')==0 or (c.get('exit_code')==1 and re.search(r'\bgit\s+diff\s+--no-index\s+(?:--\s+)?/dev/null\s+',c['command']) and c.get('aggregated_output','').startswith('diff --git ')) for c in commands),'correct_source_reads':all((plugin/'skills/design'/n/'SKILL.md').exists() for n in loaded)}
        checks['target_host_injected' if explicit else 'target_path_read']=case['expected'] in {x['name'] for x in injected} if explicit else source_path_observed(commands,trace,plugin/'skills/design'/case['expected']/'SKILL.md',bodies[case['expected']])
        checks['no_unauthorized_user_only_loads']=not(loaded & USER_ONLY - ({case['expected']} if explicit else set()))
        if case['mode']=='boundary':
            allowed={'better-interface'}|({case['expected']} if explicit else set())
            checks.update(router_loaded='better-interface' in loaded,correct_target_handoff=('$paul-skills:interface-review '+case.get('target','working')) in final,only_route_bodies=loaded<=allowed,no_repository_inspection=all(permitted_route_command(c['command'],plugin,allowed) for c in commands))
        if case['mode']=='implicit':checks['no_hidden_owner_redirect']='$paul-skills:interface-review' not in final
        if case['mode']=='handoff':checks.update(all_owners_loaded=DOMAINS|{'better-interface'}<=loaded,real_git_diff=any('git diff' in c['command'] for c in commands),classified_regression='Regression' in final and 'aria-label' in final)
        review=reviews.get('codex',{}).get(name,{})
        checks['semantic_review_pass']=review.get('pass') is True
        r={'case_id':name,'arm':case['arm'],'mode':case['mode'],'session_id':meta['session_id'],'model':ctx.get('model'),'effort':ctx.get('effort'),'checks':checks,'pass':all(checks.values()),'prompt':meta['prompt'],'final_response':redact(final,meta['cwd']),'automatic_design_catalog':sorted(available&NAMES),'loaded_skills':sorted(loaded),'injected_skills':injected,'loaded_file_hashes':{n:run.digest((plugin/'skills/design'/n/'SKILL.md').read_bytes()) for n in loaded},'commands':[{'command':redact(c['command'],meta['cwd']),'exit_code':c.get('exit_code'),'output_sha256':run.digest(c.get('aggregated_output','').encode())} for c in commands],'usage':[e.get('usage') for e in events if e.get('type')=='turn.completed'],'actual_billed_usd':None,'protocol_sha256':meta['protocol_sha256'],'cases_sha256':meta['cases_sha256'],'bundle_manifest_sha256':meta['bundle_manifest_sha256'],'stream_sha256':run.digest((RAW/(name+'.jsonl')).read_bytes()),'transcript_sha256':run.digest(tp.read_bytes()),'inputs_before':meta['files_before'],'inputs_after':meta['files_after'],'duration_seconds':meta['duration_seconds']}
        write(OUT/(name+'.json'),r);rows.append(r)
    summary={'planned':1,'completed':len(rows),'by_arm':{a:{'completed':sum(r['arm']==a for r in rows),'passed':sum(r['arm']==a and r['pass'] for r in rows)} for a in ['baseline','candidate']},'failures':{r['case_id']:[k for k,v in r['checks'].items() if not v] for r in rows if not r['pass']},'models':sorted({r['model'] for r in rows}),'efforts':sorted({r['effort'] for r in rows})}
    write(OUT/'summary.json',summary);print(json.dumps(summary))
if __name__=='__main__':main()
