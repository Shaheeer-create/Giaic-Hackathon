# Data Model: Documentation Location Constraint

**Feature**: Update Documentation Location Constraint
**Date**: 2025-01-07

## Overview

This document defines the data model for enforcing documentation location constraints within the Docusaurus-based AI-Native Textbook. The model focuses on content organization, file placement, and navigation structure to ensure all content resides within the `/docs` directory.

## Content Entities

### TextbookContent
- **Description**: The educational material that must be organized within the `/docs` directory
- **Fields**:
  - `id`: Unique identifier for the content
  - `title`: Title of the content piece
  - `path`: Path relative to `/docs` directory
  - `type`: Content type (Chapter, Lesson, Intro, etc.)
  - `format`: File format (.md or .mdx)
  - `status`: Validation status (Valid, Invalid, Pending)

### ChapterDirectory
- **Description**: Subfolders within `/docs` that contain related lessons
- **Fields**:
  - `id`: Unique identifier for the chapter directory
  - `name`: Name of the directory (e.g., "chapter-01-introduction")
  - `path`: Full path relative to project root (should be `/docs/[name]`)
  - `lessons`: List of lesson files contained in this directory
  - `categoryConfig`: Path to `_category_.json` file for this chapter

### LessonFile
- **Description**: Individual `.md` or `.mdx` files containing specific educational content
- **Fields**:
  - `id`: Unique identifier for the lesson file
  - `filename`: Name of the file including extension
  - `path`: Full path relative to project root (should be under `/docs`)
  - `frontmatter`: Metadata contained in the file's frontmatter
  - `contentStructure`: Validation of required content elements (objectives, explanations, examples, takeaways)

### NavigationLink
- **Description**: Reference to content in sidebar navigation system
- **Fields**:
  - `id`: Unique identifier for the navigation link
  - `label`: Display text for the navigation item
  - `path`: Path referenced by the navigation (should be under `/docs`)
  - `type`: Link type (generated-index, doc, etc.)
  - `valid`: Whether the path points to valid content within `/docs`

## Validation Rules

### Content Placement Validation
- All content items must have paths starting with `/docs/`
- Lesson files must be within a chapter directory under `/docs`
- No content items should have paths outside the `/docs` directory

### Navigation Integrity Validation
- All navigation links must reference paths within the `/docs` directory
- Navigation references must point to existing content files
- Navigation structure should match the actual directory organization

### Format Compliance Validation
- All lesson files must have `.md` or `.mdx` extension
- Content format must be compatible with Docusaurus processing
- Frontmatter in lesson files must follow Docusaurus standards

## State Transitions

### Content Validation State
```
Unverified → Valid | Invalid
```

- **Unverified**: Content exists but hasn't been validated against location rules
- **Valid**: Content is properly located within `/docs` directory structure
- **Invalid**: Content is located outside `/docs` directory or violates location rules

### Migration State
```
OriginalLocation → MigratedToDocs → Validated
```

- **OriginalLocation**: Content in its original location (may be outside `/docs`)
- **MigratedToDocs**: Content moved to appropriate location under `/docs`
- **Validated**: Migrated content confirmed to meet all location constraints