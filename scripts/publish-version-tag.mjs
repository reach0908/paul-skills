#!/usr/bin/env node
// Keep Paul release tags separate from inherited upstream version tags.
import { execFileSync, spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";

const { name, version } = JSON.parse(readFileSync("package.json", "utf8"));
if (name !== "paul-skills" || !/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/.test(version)) {
  throw new Error("A release version is required before publishing a tag");
}
const tag = `${name}@${version}`;
const ref = `refs/tags/${tag}`;
const existing = spawnSync("git", ["show-ref", "--verify", "--quiet", ref]);
if (existing.error || (existing.status !== 0 && existing.status !== 1)) {
  throw new Error("Could not inspect existing release tags", { cause: existing.error });
}
if (existing.status === 1) {
  execFileSync("git", ["tag", "-a", tag, "-m", tag], { stdio: "inherit" });
}
// Push only this package's version. Existing tags are never moved or force-pushed.
execFileSync("git", ["push", "origin", ref], { stdio: "inherit" });
