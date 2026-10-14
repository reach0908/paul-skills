# Composition handoff
Copy this directory outside every existing Git checkout, then run `python3 prepare.py` once before stage 1. It creates an isolated local baseline containing only app files and records the exact base commit in `baseline.json`. It refuses existing repositories and the source fixture location. No remote or global Git setting is changed.

Run the five stage tasks in order, with a fresh executor context at each handoff and a 240-second budget per stage. Give each stage the common brief, its task and real earlier artifacts. The builder changes `app/`; the reviewer compares those working changes to the prepared baseline. Do not commit the build before review or invent a previous handoff artifact.

The sequential data intentionally exposes propagation failures. An upstream omission remains evidence; downstream stages may report the mismatch but must not silently replace source artifacts. Compare end-to-end invariant survival and resource use across equal tool/budget conditions. A successful experiment does not approve a real design or promote a skill.
