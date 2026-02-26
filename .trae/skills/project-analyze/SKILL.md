---
name: project-analyze
description: Analyze project structure, tech stack, and health. Use when onboarding, exploring a new codebase, or checking project stats.
---

# Project Analyze

This skill provides a comprehensive analysis of the current project state.

## Capabilities

### 1. Tech Stack Overview

Analyze `package.json` to identify:

- Frameworks (Next.js, React, Electron)
- UI Libraries (Tailwind, Radix)
- State Management (Zustand, Redux)
- Build Tools (TypeScript, Vite, Webpack)

### 2. Project Structure Map

Analyze the directory structure (ignoring node_modules, .git) to map:

- Source Root (`src/`, `app/`, `pages/`)
- Configuration Files (`.openspec`, `tsconfig.json`)
- Documentation (`docs/`, `openspec/`)

### 3. OpenSpec Status

Check `openspec/` directory:

- List active changes in `openspec/changes`
- Summarize latest specs in `openspec/specs`

### 4. Code Stats (Optional)

Count lines of code or file types if requested.

## Usage

1.  **Run Analysis**: Use `LS` and `Read` tools to gather info.
2.  **Generate Report**: Output a structured markdown report.
    - **Tech Stack**: List versions of key deps.
    - **Structure**: Tree view of key directories.
    - **Health**: Check for missing config files or deprecated patterns.
