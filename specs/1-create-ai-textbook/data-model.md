# Data Model: AI-Native Textbook

**Feature**: AI-Native Textbook using Docusaurus
**Date**: 2025-01-07

## Overview

This document defines the data model for the AI-Native Textbook on Physical AI & Humanoid Robotics. Since this is primarily a content-focused documentation site, the "data model" consists of the content structure and metadata needed to organize and retrieve the educational material.

## Content Entities

### Textbook
- **Description**: The complete educational resource
- **Fields**:
  - `id`: Unique identifier for the textbook
  - `title`: "Physical AI & Humanoid Robotics"
  - `subtitle`: "An AI-Native Technical Textbook"
  - `description`: Description of the textbook
  - `syllabus`: Reference to the official hackathon syllabus
  - `version`: Current version of the textbook
  - `lastUpdated`: Timestamp of last content update
  - `chapters`: Array of Chapter entities

### Chapter
- **Description**: Major sections of the textbook
- **Fields**:
  - `id`: Chapter identifier (e.g., "chapter-01-introduction")
  - `number`: Sequential number (1-8)
  - `title`: Chapter title
  - `description`: Brief overview of the chapter
  - `goal`: Learning goal for the chapter
  - `lessons`: Array of Lesson entities
  - `learningObjectives`: Array of learning objectives
  - `prerequisites`: Array of prerequisite topics
  - `relatedChapters`: Array of related chapter IDs

### Lesson
- **Description**: Individual units within chapters
- **Fields**:
  - `id`: Lesson identifier (e.g., "lesson-1-what-is-physical-ai")
  - `number`: Sequential number within the chapter
  - `title`: Lesson title
  - `content`: The markdown content of the lesson
  - `learningObjectives`: Array of specific learning objectives
  - `examples`: Array of examples or illustrations
  - `keyTakeaways`: Array of key takeaways
  - `durationEstimate`: Estimated time to complete lesson
  - `difficulty`: Beginner/Intermediate/Advanced
  - `relatedLessons`: Array of related lesson IDs

### ContentBlock
- **Description**: Individual content elements within lessons
- **Fields**:
  - `id`: Unique identifier for the content block
  - `type`: Type of content (text, code, image, video, etc.)
  - `content`: The actual content
  - `title`: Optional title for the content block
  - `position`: Position within the lesson

### LearningObjective
- **Description**: Specific learning goals
- **Fields**:
  - `id`: Unique identifier
  - `text`: The learning objective statement
  - `level`: Cognitive level (Remember, Understand, Apply, Analyze, Evaluate, Create)
  - `relatedContent`: Reference to content that addresses this objective

## Metadata Entities

### Author
- **Description**: Content author information
- **Fields**:
  - `id`: Unique identifier
  - `name`: Author name
  - `role`: Role (primary author, reviewer, etc.)

### Review
- **Description**: Peer review metadata
- **Fields**:
  - `id`: Unique identifier
  - `lessonId`: Reference to the lesson being reviewed
  - `reviewer`: Reference to the reviewer
  - `date`: Review date
  - `status`: Accepted, needs changes, rejected
  - `comments`: Reviewer comments

## RAG-Specific Entities

### ContentChunk
- **Description**: Text segments optimized for RAG retrieval
- **Fields**:
  - `id`: Unique identifier
  - `content`: The text chunk
  - `sourceLesson`: Reference to the source lesson
  - `sourceChapter`: Reference to the source chapter
  - `keywords`: Array of keywords for retrieval
  - `embedding`: Vector embedding (computed later)
  - `sectionHeading`: The heading under which this chunk appears

### KnowledgeGraphEntity
- **Description**: Entities extracted for knowledge graph
- **Fields**:
  - `id`: Unique identifier
  - `name`: Entity name
  - `type`: Entity type (concept, technique, tool, etc.)
  - `description`: Brief description of the entity
  - `relatedEntities`: Array of related entity IDs
  - `mentionedIn`: Array of content IDs where the entity is mentioned

## Validation Rules

### Content Structure Validation
- Each lesson must include learning objectives, concept explanation, examples, and key takeaways
- Chapter titles must match the official hackathon syllabus
- All content must be written in Markdown format
- Each chapter must have a clear learning goal
- Content chunks must not exceed 500 words for optimal RAG performance

### Cross-Reference Validation
- All referenced chapters must exist
- All referenced lessons must exist
- All prerequisites must be covered in earlier chapters or be external knowledge
- Learning objectives must be addressed by content within the same chapter/lesson

### RAG Optimization Validation
- All content must have clear, hierarchical headings
- Content chunks must maintain semantic coherence
- Keywords for retrieval must be relevant to the content
- No off-topic content or unsourced claims

## State Transitions

### Content State
```
Draft → Review → Approved → Published → Archived
```

- **Draft**: Content is being authored
- **Review**: Content is under peer review
- **Approved**: Content has passed review, awaiting publication
- **Published**: Content is live and accessible
- **Archived**: Content is no longer current but preserved for reference

### Lesson State
```
Outline → In Progress → Review → Complete
```

- **Outline**: Basic structure defined
- **In Progress**: Content is being written
- **Review**: Ready for review
- **Complete**: Finalized and approved