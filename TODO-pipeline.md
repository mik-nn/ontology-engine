# TODO: Pipeline Low Fidelity + Tavily Search

## Approved Plan (with Tavily)

- [x] 1. Fixed tavily_search.py import error (next_id unused).
- [x] 2. task_classifier.py: low_conf <0.6 → AnalysisTask (triggers search).
- [ ] 3. planning/task_planner.py: Sequence enrichment → search → summarize → interview loop.
- [ ] 4. pipeline/interview.py: Use search tool + LLM summarize.
- [x] 5. Tavily deps installed + auto-registered in tools/__init__.py.
- [ ] 6. Test `ont run "explain quantum computing"` → verify search/enrich.
