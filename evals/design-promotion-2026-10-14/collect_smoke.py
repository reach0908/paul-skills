"""Recollect the three release smoke sessions from locally retained raw traces."""
from pathlib import Path
import hashlib,json,re
repo=Path(__file__).resolve().parents[2]
raw=repo/'.scratch/design-promotion-20261014'
out=repo/'evals/design-promotion-2026-10-14/evidence'
names=['implicit-diff-a','implicit-review','explicit-review']
domains={'better-accessibility','better-layout','better-writing','better-typography','better-colors','better-ui'}
records=[]
for name in names:
    receipt=json.loads((raw/(name+'.receipt.json')).read_text())
    events_path=raw/(name+'.events.jsonl')
    events=[json.loads(line) for line in events_path.read_text().splitlines() if line]
    tid=next(e['thread_id'] for e in events if e.get('type')=='thread.started')
    commands=[e['item'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='command_execution']
    loaded=set()
    for c in commands:
        if c.get('exit_code')==0:
            loaded.update(re.findall(r'^name:\s*["\']?((?:better-[a-z-]+|design-browser|interface-review))["\']?\s*$',c.get('aggregated_output',''),re.M))
    rollout=next((Path.home()/'.codex/sessions').rglob('*'+tid+'.jsonl'))
    initial=[json.loads(line) for line in rollout.read_text().splitlines() if line]
    context=next(e['payload'] for e in initial if e.get('type')=='turn_context')
    available=[]
    injected=[]
    for event in initial:
        p=event.get('payload',{})
        if event.get('type')=='response_item' and p.get('role')=='user':
            for part in p.get('content',[]):
                text=part.get('text','') if isinstance(part,dict) else ''
                if text.startswith('<skill>'):
                    match=re.search(r'<path>([^<]+)</path>',text)
                    if match and '/paul-skills/paul-skills/0.3.0/skills/design/' in match[1]:
                        skill_path=Path(match[1]); body=skill_path.read_text().strip()
                        assert body in text
                        skill_name=skill_path.parent.name
                        loaded.add(skill_name)
                        injected.append({'name':skill_name,'path':str(skill_path),'sha256':hashlib.sha256(skill_path.read_bytes()).hexdigest(),'contentMatchesInstalledFile':True})
        if event.get('type')=='response_item' and p.get('role')=='developer':
            text='\n'.join(c.get('text','') for c in p.get('content',[]) if isinstance(c,dict))
            if '### Available skills' in text:
                available+=re.findall(r'^- (paul-skills:[^:\n]+): ',text,re.M)
    final=(raw/(name+'.final.md')).read_text()
    checks={'completed':receipt['exitCode']==0 and any(e.get('type')=='turn.completed' for e in events),
            'sourceUnchanged':receipt['inputSha256']==receipt['outputSourceSha256'],
            'eightDesignRolesAvailable':all('paul-skills:'+s in available for s in domains|{'better-interface','design-browser'}),
            'explicitOnlyRoleHidden':'paul-skills:interface-review' not in available,
            'releasedBundleRead':any('/paul-skills/paul-skills/0.3.0/' in c['command'] for c in commands)}
    if name=='implicit-diff-a':
        checks.update(correctWorkingInvocation='$paul-skills:interface-review working' in final,onlyRoutingSkillLoaded=loaded=={'better-interface'},noChangeReview=not any(re.search(r'\bgit (?:diff|show|blame)\b|index\.html',c['command']) for c in commands),noReviewVerdict=not re.search(r'\b(?:Approve|Block|Needs improvement)\b',final))
    else:
        checks.update(sixDomainsLoaded=domains|{'better-interface'}<=loaded)
        if name=='explicit-review': checks.update(explicitRoleLoaded='interface-review' in loaded,classificationPresent='Regression' in final and ('Pre-existing' in final or '기존' in final))
    record={'case':name,'threadId':tid,'model':context['model'],'effort':context['effort'],'receipt':receipt,'automaticallyAvailablePaulSkills':available,'loadedSkills':sorted(loaded),'hostInjectedSkills':injected,'checks':checks,'final':final,'commands':[{'command':c['command'],'exitCode':c.get('exit_code'),'outputSha256':hashlib.sha256(c.get('aggregated_output','').encode()).hexdigest()} for c in commands],'rawEventsSha256':hashlib.sha256(events_path.read_bytes()).hexdigest(),'limits':'Fresh global session, not an isolated or blinded quality trial. Normal global memory and other installed capabilities remain enabled. Source-only review; no browser QA.'}
    (out/(name+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    records.append(record)
summary={'cases':len(records),'passed':sum(all(r['checks'].values()) for r in records),'distinctThreads':len({r['threadId'] for r in records}),'model':'gpt-5.6-sol','effort':'xhigh','globalInstallation':True,'qualityComparisonRepeated':False}
(out/'smoke-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary));print(json.dumps({r['case']:{k:v for k,v in r['checks'].items() if not v} for r in records}))
