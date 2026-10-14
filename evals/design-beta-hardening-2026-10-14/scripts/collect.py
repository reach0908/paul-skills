from pathlib import Path
import json,hashlib,shutil,re
R=Path('/Users/jinhokim/dev/paul-skills');E=R/'evals/design-beta-hardening-2026-10-14';RAW=R/'.scratch/design-beta-hardening-20261014';T=Path('/private/tmp/paul-beta-hardening-20261014')
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prepared=json.loads((E/'prepared.json').read_text()); records=[]
sessions={}
for p in (T/'codex-home/sessions').rglob('*.jsonl'):
 events=[json.loads(s) for s in p.read_text().splitlines() if s.strip()]
 meta=next((e.get('payload',{}) for e in events if e.get('type')=='session_meta'),{})
 sessions[meta.get('id')]=(p,events)
for c in prepared['cases']:
 receipt=RAW/(c['id']+'.receipt.json')
 if not receipt.exists():continue
 d=Path(c['workspace']);dest=E/'artifacts'/c['id'];dest.mkdir(parents=True,exist_ok=True)
 changed=[rel for rel,sha in c['inputs'].items() if (d/rel).exists() and h(d/rel)!=sha]
 missing=[rel for rel in c['inputs'] if not (d/rel).exists()]
 for folder in ['app','output','input','ref']:
  if (d/folder).exists():shutil.copytree(d/folder,dest/folder,dirs_exist_ok=True)
 for f in ['PROMPT.md','TASK.md','BRIEF.md','REFERENCE.md']:
  if (d/f).exists():shutil.copy2(d/f,dest/f)
 if (RAW/(c['id']+'.final.md')).exists():shutil.copy2(RAW/(c['id']+'.final.md'),dest/'final.md')
 # Retain screenshots wherever the executor stored them, without copying caches or skill bundles.
 for f in d.rglob('*.png'):
  if '.agents' not in f.parts:
   p=dest/'captures'/f.relative_to(d);p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,p)
 events=[json.loads(s) for s in (RAW/(c['id']+'.events.jsonl')).read_text().splitlines() if s.strip()]
 tid=next((e.get('thread_id') for e in events if e.get('type')=='thread.started'),None)
 commands=[{'command':e['item'].get('command'),'exitCode':e['item'].get('exit_code'),'output':e['item'].get('aggregated_output','')} for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='command_execution']
 reads=set()
 for command in commands:reads.update(re.findall(r'^name:\s*[\"\']?([\w-]+)[\"\']?\s*$',command['output'],re.M))
 injected=[];available=[];context={};load_evidence=[]
 if tid in sessions:
  path,sev=sessions[tid]
  context=next((e.get('payload',{}) for e in sev if e.get('type')=='turn_context'),{})
  for ev in sev:
   p=ev.get('payload',{})
   if ev.get('type')!='response_item':continue
   text='\n'.join(b.get('text','') for b in p.get('content',[]) if isinstance(b,dict))
   if p.get('role')=='developer' and '### Available skills' in text:available.extend(re.findall(r'^- ([\w-]+): .+\(file: [^\n]+\)\s*$',text,re.M))
   if p.get('role')=='user' and '<skill>' in text:
    for name in re.findall(r'^name:\s*[\"\']?([\w-]+)[\"\']?\s*$',text,re.M):
     sp=d/'.agents/skills'/name/'SKILL.md';match=sp.exists() and sp.read_text().strip() in text
     injected.append(name);load_evidence.append({'name':name,'fullLocalBodyMatches':match,'bodySha256':h(sp) if sp.exists() else None})
 outputs={str(p.relative_to(dest)):h(p) for p in dest.rglob('*') if p.is_file() and p.name not in ['commands.json','progress-messages.json']}
 record={'id':c['id'],'role':c['role'],'arm':c['arm'],'kind':c['kind'],'threadId':tid,'receipt':json.loads(receipt.read_text()),'turnCompleted':any(e.get('type')=='turn.completed' for e in events),'inputChanges':changed,'inputMissing':missing,'loadedThroughCommandOutput':sorted(reads),'hostInjectedBodies':load_evidence,'loadedSkills':sorted(reads|set(injected)),'automaticallyAvailable':sorted(set(available)),'model':context.get('model'),'effort':context.get('effort'),'toolFailures':[x for x in commands if x['exitCode']!=0 or '### Error' in x['output']],'outputs':outputs,'usage':[e.get('usage') for e in events if e.get('type')=='turn.completed']}
 (dest/'commands.json').write_text(json.dumps(commands,ensure_ascii=False,indent=2)+'\n')
 (dest/'progress-messages.json').write_text(json.dumps([e['item'].get('text','') for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message'],ensure_ascii=False,indent=2)+'\n')
 records.append(record)
(E/'run-integrity.json').write_text(json.dumps({'protocolUnchanged':h(E/'PROTOCOL.md')==prepared['protocolSha256'],'completed':len(records),'runs':records},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'completed':len(records),'rows':[{'id':r['id'],'loaded':r['loadedSkills'],'changed':r['inputChanges'],'errors':len(r['toolFailures'])} for r in records]},ensure_ascii=False))
