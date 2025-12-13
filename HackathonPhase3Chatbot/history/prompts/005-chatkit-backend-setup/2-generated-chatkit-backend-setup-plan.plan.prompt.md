---
id: 2
title: Generated ChatKit Backend Setup Plan
stage: plan
date: 2025-12-14
surface: agent
model: unknown
feature: 005-chatkit-backend-setup
branch: 005-chatkit-backend-setup
user: Ahmed
command: /sp.plan
labels: ["planning", "backend-setup"]
links:
  spec: specs/005-chatkit-backend-setup/spec.md
  plan: specs/005-chatkit-backend-setup/plan.md
  ticket: null
  adr: null
  pr: null
files:
- specs/005-chatkit-backend-setup/plan.md
- specs/005-chatkit-backend-setup/research.md
- specs/005-chatkit-backend-setup/data-model.md
- specs/005-chatkit-backend-setup/quickstart.md
- specs/005-chatkit-backend-setup/contracts/README.md
tests: []
---

## Prompt

```text
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/setup-plan.ps1 -Json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType gemini`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications
```

## Response snapshot

Successfully executed the implementation planning workflow for the "ChatKit Backend Setup" feature (005-chatkit-backend-setup). The `plan.md` file was generated and updated with technical context, constitution check, and project structure. All "NEEDS CLARIFICATION" markers were resolved. The following artifacts were created: `research.md`, `data-model.md`, `quickstart.md`, and `contracts/README.md`. The agent context was also updated.

## Outcome

- ✅ Impact: Implementation plan for ChatKit backend setup generated.
- 🧪 Tests: N/A - planning task.
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/README.md.
- 🔁 Next prompts: User to proceed with /sp.tasks.
- 🧠 Reflection: Successfully executed planning workflow. Continued to face issues with PHR script, necessitating manual creation.

## Evaluation notes (flywheel)

- Failure modes observed: Non-existent PHR script.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment: Further investigate PHR script issue.
