# TODO: Enable Local Ollama Models & Generate README

## Steps from Approved Plan

- [x] 1. Edit .ontology.toml: Activate [llm] section with Ollama config to avoid Claude CLI fallback.
- [x] 2. litellm installed (pyproject.toml supports [litellm]; run `pip install -e .[litellm]` if issues).
- [ ] 3. Start Ollama: `ollama serve` (background) & `ollama pull qwen2.5-coder:14b deepseek-r1:14b`
- [x] Sync requirements.txt ✅
- [ ] 4. Re-run pipeline: `ont run "Please add a description of how the project works, installation instructions for different operating systems, and system requirements to the README. "`
- [ ] 5. Approve README.md write permission in VSCode.
- [ ] 6. Verify success & commit if auto=true.

**Next:** Proceed to Step 1 (config edit)?
