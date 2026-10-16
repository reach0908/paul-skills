"""Check source snapshots, execution receipts and unchanged daily installs."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
def read(path):return json.loads(path.read_text())
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-manifest',action='store_true');parser.add_argument('--live-install',action='store_true');args=parser.parse_args()
    baseline=read(HERE/'baseline-manifest.json')['files'];first=read(HERE/'candidate-manifest.json')['files'];second=read(HERE/'round2/candidate-manifest.json')['files'];final=read(HERE/'round3/candidate-manifest.json')['files']
    for path,digest in baseline.items():
        data=subprocess.check_output(['git','show','paul-skills@0.4.1:'+path],cwd=REPO);assert sha(data)==digest,path
        snapshot=HERE/'candidate1-sources'/path
        assert sha(snapshot.read_bytes() if snapshot.exists() else data)==first[path],path
        snapshot2=HERE/'candidate2-sources'/path
        assert sha(snapshot2.read_bytes() if snapshot2.exists() else data)==second[path],path
        snapshot3=HERE/'candidate3-sources'/path
        assert sha(snapshot3.read_bytes() if snapshot3.exists() else data)==final[path],path
    assert len(baseline)==len(first)==len(second)==len(final)==174
    assert read(HERE/'native-read-control/candidate-manifest.json')['files']==final
    catalog=read(HERE/'round3/catalog.json');assert catalog['selected']==len(catalog['entries'])==44
    for entry in catalog['entries']:assert entry['enabled'] and final[entry['relative_path']]==entry['file_sha256']
    config1=read(HERE/'cases.json');config2=read(HERE/'round2/cases.json');assert config1['cases']==config2['cases'];config3=read(HERE/'round3/cases.json');assert config3['cases'][:19]==config2['cases'];assert len(config3['cases'])==21
    domains={'better-accessibility','better-layout','better-writing','better-typography','better-colors','better-ui'}
    for name in domains:
        path='skills/design/'+name+'/SKILL.md'
        old=subprocess.check_output(['git','show','paul-skills@0.4.1:'+path],cwd=REPO,text=True).split('---',2)[2]
        new=(HERE/'candidate3-sources'/path).read_text().split('---',2)[2]
        assert re.sub(r'## Review entry\n\n.*?\n\n','',new,count=1,flags=re.S)==old,name
    sessions=set();outcomes={};cost=0
    for phase,root,expected in [('pilot',HERE,{'codex':6,'claude':3}),('candidate2',HERE/'round2',{'codex':19,'claude':19}),('final',HERE/'round3',{'codex':21,'claude':21}),('native-read-control',HERE/'native-read-control',{'codex':1})]:
        manual=read(root/'manual-review.json');cfg=read(root/'cases.json');known={c['id']:c for c in cfg['cases']}
        if phase=='pilot':known.update({f'baseline-staged-{i+1}':dict(cfg['cases'][i],id=f'baseline-staged-{i+1}',arm='baseline') for i in range(3)})
        for host,count in expected.items():
            rows=[read(p) for p in (root/host).glob('*.json') if p.name!='summary.json'];assert len(rows)==count,(phase,host,len(rows))
            for row in rows:
                case=known[row['case_id']];assert row['session_id'] not in sessions;sessions.add(row['session_id'])
                assert row['pass']==all(row['checks'].values())
                assert row['protocol_sha256']==sha((root/'PROTOCOL.md').read_bytes())
                assert row['cases_sha256']==sha((root/'cases.json').read_bytes())
                if phase=='final' and host=='claude':assert row['host_protocol_sha256']==sha((root/'CLAUDE-PROTOCOL.md').read_bytes())
                expected_prompt=case['prompt'].replace('/paul-skills:','$paul-skills:') if host=='codex' else case['prompt']
                assert row['prompt']==expected_prompt
                arm='baseline' if row.get('arm')=='baseline' else 'candidate';mf=root/(arm+'-manifest.json')
                assert row['bundle_manifest_sha256']==sha(mf.read_bytes())
                frozen=read(mf)['files'];loads=row.get('loaded_file_hashes',{b['name']:b['file_sha256'] for b in row.get('full_body_loads',[])})
                for n,d in loads.items():assert frozen['skills/design/'+n+'/SKILL.md']==d
                review=manual['codex' if host=='codex' else 'cases'][row['case_id']]
                assert review['response_sha256']==sha(row['final_response'].encode())
                assert row['checks']['semantic_review_pass']==review['pass']
                cost+=row.get('reported_cost_usd') or 0
            summary=read(root/host/'summary.json')
            for arm,counts in summary['by_arm'].items():
                subset=[r for r in rows if r['arm']==arm]
                assert counts=={'completed':len(subset),'passed':sum(r['pass'] for r in subset)}
            outcomes[phase+'-'+host]=summary['by_arm']
    assert len(sessions)==90
    infra=read(HERE/'round3/network-diagnostic.json')['attempts']
    for item in infra:
        assert item['session_id'] not in sessions;sessions.add(item['session_id'])
        assert item['model_responses']==0 and item['exit_code']!=0 and item['inputs_unchanged']
    assert len(sessions)==92
    totals=read(HERE/'RESULTS.json')
    assert totals['behavior_sessions']==90 and totals['network_failed_launches']==len(infra) and totals['unique_sessions_total']==len(sessions)
    assert totals['claude_reported_list_cost_usd']==round(cost,7)
    assert totals['outcomes']=={key:{arm:counts for arm,counts in arms.items() if counts['completed']} for key,arms in outcomes.items()}
    before=read(HERE/'global-before.json');after=read(HERE/'global-after.json');assert before==after
    if args.live_install:
        for host,files in before.items():
            cache=Path.home()/('.'+host)/'plugins/cache/paul-skills/paul-skills/0.4.1'
            for p,d in files.items():assert sha((cache/p).read_bytes())==d,(host,p)
    files={str(p.relative_to(HERE)):sha(p.read_bytes()) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
    for rel in files:
        text=(HERE/rel).read_text();assert '\N{EM DASH}' not in text,rel
        assert not re.search(r'/Users/[A-Za-z0-9_-]+/|sk-ant-[a-z0-9_-]{10,}|gh[pousr]_[A-Za-z0-9]{20,}',text),rel
    if args.write_manifest:(HERE/'MANIFEST.json').write_text(json.dumps({'files':files},indent=2)+'\n')
    assert read(HERE/'MANIFEST.json')['files']==files
    print(json.dumps({'receipt_integrity':'pass','unique_sessions':len(sessions),'outcomes':outcomes,'claude_reported_list_cost_usd':round(cost,7),'daily_install_unchanged':True,'files':len(files)}))
if __name__=='__main__':main()
