"""Record actual Codex discovery of the isolated project skill copies."""
from pathlib import Path
import os,json,subprocess,select,time
E=Path(__file__).resolve().parents[1];T=Path('/private/tmp/paul-beta-hardening-20261014');w=T/'public/runs/chain-ia'
with (E/'catalog-stderr.log').open('w') as errors:
 p=subprocess.Popen(['codex','app-server','--stdio'],cwd=w,env=dict(os.environ,CODEX_HOME=str(T/'codex-home')),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=errors,text=True)
 messages=[]
 def call(number,method,params):
  p.stdin.write(json.dumps({'id':number,'method':method,'params':params})+'\n');p.stdin.flush();deadline=time.monotonic()+45
  while time.monotonic()<deadline:
   if not select.select([p.stdout],[],[],1)[0]:continue
   line=p.stdout.readline()
   if not line:raise RuntimeError('App server closed before response')
   m=json.loads(line);messages.append(m)
   if m.get('id')==number:return m
  raise TimeoutError(method)
 try:
  call(1,'initialize',{'clientInfo':{'name':'paul-beta-hardening','version':'1.0'}})
  p.stdin.write(json.dumps({'method':'initialized'})+'\n');p.stdin.flush()
  result=call(2,'skills/list',{'cwds':[str(w)],'forceReload':True})
  selected=[s for row in result.get('result',{}).get('data',[]) for s in row.get('skills',[]) if str(w/'.agents/skills') in s.get('path','')]
  for name,value in [('catalog',result),('catalog-selected',selected)]:
   (E/(name+'.json')).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
  print(json.dumps({'selected':len(selected),'names':[s['name'] for s in selected]}))
 finally:
  p.terminate()
  try:p.wait(timeout=5)
  except subprocess.TimeoutExpired:p.kill();p.wait()
  (E/'catalog-rpc.json').write_text(json.dumps(messages,ensure_ascii=False,indent=2)+'\n')
