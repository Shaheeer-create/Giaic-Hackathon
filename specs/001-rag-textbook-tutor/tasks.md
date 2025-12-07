---

description: "Task list for RAG Backend System implementation"
---

# Tasks: RAG Backend System (Gemini-Based Agents) for Physical AI & Humanoid Robotics Textbook Tutor

**Input**: Design documents from `/specs/001-rag-textbook-tutor/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The feature specification requests validation and testing capabilities, so we include test tasks where appropriate.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/` structure, following plan.md structure

<!--
  ============================================================================
  ACTUAL TASKS based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure per implementation plan
- [x] T002 Initialize Python project with pyproject.toml and required dependencies
- [x] T003 [P] Create .env.example file with all required environment variables
- [x] T004 [P] Configure linting and formatting tools (ruff, black, mypy)
- [x] T005 Create initial README.md with project overview and setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Setup Qdrant client connection in backend/app/db/qdrant_client.py
- [x] T007 Setup Neon PostgreSQL connection and basic models in backend/app/db/neon.py
- [x] T008 [P] Configure FastAPI application in backend/app/main.py
- [x] T009 [P] Create configuration and settings management in backend/app/core/config.py and backend/app/core/settings.py
- [x] T010 Create utility functions for text cleaning in backend/app/utils/text_cleaner.py
- [x] T011 Create utility functions for semantic chunking in backend/app/utils/chunking.py
- [x] T012 Setup logging infrastructure with configurable log levels
- [x] T013 Configure error handling and response formatting infrastructure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Query Textbook Content (Priority: P1) 🎯 MVP

**Goal**: Enable students to ask questions about the textbook and receive accurate answers based on indexed content, with the system refusing to answer when no relevant content exists.

**Independent Test**: Can be fully tested by submitting textbook-related questions and verifying that responses are accurate and grounded in the indexed textbook content.

### Tests for User Story 1 (OPTIONAL - included based on requirements) ⚠️

- [ ] T014 [P] [US1] Contract test for POST /query endpoint in backend/tests/contract/test_query_contract.py
- [ ] T015 [P] [US1] Integration test for query flow in backend/tests/integration/test_query_flow.py

### Implementation for User Story 1

- [x] T016 [P] [US1] Create Query entity model in backend/app/db/models.py
- [x] T017 [P] [US1] Create GeneratedAnswer entity model in backend/app/db/models.py
- [x] T018 [P] [US1] Create RetrievedContext entity model in backend/app/db/models.py
- [x] T019 [P] [US1] Create ConfidenceMetadata entity model in backend/app/db/models.py
- [x] T020 [US1] Implement Tutor Agent with Gemini integration in backend/app/agents/tutor_agent.py
- [x] T021 [US1] Implement retrieval service in backend/app/rag/retriever.py
- [x] T022 [US1] Implement generation service in backend/app/rag/generator.py
- [x] T023 [US1] Implement query endpoint in backend/app/api/routes.py
- [x] T024 [US1] Add validation for query input and confidence threshold
- [x] T025 [US1] Implement logic to refuse answers when no relevant content exists

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Ingest Textbook Content (Priority: P2)

**Goal**: Allow administrators to add or update textbook content in the system, with content being properly indexed for future retrieval.

**Independent Test**: Can be fully tested by ingesting sample textbook content and verifying that it is properly stored and retrievable for future queries.

### Tests for User Story 2 (OPTIONAL - included based on requirements) ⚠️

- [ ] T026 [P] [US2] Contract test for POST /ingest endpoint in backend/tests/contract/test_ingest_contract.py
- [ ] T027 [P] [US2] Integration test for ingestion flow in backend/tests/integration/test_ingestion_flow.py

### Implementation for User Story 2

- [x] T028 [P] [US2] Create TextbookContent entity model in backend/app/db/models.py
- [x] T029 [P] [US2] Create DocumentChunk entity model in backend/app/db/models.py
- [x] T030 [P] [US2] Create Embedding entity model in backend/app/db/models.py
- [x] T031 [US2] Implement ingestion service in backend/app/rag/ingestion.py
- [x] T032 [US2] Implement embedding service using Cohere in backend/app/rag/embeddings.py
- [x] T033 [US2] Implement ingest endpoint in backend/app/api/routes.py
- [x] T034 [US2] Add validation and normalization for incoming content
- [x] T035 [US2] Implement semantic chunking logic in backend/app/rag/ingestion.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Retrieve Contextually Relevant Information (Priority: P3)

**Goal**: Efficiently search through indexed textbook content to find the most relevant information for a given query.

**Independent Test**: Can be tested by submitting various questions and verifying that the system retrieves the most relevant textbook passages for each query.

### Tests for User Story 3 (OPTIONAL - included based on requirements) ⚠️

- [ ] T036 [P] [US3] Contract test for retrieval functionality in backend/tests/contract/test_retrieval_contract.py
- [ ] T037 [P] [US3] Integration test for retrieval accuracy in backend/tests/integration/test_retrieval_accuracy.py

### Implementation for User Story 3

- [x] T038 [US3] Enhance retrieval service with ranking and filtering in backend/app/rag/retriever.py
- [x] T039 [US3] Implement similarity scoring and ranking algorithms
- [x] T040 [US3] Add relevance filtering based on confidence and similarity thresholds
- [x] T041 [US3] Optimize retrieval performance for large content sets
- [x] T042 [US3] Add logging and metrics for retrieval effectiveness

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Agent & RAG Pipeline Integration

**Goal**: Integrate all components into a cohesive RAG pipeline and implement the Tutor Agent for enhanced reasoning.

- [x] T043 [P] Create tools for the agent in backend/app/agents/tools.py
- [x] T044 Implement pipeline orchestration in backend/app/rag/pipeline.py
- [x] T045 Integrate Tutor Agent with retrieval and generation services
- [x] T046 Implement Context7 integration for clarification (without overriding facts)
- [x] T047 Add comprehensive logging for agent reasoning steps

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T048 [P] Documentation updates in backend/README.md
- [x] T049 Add comprehensive API documentation with OpenAPI/Swagger
- [ ] T050 [P] Additional unit tests in backend/tests/unit/
- [ ] T051 Performance optimization for concurrent query handling
- [ ] T052 Security hardening for API endpoints
- [x] T053 Run quickstart validation to ensure setup instructions work correctly
- [x] T054 Add health check endpoint in backend/app/api/routes.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Agent Integration (Phase 6)**: Depends on foundational stories being complete
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on US2 (ingestion) since we need content to retrieve

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Contract test for POST /query endpoint in backend/tests/contract/test_query_contract.py"
Task: "Integration test for query flow in backend/tests/integration/test_query_flow.py"

# Launch all models for User Story 1 together:
Task: "Create Query entity model in backend/app/db/models.py"
Task: "Create GeneratedAnswer entity model in backend/app/db/models.py"
Task: "Create RetrievedContext entity model in backend/app/db/models.py"
Task: "Create ConfidenceMetadata entity model in backend/app/db/models.py"
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
5. Add Agent Integration → Test → Deploy/Demo
6. Add Polish → Final deployment
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
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