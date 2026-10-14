"""Shared command evidence for explicit local scopes, not an answer-only grade."""
import re

def local_scope_checks(case, commands):
    if case['mode'] != 'handoff':
        return {}
    texts=[c for c in commands if re.search(r'\bgit\b|\bgh\b',c)]
    # Local targets need neither remote/default branch discovery nor merge base.
    unrelated=re.compile(r'\bmerge-base\b|\bgh\s+repo\s+view\b|\bgit\s+remote\b|origin/(?:HEAD|main|master)')
    staged=case['id']=='staged-divergent'
    index_diff=any(re.search(r'\bgit\s+diff\b[^\n]*(?:--cached|--staged)',c) for c in texts)
    index_read=any(re.search(r'\bgit\s+show\s+[\"\']?:src/Panel\.html',c) for c in texts)
    working_diff=any(re.search(r'\bgit\s+diff\b',c) and re.search(r'\bHEAD\b|\b[0-9a-f]{40}\b',c) and not re.search(r'--cached|--staged',c) for c in texts)
    untracked=any('ls-files' in c and ('--others' in c or '-o ' in c) for c in texts)
    return {'no_default_branch_resolution':not any(unrelated.search(c) for c in texts),
            'target_snapshot_read':index_diff and index_read if staged else working_diff and untracked}
