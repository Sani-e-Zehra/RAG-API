# Implementation Plan: AI-Native Unified Book + RAG Chatbot Platform

**Branch**: `001-ai-book-rag-chatbot` | **Date**: 2025-12-06 | **Spec**: [link to spec.md]
**Input**: Feature specification from `/specs/001-ai-book-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The AI-Native Unified Book + RAG Chatbot Platform will be built as a monorepo with a Docusaurus-based frontend, FastAPI backend, and integration with vector DB for RAG functionality. The system will include user authentication, personalization, Urdu translation, and advanced AI tools. It will follow Specification-Driven Development practices and be implemented using TypeScript for frontend and Python for backend services.

## Technical Context

**Language/Version**: TypeScript 5, Python 3.11
**Primary Dependencies**: Docusaurus, FastAPI, OpenAI/ChatKit SDKs, Neon Postgres, Qdrant, Better-Auth, Claude Subagents
**Storage**: Neon Postgres (relational), Qdrant Cloud (vector DB)
**Testing**: pytest for backend, Jest for frontend, contract testing for API endpoints
**Target Platform**: Web application (SSR/client-side rendering)
**Project Type**: Web application with monorepo structure following Architecture Standards
**Performance Goals**: <1.5s average for RAG lookups, 95% response rate within 5 seconds (per spec requirement FR-013)
**Constraints**: <200ms p95 for non-RAG API calls, token limit management for RAG queries, free tier usage constraints for Qdrant
**Scale/Scope**: 1000+ concurrent users, book content covering full lifecycle of AI-native systems

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Constitution requires:
- Specification-Driven Development: Feature must have clear spec, plan, and tasks before implementation
- Quality Standards: Implementation must be deterministic, modular, readable, with manual review of AI-generated code
- Architecture Standards: Implementation must follow monorepo structure with separation of concerns
- Documentation: Component must include README.md, ADR if significant decisions made, and prompt history via PHR
- Security: JWT/session tokens via Better-Auth, sensitive data stored only in Postgres/Qdrant
- Coding: Use TypeScript for Docusaurus, Python for FastAPI/agents, Pydantic schemas, async everywhere

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-book-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
book/                    # Docusaurus project
├── docs/                # Book content
├── src/
│   ├── components/      # Custom React components (chatbot, highlight widget, etc.)
│   ├── pages/
│   └── theme/
├── static/
├── docusaurus.config.js
├── package.json
└── README.md

backend/                 # FastAPI backend
├── src/
│   ├── api/             # API routes (auth, rag, translation, user prefs)
│   ├── models/          # Pydantic models
│   ├── services/        # Business logic
│   ├── database/        # Database connections and operations
│   ├── agents/          # OpenAI/ChatKit agent logic
│   └── skills/          # Claude Subagents + Skills
├── tests/
├── requirements.txt
└── README.md

agents/                  # OpenAI or ChatKit agent logic
├── rag_agent.py         # RAG agent for question answering
├── reasoning_agent.py   # Reasoning agent for complex queries
└── README.md

skills/                  # Claude Subagents + Skills
├── glossary_generator.py
├── chapter_summarizer.py
├── personalized_tutor.py
└── README.md

db/                      # Database migrations and schema
├── migrations/          # SQL migration files
├── schema.sql
└── README.md

pipelines/               # Ingestion pipelines (chunking, embedding, uploading)
├── chunker.py           # Text chunking logic
├── embedder.py          # Embedding generation
├── uploader.py          # Upload to vector DB
└── README.md

README.md
```

**Structure Decision**: Web application monorepo with separation of concerns following Architecture Standards. Frontend (Docusaurus) handles presentation, Backend (FastAPI) handles API and business logic, Vector DB (Qdrant) handles RAG data, RDBMS (Neon Postgres) handles user data, Agents & Skills (OpenAI Agents, Claude Subagents) handle AI logic.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple agent SDKs | Different AI providers offer unique strengths for various tasks | Using a single AI provider would limit functionality and create vendor lock-in |
| Multiple database systems | Different data types require different storage approaches (relational vs vector) | Single database would compromise performance for either structured or vector data |
