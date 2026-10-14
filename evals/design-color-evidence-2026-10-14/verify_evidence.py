"""Verify fixed cases, source/response identity and review integrity, not semantics."""
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
    cases=read(HERE/'cases.json')['cases'];reviews=read(HERE/'manual-review.json');results=read(HERE/'RESULTS.json');ids=[];counts={}
    for host,key in [('codex','codex'),('claude','cases')]:
        rows=[]
        for c in cases:
            r=read(HERE/host/(c['id']+'.json'));ids.append(r['session_id']);rows.append(r)
            digest=hashlib.sha256(r['final_response'].encode()).hexdigest();v=reviews[key][c['id']]
            assert r['response_sha256']==v['response_sha256']==digest
            assert r['checks']['semantic_review_pass']==v['pass'];assert r['pass']==all(r['checks'].values())
            assert r['protocol_sha256']==sha(HERE/'PROTOCOL.md');assert r['cases_sha256']==sha(HERE/'cases.json')
            assert r['bundle_manifest_sha256']==sha(HERE/(c['arm']+'-manifest.json'))
            expected=read(HERE/(c['arm']+'-manifest.json'))['files']['skills/design/'+c['expected']+'/SKILL.md']
            observed=r['loaded_file_hashes'][c['expected']] if host=='codex' else next(x['file_sha256'] for x in r['full_body_loads'] if x['name']==c['expected'])
            assert observed==expected
            if c['id'].endswith('-resolved'):assert r['checks']['contrast_reference_fully_read']
        counts[host]={a:{'completed':sum(r['arm']==a for r in rows),'passed':sum(r['arm']==a and r['pass'] for r in rows)} for a in ['baseline','candidate']}
        assert counts[host]==results[host]['by_arm']
    assert len(ids)==24==len(set(ids))
    b=read(HERE/'baseline-manifest.json')['files'];c=read(HERE/'candidate-manifest.json')['files'];assert b.keys()==c.keys()
    assert [p for p in b if b[p]!=c[p]]==['skills/design/better-colors/SKILL.md']
    assert all(sha(REPO/p)==v for p,v in c.items())
    g=read(HERE/'global-before.json');assert all(v==b for v in g.values())
    global_unchanged={host:all(sha(Path.home()/('.'+host)/'plugins/cache/paul-skills/paul-skills/0.4.2'/p)==v for p,v in files.items()) for host,files in g.items()};assert all(global_unchanged.values())
    for name,d in read(HERE/'harness-manifest.json').items():
        current=sha(REPO/name)
        if name.endswith('/collect.py'):
            a=read(HERE/'grader-amendment.json');assert d==a['initial_collect_sha256'];assert current==a['updated_collect_sha256'];assert sha(HERE/'initial-collect.py.txt')==d
        else:assert current==d,name
    historical=read(HERE/'environment.json')['historical_failure'];assert sha(REPO/historical['path'])==historical['sha256']
    old=read(REPO/historical['path']);assert old['checks']['semantic_review_pass'] is False
    print(json.dumps({'integrity_pass':True,'unique_native_sessions':len(ids),'counts':counts,'global_0_4_2_unchanged':global_unchanged}))
if __name__=='__main__':main()
