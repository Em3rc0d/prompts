# Explain Code Clearly

Status: `FREE CANDIDATE / NOT_FOR_SALE`

Use when you have code you want to understand rather than merely rewrite.

## What to provide

- the code or relevant snippet;
- language/framework if known;
- what you already understand, if useful;
- the level of explanation you want.

## Prompt

```text
Help me understand the code I provide.

GOAL
Explain what the code does, how the important parts work together, and what I should notice to understand it correctly.

INPUT
Code:
{{code}}

Known language/framework:
{{runtime_context_or_unknown}}

My current level:
{{beginner_intermediate_advanced_or_unspecified}}

What I especially want to understand:
{{question_or_unspecified}}

RULES
- Base the explanation on the supplied code.
- Do not invent surrounding application behavior that is not visible.
- Separate what is directly visible from reasonable inference.
- Prefer concrete references to functions, variables, branches, data flow, or side effects.
- Define unfamiliar terms when they are necessary.
- If missing context materially changes the explanation, say exactly what is missing.
- Do not rewrite the code unless I ask.

OUTPUT
1. One-paragraph overview.
2. Step-by-step flow.
3. Important concepts or constructs.
4. Inputs, outputs, side effects, and dependencies visible in the snippet.
5. Anything uncertain because context is missing.
6. A short "check your understanding" question.

VERIFICATION
Before finishing, verify that every important claim can be traced to the supplied code or is clearly labeled as inference.
```
