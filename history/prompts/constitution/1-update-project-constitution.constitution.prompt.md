---
id: 1
title: Update Project Constitution
stage: constitution
date: 2025-12-06
surface: agent
model: Qwen Code
feature: none
branch: main
user: user
command: /sp.constitution
labels: [constitution, setup, documentation]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/spec-template.md
 - .specify/templates/tasks-template.md
tests:
 - none
---

## Prompt

```
/sp.constitution Project Name: AI-Native Unified Book + RAG Chatbot Platform
Primary Tools: Qwen Code, Spec-Kit Plus, Docusaurus, GitHub Pages, FastAPI, OpenAI Agents/ChatKit SDKs, Neon Serverless Postgres, Qdrant Cloud, Better-Auth

1. Project Principles

Specification-Driven Development (SDD) will be followed strictly.

No code is written without a clear spec, plan, and task.

All generated code must be deterministic, modular, and readable.

All AI-generated code must be reviewed manually before merging.

2. Quality Standards

Docusaurus pages must be clean, responsive, and accessible.

Chatbot must meet latency target ≤ 1.5s average for indexed lookups.

Backend APIs must follow REST standards.

Database schema must be normalized and migrations consistent.

Security: JWT or session tokens via Better-Auth.

Sensitive data stored only in Postgres / Qdrant, not in client.

3. Architecture Standards

Monorepo using /book, /backend, /agents, /skills.

Strong separation of concerns:

Frontend (Docusaurus)

Backend (FastAPI)

Vector DB (Qdrant)

RDBMS (Neon Postgres)

Agents & Skills (OpenAI Agents, Claude Subagents)

4. Documentation Rules

Every component must have a README.md.

ADR files generated using /sp.adr.

Prompt history captured via /sp.phr.
Coding Guidelines

Use TypeScript for Docusaurus custom components.

Use Python for FastAPI, agent logic, ingestion pipelines.

Use Pydantic for schemas.

Use async everywhere.
```

## Response snapshot

Constitution update complete with version 1.0.0. All principles and requirements from the input have been incorporated into the constitution file. Dependent templates have been updated to align with the new constitution.

## Outcome

- ✅ Impact: New project constitution created with 6 core principles and aligned templates
- 🧪 Tests: none
- 📁 Files: 4 files updated (.specify/memory/constitution.md, .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md)
- 🔁 Next prompts: Ready to proceed with project development following the new constitution
- 🧠 Reflection: Constitution properly captures all specified principles and requirements

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A