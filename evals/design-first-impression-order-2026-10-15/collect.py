"""Export scoped native receipts without system prompts, private settings or image data."""
from pathlib import Path
import hashlib, json, re
from run_trials import HERE, RAW, ROOT, events

OWNERS=['better-accessibility','better-layout','better-writing','better-typography','better-colors','better-ui']
def sha(data):return hashlib.sha256(data).hexdigest()
def unwrap(value):
 for _ in range(3):
  if not isinstance(value,str):break
  try:value=json.loads(value)
  except (ValueError,TypeError):break
 return value
def numbered_lines(value):
 value=unwrap(value)
 if not isinstance(value,str):return {}
 return {int(m[1]):m[2] for line in value.splitlines() if (m:=re.match(r'^\s*(\d+)\t(.*)$',line))}
def full_read(expected,observed):
 return bool(expected.splitlines()) and all(observed.get(i)==line for i,line in enumerate(expected.splitlines(),1))
def sanitize(text,meta):
 return text.replace(meta['bundle'],'BUNDLE').replace(meta['cwd'],'FIXTURE').replace(str(ROOT),'TRIAL_ROOT')
def collect(folder):
 meta=json.loads((folder/'meta.json').read_text());rows=events(folder/'events.jsonl')
 phase='order'
 if 'exit_code' not in meta:return None
 init=next((r for r in rows if r.get('type')=='system' and r.get('subtype')=='init'),{})
 results={b.get('tool_use_id'):b for r in rows if r.get('type')=='user' and isinstance(r.get('message',{}).get('content'),list) for b in r['message']['content'] if b.get('type')=='tool_result'}
 calls=[];read_lines={};launched=[];screens=[];errors=[]
 for r in rows:
  if r.get('type')!='assistant':continue
  for b in r.get('message',{}).get('content',[]):
   if b.get('type')!='tool_use':continue
   result=results.get(b['id'],{});inp=b.get('input',{});raw=result.get('content','')
   entry={'name':b['name'],'input':json.loads(sanitize(json.dumps(inp,ensure_ascii=False),meta)),'result_received':bool(result),'is_error':bool(result.get('is_error')),'result_sha256':sha(json.dumps(raw,ensure_ascii=False,sort_keys=True).encode())}
   if result.get('is_error'):errors.append(entry)
   if b['name']=='Skill' and result and not result.get('is_error'):launched.append(inp.get('skill','').split(':')[-1])
   if b['name']=='Read':
    path=inp.get('file_path','');lines=numbered_lines(raw);read_lines.setdefault(path,{}).update(lines)
    entry['line_numbers']=sorted(lines)
    if path.endswith('.png') and result and not result.get('is_error'):screens.append(sanitize(path,meta))
   calls.append(entry)
 reference=str(Path(meta['bundle'])/'skills/design/better-layout/first-impression.md')
 reference_full=full_read(Path(reference).read_text(),read_lines.get(reference,{})) if Path(reference).exists() else None
 read_owners=[o for o in OWNERS if full_read((Path(meta['bundle'])/f'skills/design/{o}/SKILL.md').read_text(),read_lines.get(str(Path(meta['bundle'])/f'skills/design/{o}/SKILL.md'),{}))]
 result=next((r for r in reversed(rows) if r.get('type')=='result'),{})
 response=result.get('result','')
 if not response:
  response='\n\n'.join(b.get('text','') for r in rows if r.get('type')=='assistant' for b in r.get('message',{}).get('content',[]) if b.get('type')=='text')
 response=sanitize(response,meta)
 name=(phase+'-' if phase!='initial' else '')+f'{meta["arm"]}-{meta["case_id"]}';out=HERE/'responses';out.mkdir(exist_ok=True)
 (out/(name+'.md')).write_text(response+'\n')
 own_plugin=next((p for p in init.get('plugins',[]) if p.get('name')=='paul-skills'),{})
 receipt={k:meta.get(k) for k in ['arm','case_id','session_id','prompt','exit_code','timed_out','duration_seconds','cost_usd','result_subtype','actual_model','usage','model_usage','files_before','files_after','freeze_sha256']}
 receipt.update(phase=phase,host_version=init.get('claude_code_version'),requested_effort='low',response=f'responses/{name}.md',response_sha256=sha((out/(name+'.md')).read_bytes()),raw_events_sha256=sha((folder/'events.jsonl').read_bytes()),completed=meta['exit_code']==0 and not meta['timed_out'] and meta['result_subtype']=='success',inputs_unchanged=meta['files_before']==meta['files_after'],plugin_path_matches=own_plugin.get('path')==meta['bundle'],plugin_version=own_plugin.get('version'),per_turn_effort_active=init.get('per_turn_effort_active'),explicit_entry_command_recorded=any('/paul-skills:' in str(r.get('message',{}).get('content','')) for r in rows if r.get('type')=='user'),primary_body_visibility='host command expansion receipt; full injected body not exposed in stream',launched_skills=launched,loaded_domain_owners=sorted(set(launched+read_owners)&set(OWNERS)),first_impression_fully_read=reference_full,screenshot_reads=screens,tool_calls=calls,tool_errors=errors)
 target=HERE/'receipts';target.mkdir(exist_ok=True);(target/(name+'.json')).write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
 return receipt

if __name__=='__main__':
 folders=[RAW]
 receipts=[x for f in folders if f.exists() for p in sorted(f.iterdir()) if p.is_dir() and (x:=collect(p))]
 print(json.dumps([{'id':r['phase']+'-'+r['arm']+'-'+r['case_id'],'complete':r['completed'],'ref':r['first_impression_fully_read'],'owners':len(r['loaded_domain_owners']),'cost':r['cost_usd']} for r in receipts],indent=2))
