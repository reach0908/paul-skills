"""Confirm a narrow expected no-match exit by replaying read-only Git discovery."""
import hashlib,os,shlex,subprocess
from pathlib import Path

def confirm_empty_discovery(command,cwd):
    if command.get('exit_code')!=1:return None
    try:
        outer=shlex.split(command['command']);inner=outer[-1] if len(outer)>=3 and outer[1] in {'-c','-lc'} else command['command']
        tokens=shlex.split(inner)
    except ValueError:return None
    if any(t in tokens for t in [';','|','||','>','>>','<']):return None
    parts=[];part=[]
    for token in tokens:
        if token=='&&':parts.append(part);part=[]
        else:part.append(token)
    parts.append(part)
    stop=next((i for i,p in enumerate(parts) if p[:2]==['rg','--files']),None)
    if stop is None or stop==0:return None
    safe={'rev-parse','status','diff','ls-files'}
    if any(len(p)<2 or p[0]!='git' or p[1] not in safe or any(a.startswith('--output') or a in ['--no-index','--ext-diff','--textconv'] for a in p) for p in parts[:stop]):return None
    search=parts[stop];i=2
    while i<len(search)-1:
        if search[i]!='-g' or i+1>=len(search)-1:return None
        i+=2
    if i!=len(search)-1 or search[-1]!='.':return None
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0');combined='';receipts=[]
    for args in parts[:stop+1]:
        result=subprocess.run(args,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=15)
        if result.stderr:return None
        combined+=result.stdout;receipts.append({'argv':args,'exit_code':result.returncode})
        if args!=search and result.returncode!=0:return None
    if receipts[-1]['exit_code']!=1 or combined!=command.get('aggregated_output',''):return None
    return {'reason':'optional file discovery returned no matches','replay_output_equal':True,'output_sha256':hashlib.sha256(combined.encode()).hexdigest(),'commands':receipts,'skipped_successors':len(parts)-stop-1}

def confirm_absent_doc_guards(command,cwd):
    if command.get('exit_code')!=1:return None
    try:
        outer=shlex.split(command['command']);inner=outer[-1] if len(outer)>=3 and outer[1] in {'-c','-lc'} else command['command']
    except ValueError:return None
    names=['AGENTS.md','CLAUDE.md','CONTRIBUTING.md','CODING_STANDARDS.md','README.md','package.json']
    guard='for f in '+' '.join(names)+'; do test -f "$f" && { echo "===== $f ====="; sed -n \'1,260p\' "$f"; }; done &&'
    if guard not in inner or not command.get('aggregated_output','').endswith('===== ROOT DOCS =====\n'):return None
    if any((Path(cwd)/name).exists() for name in names):return None
    return {'reason':'optional document guards found no files','all_guarded_paths_absent':names,'output_sha256':hashlib.sha256(command['aggregated_output'].encode()).hexdigest(),'skipped_successors':True}
