"""Validate frozen source, trial receipts, scope facts and publication manifest."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
def sha(data):return hashlib.sha256(data).hexdigest()
def read(path):return json.loads(path.read_text())
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write-manifest',action='store_true');parser.add_argument('--live-install',action='store_true');parser.add_argument('--live-source',action='store_true');args=parser.parse_args()
    manifest=read(HERE/'candidate-manifest.json')['files'];assert len(manifest)==175
    baseline=read(REPO/'evals/design-staged-routing-repair-2026-10-14/baseline-manifest.json')['files']
    for rel,digest in manifest.items():
        if args.live_source:assert sha((REPO/rel).read_bytes())==digest,rel
        snap=HERE/'candidate-sources'/rel
        data=snap.read_bytes() if snap.exists() else subprocess.check_output(['git','show','paul-skills@0.4.1:'+rel],cwd=REPO)
        assert sha(data)==digest,rel
    domains=['better-accessibility','better-layout','better-writing','better-typography','better-colors','better-ui']
    for name in domains:
        rel='skills/design/'+name+'/SKILL.md'
        old=subprocess.check_output(['git','show','paul-skills@0.4.1:'+rel],cwd=REPO,text=True).split('---',2)[2]
        new=(HERE/'candidate-sources'/rel).read_text().split('---',2)[2]
        new=re.sub(r'## Review entry\n\n.*?\n\n','',new,count=1,flags=re.S)
        new=re.sub(r'## Read supporting references\n\n.*?\n\n','',new,count=1,flags=re.S)
        assert new==old,name
    original=(REPO/'evals/design-staged-routing-repair-2026-10-14/candidate3-sources/skills/design/better-interface/SKILL.md').read_text()
    procedure=(HERE/'candidate-sources/skills/design/better-interface/audit-procedure.md').read_text()
    assert original[original.index('### 2. Resolve the surface scope'):] in procedure
    catalog=read(HERE/'catalog.json');assert catalog['selected']==len(catalog['entries'])==44
    for entry in catalog['entries']:assert entry['enabled'] and manifest[entry['relative_path']]==entry['file_sha256']
    cases={c['id']:c for c in read(HERE/'cases.json')['cases']};assert len(cases)==27
    manual=read(HERE/'manual-review.json');sessions=set();totals={};cost=0
    runner=(HERE/'run_trials.py').read_text()
    addition="\n파일과 참조 문서는 Read/Glob/Grep으로 읽고, Git 조회는 허용된 읽기 전용 git 하위 명령을 각각 하나의 Bash 호출로 실행해. 셸 연결이나 파이프, cd, git -C 없이 현재 폴더에서 조회해."
    facts=read(HERE/'fixture-facts.json')
    for host in ['codex','claude']:
        rows=[read(p) for p in (HERE/host).glob('*.json') if p.name!='summary.json'];assert len(rows)==27
        for row in rows:
            case=cases[row['case_id']];assert row['session_id'] not in sessions;sessions.add(row['session_id'])
            assert row['pass']==all(row['checks'].values())
            assert row['protocol_sha256']==sha((HERE/'PROTOCOL.md').read_bytes())
            assert row['cases_sha256']==sha((HERE/'cases.json').read_bytes())
            assert row['bundle_manifest_sha256']==sha((HERE/'candidate-manifest.json').read_bytes())
            prompt=case['prompt'].replace('/paul-skills:','$paul-skills:') if host=='codex' else case['prompt']+(addition if case['mode']=='handoff' else '')
            assert row['prompt']==prompt,(host,case['id'])
            loads=row.get('loaded_file_hashes',{b['name']:b['file_sha256'] for b in row.get('full_body_loads',[])})
            for name,digest in loads.items():assert manifest['skills/design/'+name+'/SKILL.md']==digest
            review=manual['codex' if host=='codex' else 'cases'][case['id']]
            assert review['response_sha256']==sha(row['final_response'].encode())
            assert review['pass']==row['checks']['semantic_review_pass']
            cost+=row.get('reported_cost_usd') or 0
            if case['fixture']!='empty':
                fact=facts[host][case['id']];assert fact['main']!=fact['head'] and fact['main_lacks_name'] and fact['head_has_name']
                assert fact['index_lacks_name'] and fact['index_diff_files']==['src/Panel.html']
                if case['mode']=='handoff':assert fact['head'] in row['final_response'],(host,case['id'],'head')
                if case['fixture']=='index-divergent':
                    assert fact['working_diff_files']==[] and fact['untracked']==['src/New.html'] and fact['working_has_name']
        counts={'completed':len(rows),'passed':sum(r['pass'] for r in rows)}
        assert read(HERE/host/'summary.json')['by_arm']['candidate']==counts;totals[host]=counts
    assert len(sessions)==54
    results=read(HERE/'RESULTS.json');assert results['outcomes']==totals and results['unique_sessions']==54
    assert results['claude_reported_list_cost_usd']==round(cost,7)
    references=read(HERE/'reference-reads.json')
    for host in ['codex','claude']:
        assert len(references[host])==3
        for name,record in references[host].items():
            row=read(HERE/host/(name+'.json'))
            assert record['session_id']==row['session_id'] and record['count']==len(record['completed_full_reads']) and record['count']>0
            for file,proof in record['completed_full_reads'].items():
                assert proof['full_body_equal'] and proof['source_sha256']==manifest['skills/design/better-colors/'+file]
    for p in (HERE/'codex').glob('*.json'):
        if p.name=='summary.json':continue
        row=read(p)
        assert all('Excludes change/regression reviews.' in row['delivered_design_descriptions'][name] for name in domains)
    before=read(HERE/'global-before.json');after=read(HERE/'global-after.json');assert before==after
    if args.live_install:
        for host,files in before.items():
            cache=Path.home()/('.'+host)/'plugins/cache/paul-skills/paul-skills/0.4.1'
            for rel,digest in files.items():assert sha((cache/rel).read_bytes())==digest,(host,rel)
    files={str(p.relative_to(HERE)):sha(p.read_bytes()) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
    for rel in files:
        text=(HERE/rel).read_text();assert '\N{EM DASH}' not in text,rel
        assert not re.search(r'/Users/[A-Za-z0-9_-]+/|sk-ant-[a-z0-9_-]{10,}|gh[pousr]_[A-Za-z0-9]{20,}',text),rel
    if args.write_manifest:(HERE/'MANIFEST.json').write_text(json.dumps({'files':files},indent=2)+'\n')
    assert read(HERE/'MANIFEST.json')['files']==files
    print(json.dumps({'receipt_integrity':'pass','unique_sessions':54,'outcomes':totals,'daily_install_unchanged':True,'files':len(files)}))
if __name__=='__main__':main()
