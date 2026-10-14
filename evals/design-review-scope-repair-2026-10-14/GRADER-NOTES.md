# Native evidence corrections

The initial collector temporarily flagged `normal-better-ui` as not having read its full body. The completed command stream retained only the later search output, whereas the native transcript contained the entire exact SKILL.md. The collector now also binds a native call ID, the requested absolute source path and the complete matching body in that call's output. A matching filename, an assistant claim or a partial body is insufficient. The source snapshot, prompt and model answer remain unchanged. Tests reject a different path, mismatched call ID and missing body tail.

The initial collector also treated `rg` exit 1 as a tool failure in `explicit-domain`. That code means no match, while the preceding skill read had succeeded. The collector recognizes normal search outcomes; malformed `sed` commands and real errors remain failures. In particular, the five malformed reference reads in `normal-better-colors` are not forgiven because the agent later recovered. Controls reject a failing predecessor and empty-path read errors.

These correct evidence interpretation, not invocation or scope requirements. The Codex typography/color staged preloading failure remains a failure. The run protocol and all 25 cases were frozen before execution. These corrections are recorded after observing native host output and before the final report.

Claude numbered Read output needs whitespace-preserving normalization: strip the line-number prefix only. The initial pattern consumed blank lines and code indentation, falsely rejecting the complete audit procedure. A control preserves both blank lines and indentation before exact-body comparison. Actual tool calls and full matching text remain mandatory.
