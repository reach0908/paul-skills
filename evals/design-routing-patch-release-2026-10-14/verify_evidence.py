"""Verify published release receipts without replaying any agent."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(name):return json.loads((HERE/name).read_text())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write-manifest',action='store_true');args=ap.parse_args()
    install=read('installation.json');release=read('release.json');catalog=read('catalog.json')
    assert install['release_commit']==release['release_commit']==release['release_run']['headSha']
    assert release['release_run']['conclusion']=='success'
    assert install['promoted_skills']==catalog['total']==44
    assert len(install['files'])==174
    for path,expected in install['files'].items():
        content=subprocess.check_output(['git','show',install['release_tag']+':'+path],cwd=REPO)
        assert hashlib.sha256(content).hexdigest()==expected,path
    assert set(install['hosts'])=={'claude','codex'}
    assert all(x['version']=='0.4.1' and x['enabled'] and x['all_promoted_files_equal'] for x in install['hosts'].values())
    cfg=read('cases.json');names={Path(p).parent.name for p in install['files'] if p.startswith('skills/design/') and p.endswith('/SKILL.md')}
    assert len(names)==17
    auto=names-set(cfg['user_only']);sessions=set();outcomes={};manual=read('manual-review.json')
    for host in ['claude','codex']:
        rows=[]
        for case in cfg['cases']:
            r=read(host+'/'+case['id']+'.json')
            assert r['session_id'] not in sessions;sessions.add(r['session_id'])
            assert r['cases_sha256']==sha(HERE/'cases.json')
            expected_protocol='PROTOCOL.md' if host=='claude' else 'CODEX-COMPATIBILITY.md'
            assert r['protocol_sha256']==sha(HERE/expected_protocol)
            expected_prompt=case['prompt'].replace('/paul-skills:','$paul-skills:') if host=='codex' else case['prompt']
            assert r['prompt']==expected_prompt
            assert set(r['automatic_design_catalog'])==auto
            if host=='claude':
                assert set(r['direct_design_catalog'])==names
                assert r['checks']['actual_global_no_override']
                hashes={x['name']:x['file_sha256'] for x in r['full_body_loads']}
            else:hashes=r['loaded_file_hashes']
            for n,d in hashes.items():assert install['files']['skills/design/'+n+'/SKILL.md']==d
            mr=manual['cases' if host=='claude' else host][case['id']]
            assert mr['response_sha256']==hashlib.sha256(r['final_response'].encode()).hexdigest()
            assert r['checks']['semantic_review_pass']==mr['pass']
            assert r['pass']==all(r['checks'].values())
            rows.append(r)
        outcomes[host]={'completed':len(rows),'passed':sum(r['pass'] for r in rows)}
        summary=read(host+'/summary.json')
        assert summary['completed']==len(rows)
        assert (summary['by_arm']['installed']['passed'] if host=='claude' else summary['passed'])==outcomes[host]['passed']
    failures=read('environment-failures.json')['failed_launches']
    assert len(failures)==2
    for f in failures:
        assert f['exit_code']!=0 and f['inputs_unchanged'] and f['session_id'] not in sessions;sessions.add(f['session_id'])
    files={str(p.relative_to(HERE)):sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
    for p in files:
        content=(HERE/p).read_text()
        assert '\N{EM DASH}' not in content,p
        assert not re.search(r'/Users/[A-Za-z0-9_-]+/|sk-ant-[a-z0-9_-]{10,}|gh[pousr]_[A-Za-z0-9]{20,}',content),p
    if args.write_manifest:(HERE/'MANIFEST.json').write_text(json.dumps({'files':files},indent=2)+'\n')
    assert read('MANIFEST.json')['files']==files
    print(json.dumps({'receipt_integrity':'pass','outcomes':outcomes,'initial_environment_failures':2,'unique_sessions':len(sessions),'manifest_files':len(files)}))
if __name__=='__main__':main()
