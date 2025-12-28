---

description: "Task list for AI-Native Unified Book + RAG Chatbot Platform implementation"
---

# Tasks: AI-Native Unified Book + RAG Chatbot Platform

**Input**: Design documents from `/specs/001-ai-book-rag-chatbot/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `book/src/`, `agents/`, `skills/`, `db/`, `pipelines/`
- Adjust based on plan.md structure for monorepo

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan following monorepo with /book, /backend, /agents, /skills, /db, /pipelines
- [X] T002 [P] Initialize Docusaurus project in book/ directory with TypeScript configuration
- [X] T003 [P] Initialize FastAPI project in backend/ directory with Python 3.11 and async support
- [X] T004 Initialize agents/ directory for OpenAI/ChatKit agent logic
- [X] T005 Initialize skills/ directory for Claude Subagents and Skills
- [X] T006 Initialize db/ directory with SQL schema and migration setup
- [X] T007 Initialize pipelines/ directory for ingestion processing
- [X] T008 Configure linting and formatting tools for deterministic, readable code (ESLint, Prettier for TS, Black/isort for Python)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 [P] Setup database schema and migrations framework with normalized schema and consistent migrations in db/
- [ ] T010 [P] Implement authentication/authorization framework using Better-Auth with JWT/session tokens for both frontend and backend
- [ ] T011 Setup API routing and middleware structure in backend/src/api/ following REST standards
- [X] T012 [P] Create base Pydantic models that all stories depend on in backend/src/models/
- [X] T013 [P] Configure error handling and logging infrastructure with async support in backend/src/utils/
- [X] T014 Setup environment configuration management for both frontend and backend
- [X] T015 [P] Configure Qdrant Cloud connection and initial collection for vector embeddings
- [X] T016 Setup basic ingestion pipeline components in pipelines/ (chunker, embedder, uploader)
- [X] T017 Create book content structure in book/docs/ with placeholder content
- [X] T018 [P] Implement basic book deployment to GitHub Pages from book/ directory

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

## Phase 3: User Story 1 - Read AI-Generated Book and Ask Questions (Priority: P1) 🎯 MVP

**Goal**: Enable users to access the AI-generated book and ask questions about the content to get answers based on book content

**Independent Test**: A user can navigate to the deployed book, read content, and ask questions about chapters to get accurate answers based on the book's content.

### Implementation for User Story 1

- [ ] T019 [P] [US1] Create BookContent model in backend/src/models/book_content.py based on data model
- [ ] T020 [P] [US1] Create ChatSession and ChatMessage models in backend/src/models/chat_models.py based on data model
- [ ] T021 [US1] Implement BookService in backend/src/services/book_service.py to manage book content
- [ ] T022 [US1] Implement ChatService in backend/src/services/chat_service.py to manage chat sessions
- [ ] T023 [US1] Create RAG agent in agents/rag_agent.py for question answering from book content
- [ ] T024 [US1] Implement /rag/query endpoint in backend/src/api/rag_routes.py
- [ ] T025 [US1] Implement /rag/highlight-query endpoint in backend/src/api/rag_routes.py
- [ ] T026 [P] [US1] Create React chatbot widget component in book/src/components/ChatbotWidget.tsx
- [ ] T027 [US1] Add highlight-to-RAG selection logic in book/src/components/ChatbotWidget.tsx
- [ ] T028 [US1] Connect chatbot widget to backend API endpoints
- [ ] T029 [US1] Implement streaming UI for chat responses in book/src/components/ChatbotWidget.tsx
- [ ] T030 [US1] Add basic ingestion pipeline to upload book content to Qdrant in pipelines/uploader.py
- [ ] T031 [US1] Integrate RAG agent with Qdrant vector store for retrieval
- [ ] T032 [US1] Add proper error handling and validation for RAG queries

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Personalize Book Content (Priority: P2)

**Goal**: Allow users to provide technical background and preferences, and see content adapted to their level and interests

**Independent Test**: User can provide their technical background and preferences, and see content adapted to their level and interests.

### Implementation for User Story 2

- [ ] T033 [P] [US2] Create User and UserProfile models in backend/src/models/user_models.py based on data model
- [ ] T034 [P] [US2] Create PersonalizationPreferences model in backend/src/models/personalization_models.py based on data model
- [ ] T035 [US2] Implement UserService in backend/src/services/user_service.py to manage user profiles
- [ ] T036 [US2] Implement PersonalizationService in backend/src/services/personalization_service.py to manage preferences
- [ ] T037 [US2] Implement /auth/signup and /auth/signin endpoints in backend/src/api/auth_routes.py
- [ ] T038 [US2] Implement /user/preferences GET and PUT endpoints in backend/src/api/user_routes.py
- [ ] T039 [US2] Add personalization UI components in book/src/components/PersonalizationControls.tsx
- [ ] T040 [US2] Implement content personalization logic based on user preferences
- [ ] T041 [US2] Add onboarding flow to collect user background information
- [ ] T042 [US2] Integrate personalization features with book content rendering
- [ ] T043 [US2] Add preference persistence and retrieval in frontend

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Translate Content to Urdu (Priority: P3)

**Goal**: Enable users to translate book chapters to Urdu to comprehend content in their preferred language

**Independent Test**: User can click a button to translate any chapter to Urdu and read the translated content.

### Implementation for User Story 3

- [ ] T044 [US3] Create translation service in backend/src/services/translation_service.py using LLM for Urdu translation
- [ ] T045 [US3] Implement /translate/urdu endpoint in backend/src/api/translation_routes.py
- [ ] T046 [US3] Add Urdu translation UI button in book/src/components/TranslationControls.tsx
- [ ] T047 [US3] Integrate translation endpoint with frontend UI components
- [ ] T048 [US3] Implement translation for selected text functionality
- [ ] T049 [US3] Add translation caching mechanism to avoid repeated API calls
- [ ] T050 [US3] Ensure translated content maintains formatting and structure

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Access Reusable Intelligence Tools (Priority: P4)

**Goal**: Provide users with AI-powered tools like glossary generator, chapter summarizer, and personalized tutor

**Independent Test**: User can access and use AI-powered tools like glossary generator, chapter summarizer, or personalized tutor.

### Implementation for User Story 4

- [ ] T051 [US4] Create glossary generator skill in skills/glossary_generator.py
- [ ] T052 [US4] Create chapter summarizer skill in skills/chapter_summarizer.py
- [ ] T053 [US4] Create personalized tutor skill in skills/personalized_tutor.py
- [ ] T054 [US4] Implement /skills/glossary endpoint in backend/src/api/skill_routes.py
- [ ] T055 [US4] Implement /skills/summarize endpoint in backend/src/api/skill_routes.py
- [ ] T056 [US4] Implement /skills/tutor endpoint in backend/src/api/skill_routes.py
- [ ] T057 [US4] Create UI components for skills in book/src/components/SkillsPanel.tsx
- [ ] T058 [US4] Integrate glossary generator with frontend UI
- [ ] T059 [US4] Integrate chapter summarizer with frontend UI
- [ ] T060 [US4] Integrate personalized tutor with frontend UI
- [ ] T061 [US4] Add reasoning agent in agents/reasoning_agent.py to coordinate skills
- [ ] T062 [US4] Connect skills to user context and preferences

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T063 [P] Documentation updates in each component directory including README.md for book/, backend/, agents/, skills/, db/, pipelines/
- [ ] T064 Code cleanup and refactoring for deterministic, modular, readable code across all modules
- [ ] T065 Performance optimization to meet latency targets ≤ 1.5s for RAG queries
- [ ] T066 [P] Add comprehensive unit tests in backend/tests/ and book/src/tests/
- [ ] T067 Security hardening to ensure sensitive data stored only in Postgres/Qdrant
- [ ] T068 Generate ADR if significant architectural decisions were made during implementation
- [ ] T069 Run quickstart.md validation to ensure smooth setup experience
- [ ] T070 Add proper logging and monitoring setup
- [ ] T071 Performance testing to validate 95% response rate within 5 seconds
- [ ] T072 Accessibility improvements for the book content and UI components
- [ ] T073 UI/UX refinements for better user experience
- [ ] T074 Final integration testing across all user stories
- [ ] T075 Prepare deployment configurations for production environment

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create BookContent model in backend/src/models/book_content.py"
Task: "Create ChatSession and ChatMessage models in backend/src/models/chat_models.py"

# Launch all services for User Story 1 together:
Task: "Implement BookService in backend/src/services/book_service.py"
Task: "Implement ChatService in backend/src/services/chat_service.py"

# Launch all components for User Story 1 together:
Task: "Create React chatbot widget component in book/src/components/ChatbotWidget.tsx"
Task: "Create RAG agent in agents/rag_agent.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence