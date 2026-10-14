"""Verify the observed existence/search probes, not arbitrary failed reads."""
import hashlib,os,shlex,subprocess
from pathlib import Path

def confirm_git_query_result(command,cwd):
    try:
        outer=shlex.split(command['command'])
        inner=outer[-1] if len(outer)==3 and outer[1] in {'-c','-lc'} else command['command']
        args=shlex.split(inner)
    except (ValueError,KeyError):return None
    # Bound to the two observed commands; do not accept a generic nonzero exit.
    exists=args==['git','cat-file','-e','HEAD:src/New.html'] and command.get('exit_code')==128
    search=args==['git','grep','-n','-e','New.html','-e','new-action','HEAD','--','.'] and command.get('exit_code')==1
    if not (exists or search):return None
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
    def execute(argv):return subprocess.run(argv,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=10)
    head=execute(['git','rev-parse','--verify','HEAD'])
    if head.returncode or head.stderr:return None
    if exists:
        if not (Path(cwd)/'src/New.html').is_file():return None
        tree=execute(['git','ls-tree','-r','--name-only','HEAD','--','src/New.html'])
        tracked=execute(['git','ls-files','--','src/New.html'])
        if tree.returncode or tree.stdout or tree.stderr or tracked.returncode or tracked.stdout or tracked.stderr:return None
    result=execute(args)
    output=result.stdout+result.stderr
    if result.returncode!=command['exit_code'] or output!=command.get('aggregated_output',''):return None
    if exists and output!="fatal: path 'src/New.html' exists on disk, but not in 'HEAD'\n":return None
    if search and output:return None
    return {'reason':'untracked file absent from valid HEAD' if exists else 'valid HEAD search returned no matches','argv':args,'exit_code':result.returncode,'head_sha':head.stdout.strip(),'replay_output_equal':True,'output_sha256':hashlib.sha256(output.encode()).hexdigest()}
