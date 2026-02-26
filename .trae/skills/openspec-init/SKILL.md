---
name: 'openspec-init'
description: 'Initialize OpenSpec workflow structure and governance files in a new project. Use this to set up the spec-driven environment with one click.'
---

# OpenSpec Init

**Description:** Initialize the OpenSpec workflow in a new project. Creates directory structure, templates, and governance rules.

**Details:**

This skill sets up the "Spec-Driven" development environment.

## 1. Directory Structure

The skill will ensure the following directories exist:

- `openspec/specs` (The "Truth" - System state)
- `openspec/changes` (The "Diff" - Proposed changes)
- `openspec/templates` (Templates for specs and changes)
- `.trae/rules` (Agent instructions)

## 2. Core Files Generation

The skill will generate the following files with "Best Practice" content:

1.  **`openspec/specs/project-governance/spec.md`**
    - Defines the "Native Language Principle" (Chinese First).
    - Defines the "OpenSpec Workflow" (Proposal -> Specs -> Design -> Tasks).

2.  **`openspec/templates/change-template.md`**
    - A standardized template for creating new changes (Context, Problem, Solution, Tasks).

3.  **`.trae/rules/Core-OpenSpec.md`**
    - Instructions for the Agent to strictly follow the OpenSpec workflow.

## 3. How to Execute (Instructions for Agent)

When you (the Agent) are asked to run this skill, you MUST perform the following actions:

### Step 1: Create Directories

Run:

```bash
mkdir -p openspec/specs/project-governance openspec/changes openspec/templates .trae/rules
```

### Step 2: Create Governance Spec

Write to `openspec/specs/project-governance/spec.md`:

```markdown
# Project Governance

## 1. 母语原则 (Native Language Principle)

- **核心规则**：所有沟通、文档、代码注释、Commit Message 必须优先使用中文。
- **专业术语**：保留专业术语的英文原文（如 OpenSpec, Next.js），避免过度翻译。

## 2. OpenSpec 工作流 (Workflow)

- **核心理念**：Spec-Driven Development (SDD)。
- **流程**：
  1. **Proposal**: 提出变更想法。
  2. **Specs**: 修改 `openspec/specs` 中的状态文档，描述"变更后"的系统样子。
  3. **Design**: 技术设计与实现方案。
  4. **Tasks**: 生成具体的 Task 列表。
```

### Step 3: Create Change Template

Write to `openspec/templates/change-template.md`:

```markdown
# Change: <Title>

## Context

<背景描述>

## Problem

<当前问题>

## Solution

<解决方案>

## Tasks

- [ ] Task 1
- [ ] Task 2
```

### Step 4: Create Agent Rule

Write to `.trae/rules/Core-OpenSpec.md`:

```markdown
# Core-OpenSpec

## 1. OpenSpec First

- Do not modify code without an OpenSpec change artifact.
- Update `openspec/specs` before writing code.
```

### Step 5: Verification

Run `ls -R openspec` to verify the structure.
