# Архитектура

Слоистая архитектура (сверху вниз). Зависимости только вниз: верхний слой знает о нижнем, нижний — нет о верхнем.

```
┌─────────────────────────────────────────────────────────────┐
│  presentation     controllers, schemas, main.py             │
├─────────────────────────────────────────────────────────────┤
│  application      services, use-cases, оркестрация API      │
├─────────────────────────────────────────────────────────────┤
│  agents           LangGraph: Intake → Risk/Policy/Fraud →…  │
├─────────────────────────────────────────────────────────────┤
│  domain           сущности, решения, голоса, правила        │
├─────────────────────────────────────────────────────────────┤
│  infrastructure   БД, ML, RAG, LLM, alembic                 │
└─────────────────────────────────────────────────────────────┘
```

## Дерево проекта

```
credit-decision-committee/
├── main.py                          # точка входа: uvicorn + create_app()
├── alembic/                         # миграции схемы БД
│   └── versions/
├── alembic.ini
├── data/
│   └── credit_policy.md             # учебная кредитная политика
├── src/
│   ├── presentation/                # слой API (внешний контур)
│   │   ├── controllers/             # FastAPI routers
│   │   │   └── applications.py      # POST/GET /applications, protocol, what-if, resume
│   │   ├── schemas/                 # Pydantic request/response DTO
│   │   │   ├── application.py
│   │   │   └── decision.py
│   │   └── dependencies.py          # DI: сессии БД, сервисы
│   │
│   ├── application/                 # слой use-cases
│   │   ├── services/
│   │   │   ├── application_service.py   # подать заявку, статус, resume
│   │   │   ├── decision_service.py      # запуск комитета, получение решения
│   │   │   └── whatif_service.py        # контрфактические сценарии
│   │   └── dto/                     # внутренние DTO между слоями (опционально)
│   │
│   ├── agents/                      # слой мультиагентного комитета
│   │   ├── graph.py                 # LangGraph: узлы и рёбра пайплайна
│   │   ├── state.py                 # общее состояние графа (CommitteeState)
│   │   ├── intake.py                # валидация / needs_info
│   │   ├── risk_model.py            # PD + SHAP-факторы
│   │   ├── policy_rag.py            # цитаты политики, hard-stop
│   │   ├── fraud.py                 # противоречия и аномалии
│   │   ├── advocate.py              # смягчающие факторы
│   │   ├── chair.py                 # сводка голосов, hard-stop, decision
│   │   └── explain.py               # memo + what-if текст
│   │
│   ├── 
│   └── infrastructure/              # слой адаптеров к внешнему миру
│       ├── db/
│       │   ├── models.py            # SQLAlchemy ORM
│       │   ├── session.py
│       │   └── repositories/
│       │       └── application_repo.py
│       ├── ml/
│       │   ├── scorer.py            # CatBoost / sklearn inference
│       │   └── shap_explainer.py
│       ├── rag/
│       │   ├── qdrant_store.py
│       │   └── policy_retriever.py
│       ├── llm/domain/                      # слой домена (без FastAPI / LangGraph)
│   │   ├── entities/
│   │   │   ├── application.py       # заявка
│   │   │   ├── decision.py          # approve | reject | manual_review | needs_info
│   │   │   ├── vote.py              # голос агента
│   │   │   └── protocol.py          # протокол комитета
│   │   ├── enums.py
│   │   └── rules/                   # детерминированные hard-rules политики
│   │       └── hard_stops.py
│   │
│       │   └── client.py            # генерация memo / explain (не score)
│       └── mcp/                     # опционально: search_policy, run_model, …
│           └── tools.py
│
├── tests/
├── PRODUCT.md
└── architecture.md
```

## Слои и ответственность


| Слой               | Папка                | Отвечает за                                                                                 | Не делает                                  |                                  |
| ------------------ | -------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------ | -------------------------------- |
| **Presentation**   | `src/presentation`   |                                                                                             | HTTP, валидация входа/выхода, коды ответов | бизнес-логику, вызов ML напрямую |
| **Application**    | `src/application`    | сценарии: создать заявку → запустить комитет → отдать решение / protocol / what-if / resume | детали HTTP и детали промптов агентов      |                                  |
| **Agents**         | `src/agents`         | роли комитета, LangGraph state/graph, голосование                                           | персистентность, сырой SQL                 |                                  |
| **Domain**         | `src/domain`         | сущности, enum решений, hard-stop правила, инварианты                                       | I/O, фреймворки                            |                                  |
| **Infrastructure** | `src/infrastructure` | БД (Alembic + SQLAlchemy), модель риска, Qdrant, LLM                                        | решения комитета                           |                                  |


## Поток запроса

```
Client
  → presentation/controllers  (POST /applications)
    → application/services    (ApplicationService.submit)
      → agents/graph          (Committee graph.run)
        → domain              (Decision, Vote, Protocol)
        → infrastructure      (scorer, policy RAG, DB save)
    ← DecisionResponse schema
```

## Правила зависимостей

1. `presentation` → `application` → `agents` / `domain`
2. `agents` → `domain` + интерфейсы из `infrastructure` (через DI, не наоборот)
3. `domain` не импортирует остальные слои
4. `infrastructure` реализует порты (репозитории, scorer, retriever); вызывается из `application` / `agents`
5. LLM только в `explain` / memo — **не** считает PD и **не** подменяет hard-stop политики

## Соответствие API ↔ слои


| Endpoint                          | Application service         | Агенты / инфраструктура        |
| --------------------------------- | --------------------------- | ------------------------------ |
| `POST /applications`              | `ApplicationService.submit` | Intake → полный граф → persist |
| `GET /applications/{id}`          | `ApplicationService.get`    | `application_repo`             |
| `GET /applications/{id}/protocol` | `DecisionService.protocol`  | protocol из domain + votes     |
| `POST /applications/{id}/what-if` | `WhatIfService.run`         | Explain + scorer / SHAP        |
| `POST /applications/{id}/resume`  | `ApplicationService.resume` | Intake → продолжение графа     |


