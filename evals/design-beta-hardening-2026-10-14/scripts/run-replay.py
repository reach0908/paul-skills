from pathlib import Path
import subprocess,json,sys
E=Path(__file__).resolve().parents[1];stage=sys.argv[1];attempt=sys.argv[2]
assert stage in ['chain-wire','chain-build'];assert attempt.isalnum()
base=E/'evidence'/(stage+'-'+attempt);assert not base.with_suffix('.txt').exists(),'Preserve prior attempt'
script=base.with_suffix('.js');script.write_text((E/'scripts/replay-chain.js').read_text().replace('CHAIN_STAGE',stage))
cmd=['playwright-cli','-s=hard-evaluator','run-code','--filename='+str(script)]
p=subprocess.run(cmd,text=True,capture_output=True,timeout=180)
base.with_suffix('.txt').write_text(p.stdout);base.with_suffix('.stderr.log').write_text(p.stderr)
receipt={'command':cmd,'exitCode':p.returncode,'toolError':'### Error' in p.stdout}
base.with_suffix('.receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
if p.returncode or receipt['toolError']:print(json.dumps(receipt));raise SystemExit(1)
result,_=json.JSONDecoder().raw_decode(p.stdout.split('### Result\n',1)[1]);base.with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'stage':stage,'combinations':result['actualCombinations'],'keyboardControls':[r['observedFocusable'] for r in result['rows']],'states':[len(r['states']) for r in result['rows']],'captures':sum(len(r['captures']) for r in result['rows'])}))
