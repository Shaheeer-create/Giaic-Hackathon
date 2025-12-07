---
id: 1
title: Create-Project-Constitution
stage: constitution
date: 2025-01-07
surface: agent
model: Qwen
feature: none
branch: main
user: user
command: /sp.constitution
labels: [constitution, spec-driven-development, ai-textbook]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

```
/sp.constitution # Project Constitution
Project Name: Physical AI & Humanoid Robotics – AI-Native Textbook with RAG Tutor
Version: 1.0.0
Ratified On: 2025-___-___

---

## 1. Purpose & Mission

This project exists to create an **AI-native technical textbook** for teaching
**Physical AI & Humanoid Robotics**, delivered as a **Docusaurus-based website**
with an **embedded Retrieval-Augmented Generation (RAG) AI tutor**.

The project must:
- Teach Physical AI concepts clearly from beginner to advanced level
- Follow the official hackathon course structure and outcomes
- Act as a production-quality learning platform, not static notes
- Demonstrate Spec-Driven Development using Spec-Kit Plus

---

## 2. Non-Negotiable Principles

1. **Spec-Driven First**
   - No chapter, feature, or code is written without a clear specification.
   - Constitution → Specification → Plan → Tasks → Implementation is mandatory.

2. **Educational Clarity Over Complexity**
   - Content must be understandable by a motivated student.
   - Prefer clear explanations, diagrams, and examples over academic jargon.

3. **AI-Native by Design**
   - The AI tutor is a core feature, not an add-on.
   - All content must be structured for Retrieval-Augmented Generation (RAG).

4. **Source-Truth Enforcement**
   - The chatbot must answer **only from textbook content**.
   - No hallucinations, no external guessing.

5. **Reusability & Intelligence Capture**
   - Prompts, agent behaviors, and structures must be reusable.
   - Reusable intelligence is an explicit success criterion.

---

## 3. Mandatory Technology Stack

These technologies are **required** and cannot be substituted:

### Textbook Platform
- Docusaurus
- Markdown (AI-generated but human-reviewed)
- GitHub Pages or Vercel for deployment

### AI & Backend
- OpenAI Agents SDK / ChatKit SDK
- FastAPI (backend API service)
- Neon Serverless PostgreSQL (metadata & auth storage)
- Qdrant Cloud (vector database for embeddings)

### AI Authoring
- Claude Code
- Spec-Kit Plus (for constitution, specs, plans, tasks)

---

## 4. Content Structure Rules

1. The textbook **must follow the official hackathon syllabus**, including:
   - Physical AI foundations
   - ROS 2
   - Gazebo & simulation
   - NVIDIA Isaac
   - Vision-Language-Action (VLA)
   - Capstone humanoid project

2. Every chapter must include:
   - Learning objectives
   - Concept explanation
   - Practical examples
   - AI-answerable structure (RAG-friendly)

3. Chapters must be modular and independently queryable by the AI tutor.

---

## 5. RAG Chatbot Rules

1. The chatbot must:
   - Answer questions strictly from the book's indexed content
   - Support answering questions from user-selected text
   - Use embeddings stored in Qdrant

2. The chatbot must NOT:
   - Generate answers outside textbook scope
   - Invent robotics facts not present in the book

3. All chatbot behavior must be testable and explainable.

---

## 6. Personalization & Localization (Bonus Scope)

If implemented, personalization must:
- Ask learner background during signup
- Adapt explanations (beginner / intermediate)
- Be deterministic and explainable

If translation is implemented:
- Urdu translation must preserve technical meaning
- Original English remains the source of truth

---

## 7. Quality Standards

### Content
- No placeholder text
- No unexplained acronyms
- Consistent terminology across chapters

### Code
- Clear folder structure
- Explicit configuration (no hardcoded secrets)
- Graceful error handling

### AI Output
- Prompt logic must be documented
- Agent behavior must be deterministic when possible

---

## 8. Definition of Done (Global)

The project is considered complete only when:

- ✅ Textbook is published and accessible online
- ✅ RAG chatbot is embedded and functional
- ✅ Chatbot answers are sourced from book content
- ✅ Core syllabus chapters are implemented
- ✅ GitHub repository is public and structured
- ✅ Demo video (≤ 90 seconds) is prepared

---

## 9. Governance & Changes

- This constitution is **binding** for the entire project.
- Changes to this document require:
  - A version bump
  - Justification
  - Explicit ratification via `/sp.constitution`

No implementation may violate this constitution.
```

## Response snapshot

I've successfully created the project constitution for "Physical AI & Humanoid Robotics – AI-Native Textbook with RAG Tutor" as requested. The constitution includes:

1. Core principles for spec-driven development, educational clarity, AI-native design, source-truth enforcement, and reusability
2. Mandatory technology stack requirements
3. Content structure rules following the hackathon syllabus
4. RAG chatbot rules ensuring answers come only from textbook content
5. Personalization and localization guidelines
6. Quality standards for content, code, and AI output
7. Definition of Done criteria
8. Governance rules for amendments

The constitution file has been saved to `.specify/memory/constitution.md` with version 1.0.0.

## Outcome

- ✅ Impact: Created foundational project constitution that will guide all development
- 🧪 Tests: N/A for this documentation task
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: N/A
- 🧠 Reflection: The constitution clearly establishes the project's non-negotiable principles and technical requirements.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A