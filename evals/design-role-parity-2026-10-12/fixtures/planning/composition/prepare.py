"""Initialize only a fresh disposable composition checkout, never the source fixture."""
import json
from pathlib import Path
import subprocess
import sys
root=Path(__file__).resolve().parent
if '.git' in [p.name for p in root.iterdir()]:
    raise SystemExit('Refusing: this directory already contains .git')
if 'evals' in root.parts and 'fixtures' in root.parts:
    raise SystemExit('Copy this fixture to a disposable directory before preparation')
inside=subprocess.run(['git','rev-parse','--show-toplevel'],cwd=root,text=True,capture_output=True)
if inside.returncode==0:
    raise SystemExit('Refusing: this directory is inside another Git checkout')
def git(*args):
    return subprocess.check_output(['git',*args],cwd=root,text=True).strip()
git('init','-q')
git('add','app/index.html','app/tokens.css')
git('-c','user.name=Fixture Author','-c','user.email=fixture@example.invalid','-c','commit.gpgsign=false','commit','-qm','Fixture application baseline')
(root/'baseline.json').write_text(json.dumps({'base_commit':git('rev-parse','HEAD'),'scope':['app/'],'synthetic':True},indent=2)+'\n')
print('Prepared disposable baseline; all stage output must remain outside the source fixture.')
