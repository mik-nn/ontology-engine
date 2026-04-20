---
created: '2026-04-18'
id: implementation_plan
process:
  transformer: human
synced_at: '2026-04-20T12:09:19.568828+00:00'
title: Implementation Plan for Ontology Engine
type: architecture
version: 1.0.0
---

databook:
  id: implementation_plan
  title: "Implementation Plan for Ontology Engine"
  version: 1.0.0
  type: architecture
  domain: ontology-engine
  status: draft
  created: 2026-04-18
  updated: 2026-04-18
  author:
    - name: Michael
      iri: https://ontologist.ai/agents/michael
  process:
    transformer: human
    inputs: []
  license: CC-BY-4.0
  tags:
    - ontology
    - architecture
    - pipeline
    - planning
    - shacl
    - reasoning
---
# 📘 Implementation Plan (Техническое Задание)
## Онтологический Движок для Построения, Обогащения, Верификации и Планирования Проектов

---

# 1. Цель системы

Создать онтологический движок, который:

1. Строит онтологию проекта на основе:
   - запроса пользователя,
   - структуры существующего проекта,
   - данных из интернета (Tavily),
   - интерактивного интервьюирования.

2. Обогащает онтологию:
   - автоматически (reasoning, правила, SHACL),
   - внешними знаниями,
   - пользовательскими ответами.

3. Проверяет онтологию:
   - автоматически (SHACL 1.2),
   - вручную (пользовательская верификация).

4. Формирует непротиворечивые, полные и не избыточные контексты для LLM.

5. Визуализирует граф знаний (read‑only на первом этапе).

6. Выполняет планирование и декомпозицию сложных запросов до атомарных задач.

7. **Формирует pipeline исключительно на основе логики онтологии**, а не LLM.

8. **LLM используется только как исполнитель атомарных задач**, но не как управляющий компонент.

---

# 2. Общая архитектура

core/  
  ontology/  
  shacl/  
  rules/  

introspection/  
  project_scanner.py  
  code_parser.py  
  doc_parser.py  

enrichment/  
  tavily_client.py  
  external_mapper.py  

interaction/  
  interviewer.py  
  user_feedback.py  

verification/  
  shacl_validator.py  
  rule_engine.py  

context/  
  context_builder.py  
  context_pruner.py  
  context_explainer.py  

planning/  
  task_classifier.py  
  task_decomposer.py  
  task_planner.py  
  plan_executor.py  

pipeline/  
  pipeline_orches
