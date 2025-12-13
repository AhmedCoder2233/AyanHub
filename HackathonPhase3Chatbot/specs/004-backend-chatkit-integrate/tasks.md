# Tasks: ChatKit UI Enhancement & AI Service Integration

**Input**: Design documents from `/specs/004-backend-chatkit-integrate/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/chat_api.yaml

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend folder at `backend/`
- [ ] T002 Initialize Python project in `backend/` using `uv init` in `backend/pyproject.toml`
- [ ] T003 Add core backend dependencies (`fastapi`, `uvicorn`, `openai`, `python-dotenv`) to `backend/pyproject.toml`
- [ ] T004 Create `main.py` in `backend/src/api/main.py` as the entry point for the FastAPI application.
- [ ] T005 Configure CORS middleware in `backend/src/api/main.py` for `http://localhost:3000`.
- [ ] T006 Create initial directory structure for backend: `backend/src/models/`, `backend/src/services/`, `backend/tests/`.
- [ ] T007 Create initial directory structure for frontend: `frontend/src/components/`, `frontend/src/pages/`, `frontend/src/services/`, `frontend/tests/`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Define environment variable loading for `OPENAI_API_KEY` in `backend/.env` and `backend/src/api/main.py`.
- [ ] T009 Initialize OpenAI client in `backend/src/services/openai_service.py` using `OPENAI_API_KEY`.
- [ ] T010 Implement a basic database service/client in `backend/src/services/database_service.py` for interaction with conversation history (as per Constitution).

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Send Message and Receive AI Response (Priority: P1) 🎯 MVP

**Goal**: A user can send a message and receive an AI-generated response.

**Independent Test**: The user can open the chat interface, type a message, send it, and observe a response appearing in the chat window. This can be tested end-to-end (client to AI service).

### Implementation for User Story 1

- [ ] T011 [P] [US1] Define `User` model in `backend/src/models/user.py` (based on `data-model.md`).
- [ ] T012 [P] [US1] Define `Conversation` model in `backend/src/models/conversation.py` (based on `data-model.md`).
- [ ] T013 [P] [US1] Define `Message` model in `backend/src/models/message.py` (based on `data-model.md`).
- [ ] T014 [US1] Create a `ConversationService` in `backend/src/services/conversation_service.py` to handle conversation creation and retrieval (using `database_service`).
- [ ] T015 [US1] Create a `MessageService` in `backend/src/services/message_service.py` to handle message storage and retrieval (using `database_service`).
- [ ] T016 [US1] Implement `chat` endpoint logic in `backend/src/api/main.py` to handle `POST /api/{user_id}/chat` requests.
- [ ] T017 [US1] In `backend/src/api/main.py`'s `chat` endpoint, extract `user_id` from path and message/`conversation_id` from request body.
- [ ] T018 [US1] In `backend/src/api/main.py`'s `chat` endpoint, use `ConversationService` to get/create conversation.
- [ ] T019 [US1] In `backend/src/api/main.py`'s `chat` endpoint, store user message using `MessageService`.
- [ ] T020 [US1] In `backend/src/api/main.py`'s `chat` endpoint, call `OpenAIService` to generate AI response.
- [ ] T021 [US1] In `backend/src/api/main.py`'s `chat` endpoint, store AI response using `MessageService`.
- [ ] T022 [US1] In `backend/src/api/main.py`'s `chat` endpoint, return AI response in the specified contract format.
- [ ] T023 [US1] Implement basic UI for sending messages and displaying responses in `frontend/src/pages/chat_page.tsx`.
- [ ] T024 [P] [US1] Create a `ChatService` in `frontend/src/services/chat_service.ts` to interact with the backend API.
- [ ] T025 [P] [US1] Create `ChatInput` component in `frontend/src/components/chat_input.tsx` for typing and sending messages.
- [ ] T026 [P] [US1] Create `ChatMessage` component in `frontend/src/components/chat_message.tsx` to display individual messages.
- [ ] T027 [P] [US1] Create `ChatWindow` component in `frontend/src/components/chat_window.tsx` to display message history.
- [ ] T028 [US1] Integrate `ChatInput` and `ChatWindow` components into `frontend/src/pages/chat_page.tsx` and connect to `ChatService`.

---

## Phase 4: User Story 2 - Modern and Responsive Chat UI (Priority: P2)

**Goal**: A user interacts with a visually appealing and responsive chat interface.

**Independent Test**: The chat interface can be tested by opening it in various browsers and device form factors (desktop, tablet, mobile) and observing its layout, styling, and interactivity.

### Implementation for User Story 2

- [ ] T029 [P] [US2] Apply modern, clean chat interface styling to `frontend/src/pages/chat_page.tsx` and related components.
- [ ] T030 [P] [US2] Implement full height container with smooth animations in `frontend/src/pages/chat_page.tsx`.
- [ ] T031 [P] [US2] Ensure professional color scheme and typography are applied across `frontend/src/pages/chat_page.tsx` and components.
- [ ] T032 [P] [US2] Implement responsive design for `frontend/src/pages/chat_page.tsx` and components for various screen sizes.
- [ ] T033 [P] [US2] Ensure proper spacing and padding in `frontend/src/pages/chat_page.tsx` and components.
- [ ] T034 [P] [US2] Implement smooth transitions and hover effects for interactive elements in `frontend/src/pages/chat_page.tsx`.
- [ ] T035 [US2] Ensure smooth scrolling to new messages in `frontend/src/components/chat_window.tsx`.

---

## Phase 5: User Story 3 - Secure Credential Handling for AI Service (Priority: P2)

**Goal**: The system securely manages and uses credentials for the AI service without exposing them.

**Independent Test**: This can be tested by verifying that sensitive credentials are not hardcoded or exposed within the system.

### Implementation for User Story 3

- [ ] T036 [US3] Implement secure loading of `OPENAI_API_KEY` from environment variables in `backend/src/services/openai_service.py`.
- [ ] T037 [US3] Ensure `OPENAI_API_KEY` is not hardcoded or exposed in any client-side code.
- [ ] T038 [US3] Verify that the backend allows client applications to interact from authorized origins (`http://localhost:3000`) through CORS configuration in `backend/src/api/main.py`.

---

## Final Phase: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T039 Implement comprehensive error handling and logging for backend services (e.g., `backend/src/services/error_handler.py`).
- [ ] T040 Implement loading states and error handling UI in `frontend/src/pages/chat_page.tsx` for network requests.
- [ ] T041 Review and refactor code for maintainability and best practices across the feature.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

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
- [ ] T011 [P] [US1] Define `User` model in `backend/src/models/user.py`
- [ ] T012 [P] [US1] Define `Conversation` model in `backend/src/models/conversation.py`
- [ ] T013 [P] [US1] Define `Message` model in `backend/src/models/message.py`
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
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently
