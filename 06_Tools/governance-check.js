#!/usr/bin/env node
/**
 * Governance Check
 *
 * Mechanically enforces a small subset of rules that are already defined in
 * 01_Rules/Global.md and 02_Policies/Naming_Policy.md, and that were
 * previously enforced only by human/AI review discipline.
 *
 * This script intentionally checks nothing that isn't already written down
 * as a rule elsewhere in the repository. It does not invent new policy.
 */

"use strict";

const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

const REPO_ROOT = path.resolve(__dirname, "..");

const RESERVED_NAMES = new Set([
  "temp",
  "tmp",
  "new",
  "final",
  "final2",
  "draft-final",
  "copy",
  "backup",
]);

// Naming_Policy.md "Reserved Names" / "Repository Structure Naming" examples
// only govern authored repository artifacts, not third-party dependency trees.
const DEPENDENCY_DIR_NAMES = new Set([
  "node_modules",
  ".venv",
  "venv",
  "__pycache__",
  "dist",
  "build",
  "site-packages",
]);

// Global.md "Repository Hygiene": no committed secrets/credentials/build artifacts.
const DEPENDENCY_PATH_SEGMENT = new RegExp(
  `(^|/)(${[...DEPENDENCY_DIR_NAMES].join("|")})(/|$)`
);

// Naming_Policy.md "Document Naming" -> Avoid: Doc1.md, Notes.md, Final.md, New.md.
// Checked as literal generic names rather than a Pascal_Case shape regex,
// because the repository's own ID-prefixed documents (e.g. ADR-0001-*.md,
// Requirement_Review_Report_RR-REQ-002.md) legitimately mix hyphens and
// identifiers and are not "generic" names.
const AVOID_DOCUMENT_NAMES = new Set(["doc1", "notes"]);

// Versioning_Policy.md "Version Format": MAJOR.MINOR.PATCH, no leading zeros.
const SEMVER_LEADING_ZERO = /\b0\d+\.\d+\.\d+\b|\b\d+\.0\d+\.\d+\b|\b\d+\.\d+\.0\d+\b/;

// Versioning_Policy.md "Version History": "Every artifact shall maintain [a
// version history table]". Enforced for the framework's core governed
// directories only; project/example folders may contain ungoverned files.
const VERSION_HISTORY_REQUIRED_DIRS = [
  "01_Rules/",
  "02_Policies/",
  "03_Templates/",
  "04_Prompts/",
];

// NFR-003 (REQ-EX-001): on unavailable/malformed git input, fail gracefully
// with one clear error line and exit code 2 (tool failure, not a violation).
function listTrackedFiles() {
  try {
    const output = execFileSync("git", ["ls-files"], {
      cwd: REPO_ROOT,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
    });
    return output.split("\n").filter(Boolean);
  } catch (error) {
    console.error(
      `Governance check could not run: "git ls-files" failed (${String(error.message).split("\n")[0]}).`
    );
    process.exit(2);
  }
}

function checkReservedAndDependencyNames(files) {
  const errors = [];
  for (const file of files) {
    if (DEPENDENCY_PATH_SEGMENT.test(file)) {
      errors.push(
        `[dependency-committed] "${file}" is inside a dependency/build directory (Global.md Repository Hygiene: "Do not commit secrets, credentials, build artifacts, or generated output").`
      );
      continue;
    }
    const base = path.basename(file, path.extname(file)).toLowerCase();
    if (RESERVED_NAMES.has(base)) {
      errors.push(
        `[reserved-name] "${file}" uses a reserved name (Naming_Policy.md "Reserved Names").`
      );
    }
  }
  return errors;
}

function checkMarkdownCase(files) {
  const errors = [];
  for (const file of files) {
    if (!file.endsWith(".md")) continue;
    const base = path.basename(file, ".md").toLowerCase();
    if (AVOID_DOCUMENT_NAMES.has(base)) {
      errors.push(
        `[naming-case] "${file}" uses a generic document name (Naming_Policy.md "Document Naming" Avoid list).`
      );
    }
  }
  return errors;
}

// Global.md "Repository Hygiene": logs are generated output and must not be
// committed (see also 05_Projects/ChatGptInExcel gap G-006 for a real case).
function checkTrackedLogFiles(files) {
  const errors = [];
  for (const file of files) {
    if (file.endsWith(".log")) {
      errors.push(
        `[log-committed] "${file}" is a log file (Global.md Repository Hygiene: "Do not commit secrets, credentials, build artifacts, or generated output").`
      );
    }
  }
  return errors;
}

function checkVersionHistoryPresence(files) {
  const errors = [];
  for (const file of files) {
    if (!file.endsWith(".md")) continue;
    if (!VERSION_HISTORY_REQUIRED_DIRS.some((dir) => file.startsWith(dir))) continue;
    const fullPath = path.join(REPO_ROOT, file);
    if (!fs.existsSync(fullPath)) continue;
    const content = fs.readFileSync(fullPath, "utf8");
    if (!/#\s*Version History/i.test(content)) {
      errors.push(
        `[version-history-missing] "${file}" has no "# Version History" section (Versioning_Policy.md "Version History": every artifact shall maintain one).`
      );
    }
  }
  return errors;
}

function checkVersionHistorySemver(files) {
  const errors = [];
  for (const file of files) {
    if (!file.endsWith(".md")) continue;
    const fullPath = path.join(REPO_ROOT, file);
    if (!fs.existsSync(fullPath)) continue;
    const content = fs.readFileSync(fullPath, "utf8");
    if (!/#\s*Version History/i.test(content)) continue;
    const versionHistorySection = content.slice(content.search(/#\s*Version History/i));
    if (SEMVER_LEADING_ZERO.test(versionHistorySection)) {
      errors.push(
        `[version-format] "${file}" has a Version History entry with a leading zero (Versioning_Policy.md "Version Format": "Leading zeros are not permitted.").`
      );
    }
  }
  return errors;
}

function main() {
  const files = listTrackedFiles();

  const errors = [
    ...checkReservedAndDependencyNames(files),
    ...checkMarkdownCase(files),
    ...checkVersionHistorySemver(files),
    ...checkTrackedLogFiles(files),
    ...checkVersionHistoryPresence(files),
  ];

  if (errors.length === 0) {
    console.log(`Governance check passed (${files.length} tracked files).`);
    process.exit(0);
  }

  console.error(`Governance check failed with ${errors.length} issue(s):\n`);
  for (const error of errors) {
    console.error(`  - ${error}`);
  }
  process.exit(1);
}

main();
