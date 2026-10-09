#!/usr/bin/env node
// Changesets 3 output no longer triggers changesets/action's legacy tag parser.
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const { version } = JSON.parse(readFileSync("package.json", "utf8"));
if (!/^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$/.test(version)) {
  throw new Error("A release version is required before publishing a tag");
}
const cli = fileURLToPath(new URL("../node_modules/@changesets/cli/bin.js", import.meta.url));
execFileSync(process.execPath, [cli, "git-tag"], { stdio: "inherit" });
// Push only this package's version. Existing tags are never moved or force-pushed.
execFileSync("git", ["push", "origin", `refs/tags/v${version}`], { stdio: "inherit" });
