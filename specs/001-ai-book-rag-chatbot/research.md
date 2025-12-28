# Research Summary: AI-Native Unified Book + RAG Chatbot Platform

## Decision: Frontend Technology Stack
**Rationale**: Docusaurus is chosen for the documentation-based book platform due to its excellent Markdown support, built-in search, and plugin ecosystem. TypeScript is used for custom components to ensure type safety and maintainability.
**Alternatives considered**: Gatsby, Next.js, Nuxt.js - Docusaurus was chosen specifically for the book content management features.

## Decision: Backend Technology Stack
**Rationale**: FastAPI was selected for the backend due to its automatic API documentation generation, async support, and Pydantic integration. Python 3.11 provides the best ecosystem for AI/ML libraries.
**Alternatives considered**: Express.js with TypeScript, Django, Flask - FastAPI was chosen for its modern features and AI library compatibility.

## Decision: Authentication System
**Rationale**: Better-Auth was selected for its zero-backend approach, which fits well with the Docusaurus frontend. It provides secure JWT/session tokens as required by the constitution.
**Alternatives considered**: Auth0, Firebase Auth, custom JWT implementation - Better-Auth was chosen for its simplicity and no-backend requirement.

## Decision: Vector Database
**Rationale**: Qdrant Cloud was chosen for its managed service approach and good performance for semantic search. The free tier meets initial requirements.
**Alternatives considered**: Pinecone, Weaviate, Supabase Vector - Qdrant was chosen for its cost-effectiveness and Python SDK.

## Decision: Relational Database
**Rationale**: Neon Postgres was selected for its serverless capabilities, ease of use, and strong consistency. It fits the constitution requirements for storing user data.
**Alternatives considered**: PlanetScale, Supabase, traditional PostgreSQL - Neon was chosen for its serverless capabilities.

## Decision: AI Agent Frameworks
**Rationale**: OpenAI Agents SDK and Claude Subagents were chosen to leverage advanced reasoning capabilities and specialized skills. This allows for sophisticated features like chapter summarization and personalized tutoring.
**Alternatives considered**: LangChain, LlamaIndex - OpenAI/Anthropic native SDKs were chosen for their direct integration and performance.

## Decision: Content Generation
**Rationale**: Using Qwen Code with SDD process for generating the book content aligns with the project constitution and ensures high-quality documentation.
**Alternatives considered**: Other LLMs - Qwen was chosen as it's specifically mentioned in the constitution and project requirements.

## Decision: Translation Service
**Rationale**: OpenAI or similar LLMs for translation due to their advanced language understanding capabilities and ability to maintain context during translation.
**Alternatives considered**: Google Translate API, Azure Translator - LLMs were chosen for better context handling and consistency with the AI-focused architecture.

## Decision: Deployment Strategy
**Rationale**: GitHub Pages for static book content due to its simplicity and integration with GitHub. Backend services to be deployed on platforms like Render or Fly.io for Python/Node compatibility.
**Alternatives considered**: Netlify, Vercel, AWS - GitHub Pages and Render/Fly.io chosen for cost-effectiveness and technology compatibility.