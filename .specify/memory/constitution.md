<!--
SYNC IMPACT REPORT
Version change: N/A → 1.0.0
Modified principles: N/A (new constitution)
Added sections: All principles and sections added
Removed sections: N/A
Templates requiring updates: ✅ updated - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# AI-Native Unified Book + RAG Chatbot Platform Constitution

## Core Principles

### Specification-Driven Development (SDD)
All development must follow Specification-Driven Development methodology. No code is written without a clear spec, plan, and task. This ensures that every feature is well-defined before implementation, reducing ambiguity and rework.

### Quality Standards
All generated code must be deterministic, modular, and readable. All AI-generated code must be reviewed manually before merging. Quality includes: Docusaurus pages clean, responsive, and accessible; Chatbot must meet latency target ≤ 1.5s average for indexed lookups; Backend APIs follow REST standards; Database schema normalized and migrations consistent.

### Architecture Standards
Monorepo using /book, /backend, /agents, /skills. Strong separation of concerns: Frontend (Docusaurus), Backend (FastAPI), Vector DB (Qdrant), RDBMS (Neon Postgres), Agents & Skills (OpenAI Agents, Claude Subagents). This ensures maintainability and clear boundaries between system components.

### Documentation Rules
Every component must have a README.md. ADR files generated using /sp.adr. Prompt history captured via /sp.phr. This ensures knowledge is preserved and accessible to all team members.

### Security Standards
Security: JWT or session tokens via Better-Auth. Sensitive data stored only in Postgres / Qdrant, not in client. This ensures data protection and secure user authentication.

### Coding Guidelines
Use TypeScript for Docusaurus custom components. Use Python for FastAPI, agent logic, ingestion pipelines. Use Pydantic for schemas. Use async everywhere. This ensures consistency and leverages the strengths of each language appropriately.

## Technology Stack
Primary Tools: Qwen Code, Spec-Kit Plus, Docusaurus, GitHub Pages, FastAPI, OpenAI Agents/ChatKit SDKs, Neon Serverless Postgres, Qdrant Cloud, Better-Auth. All implementations must leverage these technologies as specified.

## Development Workflow
Development follows the Spec-Kit Plus methodology with specification, planning, and task creation phases. All code changes must have an associated task. Code reviews are mandatory for all pull requests. Continuous integration ensures code quality and system stability.

## Governance
This constitution supersedes all other development practices. Amendments require documentation, approval from project maintainers, and a migration plan if needed. All PRs/reviews must verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06
