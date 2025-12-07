# Quickstart Guide: AI-Native Textbook Development

**Feature**: AI-Native Textbook using Docusaurus
**Date**: 2025-01-07

## Overview

This guide provides instructions for setting up the development environment and beginning work on the AI-Native Textbook on Physical AI & Humanoid Robotics.

## Prerequisites

- Node.js (version 18 or higher)
- npm or yarn package manager
- Git
- A code editor (VS Code recommended)
- GitHub account

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Dependencies

```bash
npm install
# or
yarn install
```

### 3. Initialize Docusaurus

The project is already configured with Docusaurus, but if setting up from scratch:

```bash
npm init docusaurus@latest docs-website classic
```

### 4. Start Development Server

```bash
npm run start
# or
yarn start
```

This will start a local development server at `http://localhost:3000`.

## Project Structure

```
docs/
├── chapter-01-introduction/
├── chapter-02-sensors/
├── chapter-03-ros2/
├── chapter-04-simulation/
├── chapter-05-nvidia-isaac/
├── chapter-06-humanoid-robots/
├── chapter-07-vla/
├── chapter-08-capstone/
├── _category_.json
└── intro.md
docusaurus.config.js
package.json
sidebars.js
static/
src/
└── pages/
```

## Writing Content

### 1. Content Structure

Each lesson must follow this structure:

```markdown
---
title: Lesson Title
sidebar_position: [position number]
description: Brief description of the lesson
---

# Lesson Title

## Learning Objectives

- Objective 1
- Objective 2
- Objective 3

## Content

[Main content with clear headings and explanations]

## Examples

[Practical examples or illustrations]

## Key Takeaways

- Takeaway 1
- Takeaway 2
- Takeaway 3
```

### 2. Adding New Content

To add a new lesson:

1. Create a new `.md` file in the appropriate chapter directory
2. Use the naming convention: `lesson-[number]-[topic].md`
3. Add the proper frontmatter as shown above
4. Update `sidebars.js` to include the new lesson in the navigation

### 3. Creating New Chapters

1. Create a new directory in `docs/` with the naming convention: `chapter-[number]-[topic]`
2. Add an `_category_.json` file to define the category:
   ```json
   {
     "label": "Chapter Title",
     "position": [number],
     "link": {
       "type": "generated-index",
       "description": "Chapter description"
     }
   }
   ```
3. Add lessons to the chapter directory

## Development Workflow

### Content Creation Process

1. **Outline Creation**: Create lesson outline with learning objectives
2. **Draft Writing**: Write initial content draft
3. **Peer Review**: Submit for peer review using the PR process
4. **Revision**: Incorporate review feedback
5. **Approval**: Approval by project maintainers
6. **Publication**: Merge to main branch for publication

### Quality Standards

- All content must meet WCAG 2.1 AA accessibility standards
- No placeholder text is allowed
- Consistent terminology across all chapters and lessons
- Each lesson must include learning objectives, explanations, examples, and key takeaways
- Content must follow the official hackathon syllabus

### RAG Optimization Guidelines

- Use clear, descriptive headings
- Structure content with semantic sections
- Maintain consistent formatting
- Include relevant keywords naturally
- Ensure content is self-contained and can be understood independently

## Deployment

### Local Testing

```bash
npm run build
npm run serve
```

### Production Deployment

The site is automatically deployed to GitHub Pages or Vercel when content is merged to the main branch.

1. Ensure all content is reviewed and approved
2. Create a pull request
3. Upon approval, merge to main branch
4. The CI/CD pipeline will handle deployment automatically

## Best Practices

- Write for your audience: motivated students with varying technical backgrounds
- Use clear, concise language and avoid jargon where possible
- Include practical examples and illustrations
- Structure content for easy navigation and understanding
- Ensure all content is RAG-friendly with proper headings and sections
- Maintain consistent terminology across the entire textbook