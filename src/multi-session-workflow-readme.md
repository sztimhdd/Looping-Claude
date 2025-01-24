# [Project Name] - Multi-Session Development Workflow
Version: 1.0

## Overview
This document describes our incremental development approach for managing complex projects across multiple Claude chat sessions. Our workflow is designed to maintain context, track progress, and enable collaborative AI-assisted development.

## Workflow Process
### 1. Initial Setup
- Upload this README to project content
- Define comprehensive project requirements
- Create initial architecture design
- Generate first session summary

### 2. Project Contents
#### 2.1 Initial Static Contents
- "project-requirements-template" contains the project requirements template needed to generate the actual project requirement documentation
- "multi-session-workflow-readme" contains the incremental development approach for managing complex projects across multiple Claude chat sessions. Our workflow is designed to maintain context, track progress, and enable collaborative AI-assisted development

#### 2.2 Variable Contents (Generated and Uploaded Contents by Human during the workflow)
- "requirements-doc" the generated project requirements
- latest source codes for completed modules
- session summaries from completed chat sessions

### 2. Development Cycle
- Read previous session summary before starting new session
- Implement current module or project phase
- Generate new session summary capturing:
  * Code implementations
  * Interface updates
  * Design decisions
  * Project status
- Upload summary to project content
- Begin next session

### 3. Version Management 
- Content reference format: [module_name]_v[X.Y]
- Track all changes in session summaries
- Maintain clear interface change protocols
- Document design evolution and rationale

## Error Recovery
### Session Interruption Handling
- Comprehensive session summaries serve as recovery points
- Each summary captures complete project state
- Ability to resume work from last stable state

### Rollback Procedures
- Maintain version history in session summaries
- Ability to revert to previous module implementation
- Clear documentation of changes and reasons

### Conflict Resolution
- Explicit documentation of potential conflicts
- Clear communication of interface and design changes
- Mechanism for resolving divergent development paths

## Best Practices
- Always reference previous session summary
- Maintain clear, concise documentation
- Communicate design decisions and rationales
- Anticipate and document potential challenges

## Notes
This workflow is a living document. Adapt and modify as project needs evolve.