#!/usr/bin/env node
// Keep the installable plugin and npm lock metadata on the package version.
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repo = join(dirname(fileURLToPath(import.meta.url)), "..");
const { version } = JSON.parse(readFileSync(join(repo, "package.json"), "utf8"));
const pluginPath = join(repo, ".claude-plugin", "plugin.json");
const lockPath = join(repo, "package-lock.json");
const plugin = JSON.parse(readFileSync(pluginPath, "utf8"));
const lock = JSON.parse(readFileSync(lockPath, "utf8"));
const pluginMatches = plugin.version === version;
const lockMatches = lock.version === version && lock.packages[""].version === version;

if (pluginMatches && lockMatches) {
  console.log(`Plugin and lock metadata match package version ${version}`);
} else if (process.argv.includes("--check")) {
  console.error(`Release metadata differs from package version ${version}. Run node scripts/sync-plugin-version.mjs.`);
  process.exitCode = 1;
} else {
  if (!pluginMatches) {
    plugin.version = version;
    writeFileSync(pluginPath, JSON.stringify(plugin, null, 2) + "\n");
  }
  if (!lockMatches) {
    lock.version = version;
    lock.packages[""].version = version;
    writeFileSync(lockPath, JSON.stringify(lock, null, 2) + "\n");
  }
  console.log(`Plugin and lock metadata synchronized to ${version}`);
}
