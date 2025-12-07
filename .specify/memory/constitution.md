<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.0.0 (initial creation)
Modified principles: N/A (new document)
Added sections: All sections (initial creation)
Removed sections: N/A
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: RATIFICATION_DATE needs to be finalized
-->
# Physical AI & Humanoid Robotics – AI-Native Textbook with RAG Tutor Constitution

## Core Principles

### Spec-Driven First
No chapter, feature, or code is written without a clear specification. Constitution → Specification → Plan → Tasks → Implementation is mandatory.

### Educational Clarity Over Complexity
Content must be understandable by a motivated student. Prefer clear explanations, diagrams, and examples over academic jargon.

### AI-Native by Design
The AI tutor is a core feature, not an add-on. All content must be structured for Retrieval-Augmented Generation (RAG).

### Source-Truth Enforcement
The chatbot must answer **only from textbook content**. No hallucinations, no external guessing.

### Reusability & Intelligence Capture
Prompts, agent behaviors, and structures must be reusable. Reusable intelligence is an explicit success criterion.

### Mandatory Technology Stack
These technologies are **required** and cannot be substituted:
- Docusaurus for textbook platform
- Markdown (AI-generated but human-reviewed)
- GitHub Pages or Vercel for deployment
- OpenAI Agents SDK / ChatKit SDK for AI
- FastAPI (backend API service)
- Neon Serverless PostgreSQL (metadata & auth storage)
- Qdrant Cloud (vector database for embeddings)
- Claude Code for AI authoring
- Spec-Kit Plus (for constitution, specs, plans, tasks)

## Content Structure Rules
The textbook **must follow the official hackathon syllabus**, including:
- Physical AI foundations
- ROS 2
- Gazebo & simulation
- NVIDIA Isaac
- Vision-Language-Action (VLA)
- Capstone humanoid project

Every chapter must include:
- Learning objectives
- Concept explanation
- Practical examples
- AI-answerable structure (RAG-friendly)

Chapters must be modular and independently queryable by the AI tutor.

## RAG Chatbot Rules
The chatbot must:
- Answer questions strictly from the book's indexed content
- Support answering questions from user-selected text
- Use embeddings stored in Qdrant

The chatbot must NOT:
- Generate answers outside textbook scope
- Invent robotics facts not present in the book

All chatbot behavior must be testable and explainable.

## Personalization & Localization (Bonus Scope)
If implemented, personalization must:
- Ask learner background during signup
- Adapt explanations (beginner / intermediate)
- Be deterministic and explainable

If translation is implemented:
- Urdu translation must preserve technical meaning
- Original English remains the source of truth

## Quality Standards
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

## Definition of Done (Global)
The project is considered complete only when:
- ✅ Textbook is published and accessible online
- ✅ RAG chatbot is embedded and functional
- ✅ Chatbot answers are sourced from book content
- ✅ Core syllabus chapters are implemented
- ✅ GitHub repository is public and structured
- ✅ Demo video (≤ 90 seconds) is prepared

## Governance
This constitution is **binding** for the entire project. Changes to this document require:
- A version bump
- Justification
- Explicit ratification via `/sp.constitution`

No implementation may violate this constitution. All PRs/reviews must verify compliance.

**Version**: 1.0.0 | **Ratified**: 2025-01-07 | **Last Amended**: 2025-01-07