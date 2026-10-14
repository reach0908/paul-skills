"""Collect Codex host catalogs and exact installed body loads."""
from pathlib import Path
import hashlib,json,re
import run_trials as common
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
RAW=REPO/'.scratch/design-routing-patch-release-20261014/codex-compatible';OUT=HERE/'codex'
HOME=Path.home();CACHE=HOME/'.codex/plugins/cache/paul-skills/paul-skills/0.4.1'
CONFIG=json.loads((HERE/'cases.json').read_text());USER_ONLY=set(CONFIG['user_only'])
NAMES={p.name for p in (CACHE/'skills/design').iterdir() if (p/'SKILL.md').exists()};AUTO=NAMES-USER_ONLY
BODIES={n:(CACHE/'skills/design'/n/'SKILL.md').read_text().strip() for n in NAMES}

def redact(value,cwd):
    if isinstance(value,str):return value.replace(cwd,'$TRIAL').replace(str(REPO),'$REPO').replace(str(HOME),'$HOME')
    if isinstance(value,list):return [redact(v,cwd) for v in value]
    if isinstance(value,dict):return {k:redact(v,cwd) for k,v in value.items()}
    return value

def write(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False).replace('\N{EM DASH}',r'\u2014')+'\n')

def main():
    OUT.mkdir(exist_ok=True);rows=[]
    manual=json.loads((HERE/'manual-review.json').read_text()) if (HERE/'manual-review.json').exists() else {}
    for case in CONFIG['cases']:
        name=case['id'];mp=RAW/(name+'.meta.json')
        if not mp.exists():continue
        meta=json.loads(mp.read_text())
        if 'exit_code' not in meta:continue
        ef=RAW/(name+'.jsonl');events=common.read_events(ef)
        tid=next((e['thread_id'] for e in events if e.get('type')=='thread.started'),None)
        traces=list((HOME/'.codex/sessions').rglob('*'+str(tid)+'.jsonl'))
        if len(traces)!=1:raise RuntimeError('Missing native trace '+str(tid))
        trace=common.read_events(traces[0]);ctx=next(e['payload'] for e in trace if e.get('type')=='turn_context')
        commands=[e['item'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='command_execution']
        loaded=set();injected=[];available=set()
        for c in commands:loaded.update(n for n,b in BODIES.items() if b in c.get('aggregated_output',''))
        for e in trace:
            if e.get('type')!='response_item':continue
            p=e.get('payload',{})
            for part in p.get('content',[]):
                text=part.get('text','') if isinstance(part,dict) else ''
                if p.get('role')=='developer' and '### Available skills' in text:
                    available.update(re.findall(r'^- paul-skills:([^:\n]+): ',text,re.M))
                if p.get('role')=='user' and text.startswith('<skill>'):
                    match=re.search(r'<path>([^<]+)</path>',text)
                    if match and str(CACHE) in match[1]:
                        n=Path(match[1]).parent.name
                        assert BODIES[n] in text
                        loaded.add(n);injected.append({'name':n,'file_sha256':common.digest(Path(match[1]).read_bytes()),'full_body_equal':True})
        final=(RAW/(name+'.final.md')).read_text() if (RAW/(name+'.final.md')).exists() else ''
        explicit=case['mode']=='explicit' or case.get('entry')=='explicit'
        checks={'completed':meta['exit_code']==0 and not meta['timed_out'] and any(e.get('type')=='turn.completed' for e in events),'inputs_unchanged':meta['before']==meta['after'],'automatic_design_catalog_exact_12':available & NAMES==AUTO,'target_body_equal':case['expected'] in loaded,'no_failed_commands':all(c.get('exit_code')==0 for c in commands),'neutral_working_directory':bool(re.fullmatch('case_[0-9]{3}',Path(meta['cwd']).name))}
        if explicit:checks['exact_target_host_injected']=case['expected'] in {x['name'] for x in injected}
        else:checks['installed_target_path_read']=any(str(CACHE/'skills/design'/case['expected']/'SKILL.md') in c['command'] for c in commands)
        checks['no_unauthorized_hidden_loads']=not(loaded & USER_ONLY - ({case['expected']} if explicit else set()))
        if case['mode']=='boundary':
            checks['correct_target_handoff']='$paul-skills:interface-review '+case.get('target','working') in final
            checks['no_domain_loads']=not(loaded-{'better-interface'})
            checks['no_product_file_inspection']=all(str(CACHE/'skills/design/better-interface/SKILL.md') in c['command'] for c in commands)
        if name=='repair-current-audit':checks['no_change_review_redirect']=manual.get('codex',{}).get(name,{}).get('no_change_review_redirect') is True
        checks['semantic_review_pass']=manual.get('codex',{}).get(name,{}).get('pass') is True
        r={'case_id':name,'session_id':tid,'host_version':subprocess_version(),'model':ctx.get('model'),'effort':ctx.get('effort'),'installed_version':'0.4.1','checks':checks,'pass':all(checks.values()),'prompt':meta['prompt'],'final_response':redact(final,meta['cwd']),'automatic_design_catalog':sorted(available&NAMES),'loaded_skills':sorted(loaded),'injected_skills':injected,'loaded_file_hashes':{n:common.digest((CACHE/'skills/design'/n/'SKILL.md').read_bytes()) for n in loaded},'commands':[{'command':redact(c['command'],meta['cwd']),'exit_code':c.get('exit_code'),'output_sha256':common.digest(c.get('aggregated_output','').encode())} for c in commands],'usage':[e.get('usage') for e in events if e.get('type')=='turn.completed'],'actual_billed_usd':None,'protocol_sha256':meta['protocol_sha256'],'cases_sha256':meta['cases_sha256'],'stream_sha256':common.digest(ef.read_bytes()),'transcript_sha256':common.digest(traces[0].read_bytes()),'inputs_before':meta['before'],'inputs_after':meta['after'],'duration_seconds':meta['seconds']}
        write(OUT/(name+'.json'),r);rows.append(r)
    summary={'planned':6,'completed':len(rows),'passed':sum(r['pass'] for r in rows),'unique_sessions':len({r['session_id'] for r in rows}),'failures':{r['case_id']:[k for k,v in r['checks'].items() if not v] for r in rows if not r['pass']},'models':sorted({r['model'] for r in rows}),'efforts':sorted({r['effort'] for r in rows})}
    write(OUT/'summary.json',summary);print(json.dumps(summary))

def subprocess_version():
    import subprocess
    return subprocess.check_output(['codex','--version'],text=True).strip()

if __name__=='__main__':main()
