#!/usr/bin/env node
// Keep both installable plugin manifests and npm lock metadata on the package version.
// The Claude manifest is the source for every field the Cursor manifest shares with it.
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const SHARED_FIELDS = ["name", "description", "license", "homepage", "repository", "keywords", "skills"];

const repo = join(dirname(fileURLToPath(import.meta.url)), "..");
const files = {
  claude: ".claude-plugin/plugin.json",
  cursor: ".cursor-plugin/plugin.json",
  lock: "package-lock.json",
};
const read = (file) => readFileSync(join(repo, file), "utf8");
const { version } = JSON.parse(read("package.json"));
const original = Object.fromEntries(Object.entries(files).map(([key, file]) => [key, read(file)]));
const { claude, cursor, lock } = Object.fromEntries(
  Object.entries(original).map(([key, text]) => [key, JSON.parse(text)]),
);
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);

const drift = [];
if (claude.version !== version) drift.push(`${files.claude} version`);
if (cursor.version !== version) drift.push(`${files.cursor} version`);
if (lock.version !== version || lock.packages[""].version !== version) drift.push(`${files.lock} version`);
for (const field of SHARED_FIELDS) {
  if (!same(cursor[field], claude[field])) drift.push(`${files.cursor} ${field}`);
}
if (cursor.author?.name !== claude.author?.name) drift.push(`${files.cursor} author.name`);

if (drift.length === 0) {
  console.log(`Plugin manifests and lock metadata match package version ${version}`);
} else if (process.argv.includes("--check")) {
  console.error(
    `Release metadata differs from package version ${version} or the Claude manifest: ${drift.join(", ")}. ` +
      "Run node scripts/sync-plugin-version.mjs.",
  );
  process.exitCode = 1;
} else {
  claude.version = version;
  cursor.version = version;
  for (const field of SHARED_FIELDS) cursor[field] = claude[field];
  cursor.author = { ...cursor.author, name: claude.author.name };
  lock.version = version;
  lock.packages[""].version = version;
  for (const [key, value] of Object.entries({ claude, cursor, lock })) {
    const text = JSON.stringify(value, null, 2) + "\n";
    if (text !== original[key]) writeFileSync(join(repo, files[key]), text);
  }
  console.log(`Plugin manifests and lock metadata synchronized to ${version}`);
}
