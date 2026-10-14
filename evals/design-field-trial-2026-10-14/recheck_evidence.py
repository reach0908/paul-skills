#!/usr/bin/env python3
"""Recalculate bounded claims from saved evidence; no browser or product writes."""
from pathlib import Path
import hashlib
import json
import re
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2] / ".scratch/design-field-review-20261014"
SRC = ROOT / "source"
DECODER = json.JSONDecoder()

def json_objects(path):
    text = path.read_text()
    result = []
    offset = 0
    while offset < len(text):
        match = re.search(r"(?m)^\{", text[offset:])
        if not match:
            break
        start = offset + match.start()
        try:
            value, length = DECODER.raw_decode(text[start:])
            result.append(value)
            offset = start + length
        except ValueError:
            offset = start + 1
    return result

manifest = json.loads((ROOT / "source-manifest.json").read_text())
bad = [r["path"] for r in manifest["files"] if hashlib.sha256((ROOT / r["path"]).read_bytes()).hexdigest() != r["sha256"]]
assert not bad, bad
first = SRC / "01-accessibility/evidence"
before = json_objects(first / "labels-before.log")[0]
after = json_objects(first / "labels-after-final.log")[0]
def label_counts(value):
    cards = [card for viewport in value["results"] for card in viewport["cards"]]
    return {"observations": len(cards), "visible_name_matches": sum(c["matchesVisibleAction"] for c in cards), "new_tab_notices": sum(c["preservesNewTabNotice"] for c in cards), "widths": [x["width"] for x in value["results"]]}
labels = {"before": label_counts(before), "after": label_counts(after)}
assert labels["before"]["observations"] == labels["after"]["observations"] == 15
assert labels["before"]["visible_name_matches"] == 0
assert labels["after"]["visible_name_matches"] == labels["after"]["new_tab_notices"] == 15
pixels = []
for width in [1440, 390, 320]:
    for part in ["", "card-"]:
        a = Image.open(first / f"before-{part}{width}.png").convert("RGB")
        b = Image.open(first / f"after-{part}{width}.png").convert("RGB")
        identical = a.size == b.size and a.tobytes() == b.tobytes()
        assert identical, (width, part)
        pixels.append({"width": width, "part": part or "full", "size": list(a.size), "changed_pixels": 0})

capture_root = SRC / "05-capture-card"
capture_text = (capture_root / "after/browser.log").read_text()
capture = DECODER.raw_decode(capture_text.split("### Result", 1)[1].lstrip())[0]
entries = [e for row in capture["records"] for e in row["entries"]]
assert len(entries) == 24 and [r["width"] for r in capture["records"]] == [1440, 390, 320]
assert all(e["aligned"] and e["linksInside"] and e["linksSeparate"] and e["imagesLoaded"] for e in entries)
assert not any(row["overflow"] for row in capture["records"])
comparison = json.loads((capture_root / "comparison.json").read_text())
assert comparison["beforeDesktop"]["mediaX"] - comparison["beforeDesktop"]["captionX"] == 38.953125
assert comparison["afterDesktop"]["mediaX"] == comparison["afterDesktop"]["captionX"]

flows = []
for stage, name in [("02-catalog-recovery", "evidence/flow-final.log"), ("02-catalog-recovery", "evidence/production-flow.log"), ("03-integration", "evidence/production-creator-onboarding.log"), ("04-reading", "creator-onboarding.log")]:
    observations = json_objects(SRC / stage / name)
    assert [x["width"] for x in observations] == [1440, 390, 320]
    for x in observations:
        assert len(x["profiles"]) == 5
        assert all(p["portraitLoaded"] for p in x["profiles"])
        state = x["onboarding"]
        assert state["count"] == 5 and state["oauthSubmitted"] is False
        assert all(state[k] for k in ["allFive", "firstFiveInOrder", "deselected", "restoredDraft", "reselected", "reviewHasFive"])
    flows.append({"stage": stage, "source": name, "profiles": 15, "widths": [1440, 390, 320], "selection_and_reload": True, "oauth_submitted": False, "built_local_server": "production" in name})

readings = [row for row in json_objects(SRC / "04-reading/reading-check.log") if "width" in row and "unlinkedMentions" in row]
assert [row["width"] for row in readings] == [1440, 390, 320]
reading = []
for row in readings:
    assert not row["unlinkedMentions"] and not row["errors"]
    reading.append({"width": row["width"], "figures": len(row["figures"]), "cards": len(row["cards"]), "quotes": len(row["quotes"]), "unlinked_mentions": len(row["unlinkedMentions"]), "structure": row["structure"], "page_errors": len(row["errors"])})

builds = []
for stage, name in [("02-catalog-recovery", "evidence/build-final.log"), ("03-integration", "evidence/build.log"), ("04-reading", "build.log"), ("05-capture-card", "build.log")]:
    text = (SRC / stage / name).read_text()
    complete = "521/521" in text and not re.search(r"Build error occurred|Error: Failed to collect", text)
    assert complete
    builds.append({"stage": stage, "source": name, "static_pages": "521/521", "build_completion_recorded": True})

loads = (first / "skill-loads.md").read_text()
load_rows = []
for path, digest in re.findall(r"`(/[^`]+)`\s*\|\s*`([0-9a-f]{64})`", loads):
    if "/.local/paul-design-trial-20261013/skills/" not in path:
        continue
    p = ROOT / "loaded-skills" / path.split("/skills/", 1)[-1]
    matches = p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == digest
    load_rows.append({"skill_relative_path": path.split("/skills/", 1)[-1], "sha256": digest, "frozen_file_matches": matches})
assert len(load_rows) == 23 and all(r["frozen_file_matches"] for r in load_rows)

result = {"audit_date": "2026-10-14", "timezone": "Asia/Seoul", "method": "offline re-derivation from preserved artifacts; no new browser run", "integrity": {"files": len(manifest["files"]), "mismatches": bad, "stable_during_copy": all(x["source_stable_during_copy"] for x in manifest["files"])}, "labels": labels, "initial_visual_pairs": pixels, "capture": {"observations": 24, "all_aligned_loaded_and_links_inside": True, "no_overflow": True, "before_desktop_offset_px": 38.953125, "after_desktop_offset_px": 0, "keyboard_viewport": 320, "keyboard_initial_focus": "programmatic, followed by native Tab/Shift+Tab/Enter", "original_harness_gap": "capture count and overflow are observations without explicit failure assertions; this audit asserts both"}, "flows": flows, "reading": reading, "builds": builds, "loaded_skill_files": load_rows, "limits": {"raw_model": None, "tokens": None, "cost": None, "same_session_reuse": True, "controlled_original_comparison": False, "skill_promotion": False, "runtime_rerun_this_audit": False}}
(ROOT / "audit-results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"integrity_files": len(manifest["files"]), "initial_label_before": labels["before"]["visible_name_matches"], "initial_label_after": labels["after"]["visible_name_matches"], "identical_png_pairs": len(pixels), "capture_observations": len(entries), "flow_record_groups": len(flows), "build_records": len(builds), "matched_skill_files": len(load_rows)}, ensure_ascii=False))
