# Session Initialization and Continuation Prompts

## Project Initialization Prompt
```markdown
Starting new project development:
Project Name: [Name]
Initial Version: v1.0
Requirements Doc: [Reference]

Project Setup Instructions:
1. Verify all project documents have been uploaded to project content:
   - Requirements specification
   - Design documentation
   - Any reference materials

2. Source Code Initialization:
   - Confirm source code files follow naming convention: [module_name]_v[X.Y].py
   - Verify version numbers are consistent across related artifacts
   - Document any dependencies between artifacts

Version Control Guidelines:
- Major version increments (X.0) for significant architectural changes
- Minor version increments (X.Y) for feature additions/modifications
- All related artifacts must maintain version synchronization
- Document version relationships in session summaries

Project Analysis Request:
- Review all project documentation
- Analyze technical requirements and constraints
- Identify system components and interfaces
- Create initial architecture design
- Plan implementation sequence

Please assist in designing the system architecture and creating the initial session summary. Focus on:
- System component design
- Interface specifications
- Implementation strategy
- Version control approach
```

## Continuation Session Prompt
```markdown
Continuing [Project Name] development
Previous Session: [Session ID]
Previous Version: v[X.Y]
Current Version Target: v[X.Z]
Previous Summary: [Reference]

Version Control Checklist:
1. Confirm all source code version numbers are synchronized
2. Verify artifact relationships are documented
3. Validate version progression is appropriate for changes
4. Ensure all related artifacts are updated together

Source Code Management:
1. Verify all previously generated source code is uploaded
2. Confirm naming convention: [module_name]_v[X.Y].py
3. Document any new artifact dependencies
4. Track interface changes and their impact

Requirements Management:
1. Review any requirement changes from previous session
2. Distinguish between requirement updates vs implementation details
3. Document impact of changes on other components
4. Update requirements doc only for true requirement changes

Implementation Focus:
- Review previous session's progress
- Analyze existing code and interfaces
- Address pending challenges
- Consider impact on related artifacts
- Maintain version synchronization

Session Summary Requirements:
- Document all version changes
- Track artifact relationships
- Detail interface modifications
- Record requirement updates
- List generated source code
- Note implementation progress
- Identify integration points

Important Reminders:
- Upload ALL generated source code after session
- Maintain consistent version numbering
- Document artifact dependencies
- Track interface changes
- Validate requirement updates
```

## Generate Session Summary Prompt
```markdown
Please generate a comprehensive session summary following the template structure. Ensure all key sections are addressed:

1. Session Overview:
   - Implementation focus
   - Version changes
   - Artifact relationships

2. Code Changes:
   - Source code modifications
   - Version updates
   - Interface changes
   - Requirement impacts

3. Design Decisions:
   - Architectural choices
   - Version implications
   - Dependency considerations

4. Project Status:
   - Completed components
   - Pending items
   - Version progression
   - Related artifacts

5. Future Planning:
   - Next development phase
   - Version targets
   - Implementation guidance

Additionally, include a "Suggested Next Session Prompt" that:
- References this session's outcomes
- Provides version progression guidance
- Specifies artifact relationship validation
- Gives clear continuation instructions
```