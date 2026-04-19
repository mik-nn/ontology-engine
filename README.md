# ontology-engine

Онтологический движок для автоматического построения, обогащения, верификации и планирования проектов.

## Структура проекта

- core/ — онтология, SHACL, правила
- introspection/ — анализ существующего проекта
- enrichment/ — обогащение через Tavily
- interaction/ — интервьюирование пользователя
- verification/ — SHACL + rule engine
- context/ — формирование контекстов
- planning/ — классификация, декомпозиция, планирование
- pipeline/ — оркестрация pipeline (без LLM)
- visualization/ — граф знаний
- storage/ — хранилище RDF
- api/ — skills/tools для агентов

