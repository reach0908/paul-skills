"""Run the frozen compatibility follow-up without changing global settings."""
import run_codex as runner
runner.RAW=runner.RAW.parent/'codex-compatible'
runner.BASE=runner.BASE.parent/'codex-compatible'
runner.MODEL_OVERRIDE='gpt-5.6-sol'
runner.PROTOCOL=runner.HERE/'CODEX-COMPATIBILITY.md'
if __name__=='__main__':runner.main()
