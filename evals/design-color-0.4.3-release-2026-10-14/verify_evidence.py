"""Verify release activation evidence without equating it with semantic quality."""
from pathlib import Path
import hashlib,json,subprocess
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def source_result(receipt,case,host,expected):
    if host=='codex':
        got=receipt['loaded_file_hashes'].get(case['expected'])
        load_check=receipt['checks']['target_body_equal']
    else:
        loads=[x for x in receipt['full_body_loads'] if x['name']==case['expected']]
        got=loads[0]['file_sha256'] if loads else None
        load_check=receipt['checks']['expected_skill_invoked_and_loaded'] if case['mode']=='implicit' else receipt['checks']['target_body_equal'] if case['mode']=='explicit' else receipt['checks']['expected_owner']
    assert got is None or got==expected
    assert load_check==(got==expected)
    reference=True
    if case['id'].endswith('-resolved'):
        reference=receipt['contrast_reference']['full_body_equal']
        assert receipt['checks']['contrast_reference_fully_read']==reference
    return load_check and reference
def main():
    cfg=read(HERE/'cases.json');reviews=read(HERE/'manual-review.json');results=read(HERE/'RESULTS.json');ids=[];counts={};source_results=[]
    files=read(HERE/'candidate-manifest.json')['files'];install=read(HERE/'installation.json')
    assert install['release_commit']==subprocess.check_output(['git','rev-parse','paul-skills@0.4.3^{}'],cwd=REPO,text=True).strip()
    assert install['files']==files and len(files)==175
    previous=read(REPO/'evals/design-color-evidence-2026-10-14/candidate-manifest.json')['files']
    assert [p for p in files if files[p]!=previous[p]]==['.claude-plugin/plugin.json']
    for host,key in [('codex','codex'),('claude','cases')]:
        cache=Path(install['hosts'][host]['cache'].replace('$HOME',str(Path.home())))
        assert all(sha(cache/p)==v for p,v in files.items())
        rows=[]
        for case in cfg['cases']:
            r=read(HERE/host/(case['id']+'.json'));ids.append(r['session_id']);rows.append(r)
            v=reviews[key][case['id']];h=hashlib.sha256(r['final_response'].encode()).hexdigest()
            assert v['response_sha256']==r['response_sha256']==h
            assert r['checks']['semantic_review_pass']==v['pass'] and r['pass']==all(r['checks'].values())
            assert r['checks']['daily_global_install']
            assert r['protocol_sha256']==sha(HERE/'PROTOCOL.md') and r['cases_sha256']==sha(HERE/'cases.json')
            assert r['bundle_manifest_sha256']==sha(HERE/'candidate-manifest.json')
            source='skills/design/'+case['expected']+'/SKILL.md'
            source_results.append(source_result(r,case,host,files[source]))
        counts[host]={'completed':len(rows),'passed':sum(r['pass'] for r in rows)}
        assert counts[host]==results[host]['by_arm']['candidate']
    assert len(ids)==12==len(set(ids))
    amendment=read(HERE/'verification-amendment.json')
    for name,digest in read(HERE/'harness-manifest.json').items():
        if name==amendment['modified_file']:
            assert sha(HERE/'initial-verifier/verify_evidence.py')==digest==amendment['before_sha256']
            assert sha(REPO/name)==amendment['after_sha256']
        elif name==amendment['formatting_only']['file']:
            assert hashlib.sha256((REPO/name).read_bytes()+b'\n').hexdigest()==digest==amendment['formatting_only']['before_sha256']
            assert sha(REPO/name)==amendment['formatting_only']['after_sha256']
        else:assert sha(REPO/name)==digest,name
    old=read(REPO/'evals/design-routing-0.4.2-release-2026-10-14/codex/normal-better-colors.json');assert not old['checks']['semantic_review_pass']
    baseline=read(REPO/'evals/design-color-evidence-2026-10-14/claude/baseline-original-3.json');assert not baseline['checks']['semantic_review_pass']
    print(json.dumps({'integrity_pass':True,'installation_verified':True,'source_application_verified':all(source_results),'source_application_passed':sum(source_results),'native_sessions':len(ids),'counts':counts,'full_sample_passed':all(x['passed']==x['completed'] for x in counts.values())}))
if __name__=='__main__':main()
