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
   - данных из интернета (Tawily),
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
  tawily_client.py  
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
  pipeline_orchestrator.py  
  event_logger.py  
  graph_updater.py  
  git_client.py  
  doc_sync.py  
  databook_sync.py  

visualization/  
  graph_exporter.py  
  graph_viewer/  

storage/  
  graph_store.py  
  id_manager.py  

api/  
  skills/  
  tools/  

---

# 3. Core Ontology Layer

## 3.1. Базовые классы онтологии

### Проект
- Project  
- hasModule  
- hasDataset  
- hasModel  
- hasTask  
- hasAssumption  
- hasGoal  

### Модули
- Module  
- CodeModule  
- DataModule  
- ServiceModule  
- ConfigModule  

### Данные
- Dataset  
- File  
- Measurement  
- Schema  
- Databook  

### Модели
- Model  
- LLMModel  
- MLModel  
- RuleModel  

### Задачи
- Task  
- AnalysisTask  
- DesignTask  
- ExplainTask  
- ImplementTask  
- RefactorTask  

### Планирование
- Plan  
- Subtask  
- dependsOn  

### События
- Event  
- ProjectScanned  
- ModuleDetected  
- ExternalKnowledgeAdded  
- UserAnswerReceived  
- OntologyValidated  
- ContextBuilt  
- TaskDecomposed  
- PlanGenerated  
- PlanExecuted  
- GitCommitPushed  
- DocumentationSynced  
- DatabookUpdated  

---

# 4. SHACL 1.2 и правила

## 4.1. Минимальные SHACL‑шейпы

- Project должен иметь хотя бы один Module.  
- Task должен иметь входы и выходы.  
- Model должен иметь тип.  
- Dataset должен иметь источник.  
- Plan должен иметь хотя бы один Subtask.  
- PipelineStep должен иметь исполнителя.  

## 4.2. Правила (Rule Engine)

- Если задача относится к объяснению → использовать LLM.  
- Если задача относится к структуре проекта → использовать reasoning.  
- Если задача слишком большая → декомпозировать.  
- Если контекст превышает лимит модели → уменьшить подграф.  
- Если задача требует изменения файлов → использовать git_client.  
- Если задача требует обновления документации → использовать doc_sync.  

---

# 5. Project Introspection Layer

## 5.1. Анализ структуры проекта
- Сканирование директорий.  
- Определение типов файлов.  
- Построение дерева модулей.  

## 5.2. Парсинг кода
- AST/CPG анализ.  
- Извлечение классов, функций, зависимостей, импортов.  

## 5.3. Парсинг документации
- README, docs/, md, rst.  
- Извлечение описаний, требований, архитектурных решений.  

## 5.4. Маппинг в онтологию
- Файлы → Module  
- Документы → Databook  
- Функции → Task  
- Зависимости → dependsOn  

---

# 6. External Enrichment Layer (Tawily)

## 6.1. Запросы
- По ключевым словам проекта.  
- По библиотекам.  
- По доменным терминам.  

## 6.2. Обогащение
- Добавление внешних сущностей: стандарты, протоколы, best practices.  

## 6.3. Верификация
- SHACL проверяет непротиворечивость.  

---

# 7. Interactive Interview Layer

## 7.1. Когда задавать вопросы
- SHACL выявил пробелы.  
- Недостаточно данных для выбора модели.  
- Неясные цели проекта.  
- Неполные Databooks.  

## 7.2. Типы вопросов
- О целях.  
- О допущениях.  
- О требованиях.  
- О приоритетах.  
- О структуре.  

## 7.3. Обработка ответов
- Ответ → новая сущность или свойство.  
- Создание события UserAnswerReceived.  

---

# 8. Verification Layer

## 8.1. Автоматическая верификация
- SHACL 1.2.  
- Правила.  

## 8.2. Пользовательская верификация
- UI/CLI: просмотр сущностей, подтверждение, исправление.  

---

# 9. Context Engine

## 9.1. Формирование контекста
1. Определить ядро запроса.  
2. Построить подграф.  
3. Проверить SHACL.  
4. Удалить нерелевантные ветки.  
5. Сформировать контекстный пакет.  

## 9.2. Контекстный пакет
- Факты (тройки).  
- Краткие резюме сущностей.  
- Databook‑фрагменты.  
- Список допущений.  

## 9.3. Объяснение контекста
- Почему включено.  
- Почему исключено.  
- Какие правила сработали.  

---

# 10. Planning & Decomposition Layer

## 10.1. TaskClassifier

### Режим 1: без LLM  
- ключевые слова,  
- регулярные выражения,  
- онтологические правила.

### Режим 2: с LLM (только как парсер намерений)  
- LLM классифицирует запрос,  
- SHACL проверяет корректность,  
- при сомнениях → интервьюирование.

## 10.2. Task Decomposer (без LLM)
- Декомпозиция по правилам.  
- Использование онтологических паттернов.  
- Построение дерева задач.  

## 10.3. Task Planner (без LLM)
- Топологическая сортировка.  
- Проверка зависимостей.  
- Выбор исполнителей (LLM/ML/Reasoning).  

## 10.4. Plan Executor
- Выполнение подзадач.  
- Обновление онтологии.  
- Генерация событий.  

---

# 11. Pipeline Orchestration Layer

## 11.1. Принципы

- Pipeline формируется **только** из онтологии и правил.  
- LLM **не управляет** проектом.  
- LLM **не ведёт протокол**.  
- LLM **не пушит в GitHub**.  
- LLM **не синхронизирует документацию**.  
- Все действия фиксируются как события.  
- Граф — единственный источник истины.  

## 11.2. Компоненты

- pipeline_orchestrator.py  
- event_logger.py  
- graph_updater.py  
- git_client.py  
- doc_sync.py  
- databook_sync.py  

## 11.3. Пример потока

1. Пользователь: «Сгенерируй модуль X».  
2. TaskClassifier → ImplementTask.  
3. TaskDecomposer → 5 подзадач.  
4. Planner → порядок выполнения.  
5. Executor:  
   - вызывает LLM для генерации кода,  
   - вызывает git_client для коммита,  
   - вызывает doc_sync для обновления Databook.  
6. EventLogger фиксирует всё.  
7. GraphUpdater обновляет онтологию.  
8. SHACL проверяет консистентность.  

---

# 12. Visualization Layer

## 12.1. Экспорт графа
- Graphviz DOT.  
- JSON для web‑viewer.  

## 12.2. Интерактивная карта
- Узлы: сущности.  
- Рёбра: связи.  
- Фильтры: по типам, задачам, модулям.  

---

# 13. Storage Layer

## 13.1. Хранилище графа
- RDFLib + Turtle файлы.  
- Позже — GraphDB/Neo4j.  

## 13.2. ID Manager
- Генерация стабильных URI.  

---

# 14. API Layer (Skills/Tools)

## 14.1. Skills
- ontology.query  
- ontology.extend  
- ontology.validate  
- context.build  
- context.explain  
- interview.ask  
- model.select  
- llm.invoke  

## 14.2. Tools
- CLI  
- REST (позже)  
- MCP‑интеграция  

---

# 15. Этапы реализации

## Этап 1. Core + SHACL
- core.ttl  
- shapes.ttl  
- graph_store.py  

## Этап 2. Инспекция проекта
- project_scanner  
- code_parser  
- doc_parser  

## Этап 3. Enrichment (Tawily)
- tawily_client  
- external_mapper  

## Этап 4. Interview Layer
- interviewer  
- user_feedback  

## Этап 5. Verification
- shacl_validator  
- rule_engine  

## Этап 6. Context Engine
- context_builder  
- context_pruner  
- context_explainer  

## Этап 7. Planning
- task_classifier  
- task_decomposer  
- task_planner  
- plan_executor  

## Этап 8. Pipeline Orchestration
- pipeline_orchestrator  
- event_logger  
- git_client  
- doc_sync  
- databook_sync  

## Этап 9. Visualization
- graph_exporter  
- graph_viewer  

---

# 16. Критерии готовности

- Онтология строится автоматически.  
- SHACL выявляет ошибки.  
- Пользователь может дополнять онтологию.  
- Контексты формируются корректно.  
- Запросы декомпозируются.  
- Pipeline формируется без участия LLM.  
- LLM используется только как исполнитель.  
- Граф визуализируется.  
