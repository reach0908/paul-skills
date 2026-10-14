from pathlib import Path
import json,hashlib
E=Path(__file__).resolve().parent;P=E.parent/'design-domain-entry-repair-v4-2026-10-14';raw=E.parents[1]/'.scratch/design-domain-entry-repair-v4-20261014'
a=json.loads((P/'candidate-manifest.json').read_text())['files'];b=json.loads((E/'candidate-manifest.json').read_text())['files'];changed=[f for f in sorted(a.keys()|b.keys()) if a.get(f)!=b.get(f)]
assert changed==['skills/design/better-colors/contrast.md']
needle='Disabled and placeholder text are not covered by a requirement.'
rows=[];consumers={};carried={}
for host in ['codex','claude']:
 consumers[host]=[];carried[host]=[]
 for f in sorted((P/host).glob('*.json')):
  if f.stem=='summary':continue
  row=json.loads(f.read_text());methods=[]
  for line in (raw/host/(f.stem+'.jsonl')).read_text().splitlines():
   try:event=json.loads(line)
   except json.JSONDecodeError:continue
   if host=='codex' and event.get('type')=='item.completed' and event.get('item',{}).get('type')=='command_execution':
    item=event['item']
    if 'contrast.md' in item['command']:methods.append('explicit-reference-command')
    if needle in item.get('aggregated_output',''):methods.append('reference-content-in-tool-result')
   if host=='claude':
    content=event.get('message',{}).get('content',[])
    for block in content if isinstance(content,list) else []:
     if block.get('type')=='tool_use' and block.get('name')=='Read' and block.get('input',{}).get('file_path','').endswith('/better-colors/contrast.md'):methods.append('explicit-reference-read')
     if block.get('type')=='tool_result' and needle in json.dumps(block):methods.append('reference-content-in-tool-result')
  if host=='codex':
   for line in (raw/host/(f.stem+'.transcript.jsonl')).read_text().splitlines():
    event=json.loads(line)
    if event.get('payload',{}).get('type')=='custom_tool_call_output' and needle in json.dumps(event['payload'].get('output','')):methods.append('reference-content-in-tool-result')
  consumed=bool(methods)
  if consumed:consumers[host].append(f.stem)
  else:
   assert row['pass'],(host,f.stem)
   carried[host].append(f.stem)
  rows.append({'host':host,'case_id':f.stem,'source_receipt':str(f.relative_to(E.parent)),'receipt_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'session_id':row['session_id'],'read_changed_reference':consumed,'evidence_methods':sorted(set(methods)),'eligible_carried_pass':not consumed and row['pass']})
 for name in consumers[host]:assert name.startswith('normal-better-colors')
 assert len(consumers[host])==3 and len(carried[host])==24
out={'changed_bundle_files':changed,'unchanged_bundle_files':len(b)-len(changed),'all_entry_bodies_and_catalog_metadata_unchanged':True,'reference_consumers':consumers,'carried_cases':carried,'carried_pass_count':sum(map(len,carried.values())),'rows':rows,'limitations':'Observed dependencies from preserved native tool calls and tool outputs; carried sessions are not re-executed on candidate 9.'}
(E/'impact-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:out[k] for k in ['changed_bundle_files','unchanged_bundle_files','reference_consumers','carried_pass_count']})
