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

## User-supplied local sources

A local skill supplied for adaptation may have no Git repository or declared license. Record it in `localSources`, separately from Git-backed `sources`, and list the consuming skill's `localOrigins`. This is a direct source of copied or adapted material, not an influence. Use `composite` when a skill combines Git and local direct sources.

Each local source records a portable locator such as `local-skill:<name>`, the relative filenames actually used and their SHA-256 content digests, a `digest`, and the known license/permission status. The source digest is SHA-256 of compact JSON containing sorted `(relative filename, file digest)` pairs. A null license records an undeclared license; user authorization for local adaptation does not imply redistribution clearance. Keep personal filesystem paths and unrelated files out of the public inventory.

A `localOrigins` entry names the source, its immutable `importedDigest`, the last completely reviewed `reviewedDigest`, and adaptation decisions. Compare a changed local source as a new content snapshot; preserve historical imported fields. Record a new source key for a new immutable snapshot. The existing Git comparison helper handles Git-backed origins only. A local source's review requires reading the actual recorded files and matching their hashes; inventory validation checks metadata consistency and is not a source-content or license verification.
