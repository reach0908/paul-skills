"""Resolve current skill locations without changing frozen trial identities."""
import json
from pathlib import Path


def skill_directory(root, name):
    root = Path(root).resolve()
    records = json.loads((root / 'skill-sources.json').read_text())['skills']
    matches = [r['path'] for r in records if r['id'] == name]
    if len(matches) != 1:
        raise ValueError(f'Expected one registered skill: {name}')
    relative = Path(matches[0])
    if relative.is_absolute() or '..' in relative.parts or relative.parts[:1] != ('skills',):
        raise ValueError(f'Invalid registered skill path: {name}')
    folder = root / relative
    if any(p.is_symlink() for p in [folder, *folder.parents] if p != root and root in p.parents):
        raise ValueError(f'Linked skill path: {name}')
    if not (folder / 'SKILL.md').is_file():
        raise ValueError(f'Missing registered skill: {name}')
    return folder
