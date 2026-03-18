---
name: [Skill Name]
description: [1-2 sentence description of what this skill does and when to use it. Include trigger keywords at the end. Example: "Manages database migrations safely. Use when user wants to update schema, create migration, or rollback changes. Triggers: 'create migration', 'update schema', 'migrate database'"]
version: 0.1.0
author: Dotfiles Skills
---

# [Skill Name] Skill

## Purpose

[2-3 sentences explaining the problem this skill solves and why it's valuable]

## When to Use This Skill

Activate when the user:
- [Trigger scenario 1]
- [Trigger scenario 2]
- [Trigger scenario 3]
- Mentions keywords like: "[keyword1]", "[keyword2]", "[keyword3]"

## Workflow

### Phase 1: [Detection/Analysis]

**[Sub-step Name]**:

```bash
# Example commands
command --flags argument
```

**What to check**:
- [Check item 1]
- [Check item 2]
- [Check item 3]

### Phase 2: [Planning/Preparation]

**[Sub-step Name]**:

[Explanation of what happens in this phase]

**Key Decisions**:
- If [condition] → [action]
- If [condition] → [action]
- Otherwise → [default action]

### Phase 3: [Execution]

**[Sub-step Name]**:

```bash
# Step-by-step commands
step1_command
step2_command
```

**Error Handling**:
- If [error condition]:
  1. [Recovery step 1]
  2. [Recovery step 2]
  3. [Notify user with specific error]

### Phase 4: [Validation]

**[Sub-step Name]**:

Verify the operation succeeded:

```bash
# Validation commands
verify_command
test_command
```

**Success Criteria**:
- ✅ [Criterion 1]
- ✅ [Criterion 2]
- ✅ [Criterion 3]

### Phase 5: [Reporting]

**Success Report**:
```
✨ [Skill Name] Complete

📊 Summary:
✅ [Achievement 1]
✅ [Achievement 2]
✅ [Achievement 3]

🎯 Results:
[Key result 1]: [Value]
[Key result 2]: [Value]

⏱️ Total time: [X] seconds

Next steps:
- [Suggestion 1]
- [Suggestion 2]
```

**Failure Report**:
```
❌ [Skill Name] - Failed

🛑 [Phase] Failed

Error:
  [Specific error message]

💡 Suggested Fix:
[Step-by-step fix instructions]

📋 Logs:
[Relevant log locations]
```

## Examples

### Example 1: [Common Use Case]

**User**: "[User request]"

**Skill Actions**:
```
1. [Step 1]
2. [Step 2]
3. [Step 3]
4. Result: [Outcome]
```

### Example 2: [Edge Case]

**User**: "[User request]"

**Skill Actions**:
```
1. [Step 1]
2. [Detected edge case]
3. [Special handling]
4. Result: [Outcome]
```

### Example 3: [Error Prevented]

**User**: "[User request]"

**Skill Actions**:
```
1. [Step 1]
2. [Validation failed]
3. [Blocked operation]
4. Result: [Error prevented, user guided to fix]
```

## Guidelines

### DO:
✅ [Best practice 1]
✅ [Best practice 2]
✅ [Best practice 3]
✅ Always validate before executing
✅ Provide specific error messages
✅ Show actionable next steps
✅ Include timing information
✅ Test the happy path AND failure modes

### DON'T:
❌ [Anti-pattern 1]
❌ [Anti-pattern 2]
❌ [Anti-pattern 3]
❌ Skip validation steps
❌ Use generic error messages
❌ Leave user in broken state
❌ Execute destructive operations without confirmation
❌ Assume tools are installed without checking

## Advanced Features

### [Feature 1 Name]

[Description of advanced feature]

**Implementation**:
```bash
# Advanced feature code
```

### [Feature 2 Name]

[Description of advanced feature]

**Use Case**: [When this is useful]

## Dependencies

- **[Tool 1]**: [Why it's needed]
- **[Tool 2]**: [Why it's needed]
- **[Tool 3]**: [Optional - what it enables]

## Configuration

[Any configuration options or environment variables]

```bash
# Example configuration
SETTING_NAME=value
```

## Troubleshooting

### Common Issues

**Issue**: [Problem description]
**Solution**:
```
1. [Fix step 1]
2. [Fix step 2]
3. [Verification step]
```

**Issue**: [Another problem]
**Solution**:
[Fix description]

## Success Metrics

A successful [skill name] execution includes:
- ✅ [Success criterion 1]
- ✅ [Success criterion 2]
- ✅ [Success criterion 3]
- ✅ [Success criterion 4]
- ✅ Completion time under [X] seconds

## Integration

Works seamlessly with:
- **[Other Skill 1]**: [How they work together]
- **[Other Skill 2]**: [How they work together]

## Version History

- v0.1.0 (YYYY-MM-DD): Initial template
  - [Feature or improvement]
  - [Feature or improvement]

---

## Template Instructions

When creating a new skill from this template:

1. **Replace all [bracketed] placeholders** with actual content
2. **Define clear trigger keywords** in the description YAML frontmatter
3. **Break workflow into 3-5 logical phases** (Detection, Planning, Execution, Validation, Reporting)
4. **Provide 3 examples** showing success, edge case, and error prevention
5. **Include DO/DON'T guidelines** for clarity
6. **List all dependencies** and how to check for them
7. **Add troubleshooting** for at least 3 common issues
8. **Define success metrics** so effectiveness can be measured

### Quality Checklist

Before considering a skill complete:

- [ ] YAML frontmatter complete and accurate
- [ ] Trigger keywords clearly defined
- [ ] All workflow phases documented
- [ ] Error handling specified
- [ ] At least 3 examples provided
- [ ] DO/DON'T guidelines included
- [ ] Dependencies listed
- [ ] Troubleshooting section present
- [ ] Success metrics defined
- [ ] Tested on real use case
