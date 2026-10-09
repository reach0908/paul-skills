# Provenance contract, version 1

`skill-sources.json` is the workspace's canonical inventory. Keep it in Git, outside installed skill prompts. `metadata.provenance` in a skill's frontmatter can link to its canonical record so an individually installed skill still has a source pointer. That pointer is a locator, not a substitute for a pinned evaluation artifact.

```json
{
  "schemaVersion": 1,
  "sources": {
    "example": {
      "repository": "https://github.com/owner/repo",
      "ref": "main",
      "license": "MIT",
      "repositoryReview": "FULL_COMMIT_ID"
    }
  },
  "skills": [{
    "id": "my-skill",
    "path": "skills/engineering/my-skill",
    "kind": "adapted",
    "origins": [{
      "source": "example",
      "path": "skills/original-name",
      "importedRevision": "FULL_COMMIT_ID",
      "reviewedRevision": "FULL_COMMIT_ID",
      "localDigest": "sha256:HEX",
      "decisions": []
    }],
    "influences": []
  }]
}
```

Use `forked` for an inherited skill, `adapted` for copied and modified work, `composite` for multiple direct sources, and `original` for independently authored work. Originals have empty `origins`; optional `influences` record the repo, path, pinned revision, and what was learned. Never describe copied text as inspiration to avoid attribution. Preserve original in-file credits as transitive provenance. An unknown license or private source is not publication clearance.

`importedRevision` and import path record the historical origin and never move. `reviewedRevision` is the last completely reconciled upstream snapshot, not the latest scan. After a rename, preserve the original `path` and add `reviewPath` for subsequent comparisons. For each origin, `localDigest` hashes the entire current local skill tree. It detects local edits since reconciliation; it is not a quality score or evidence that we match upstream.

Each decision records `revision`, affected `paths`, `decision` (`adopt`, `adapt`, `keep-local`, `defer`), `reason`, and an optional report/eval link. Deferred decisions remain pending until explicitly resolved. Do not erase a permanent keep-local policy just because HEAD is unchanged. Multiple direct origins are reviewed independently; one source's review never advances another's revision.

`repositoryReview` tracks a separate review of maintenance files such as authoring rules, release workflows, manifests, and install instructions. Skill reviews do not advance it. A source with no completed repository review can omit it; the helper reports that gap. Unregistered/new skill paths are discovery candidates, not automatic imports.

The helper hashes sorted relative file paths, Git-compatible executable modes, and SHA-256 file contents as compact JSON, then hashes that payload. Symlinks, submodules, paths escaping the workspace, or missing baseline trees fail closed. Its output includes `localDigest`; after an authorized, completed review copy that value into the relevant origin. Review uses all ordinary files; remove accidental cache files before stamping. There is no automatic stamp command.

For a new source, save its canonical repository URL, ref, verified license, and exact import commit. Add one skill record per local skill, with all direct origins. Registration is a write operation: in report-only work, propose the metadata without changing it.
