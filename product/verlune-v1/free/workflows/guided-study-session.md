# Guided Study Session

Status: `FREE WORKFLOW CANDIDATE / NOT_FOR_SALE`

Use when you want a study session that adapts to what you actually understand instead of producing another passive summary.

## Inputs

Required:

- topic;
- learning goal.

Useful:

- current level;
- source material / notes;
- deadline or exam context;
- available study time.

## Workflow

### 1. Diagnose starting point

Ask 2–4 short questions or use the supplied background to estimate prerequisite knowledge.

Do not treat confidence as mastery.

### 2. Build the smallest learning sequence

Split the topic into the fewest prerequisite steps needed to reach the stated goal.

### 3. Teach one unit

For the current unit:

- give a concise explanation;
- provide one concrete example;
- distinguish the core rule from exceptions;
- connect it to what came before.

### 4. Retrieval check

Ask the learner to explain, solve, compare, or apply the idea without showing the answer first.

### 5. Evaluate the response

Classify the result:

- `UNDERSTOOD`
- `PARTIAL`
- `MISCONCEPTION`
- `NOT_YET`

Explain the specific gap. Do not simply say "correct" or "incorrect."

### 6. Adapt

- `UNDERSTOOD` → move forward;
- `PARTIAL` → repair the smallest missing piece;
- `MISCONCEPTION` → contrast the mistaken model with the correct one;
- `NOT_YET` → step back to a prerequisite.

### 7. End the session

Finish with:

- what was mastered;
- what remains weak;
- 3 retrieval questions for later;
- the next recommended study unit.

## Output contract

For each session return:

1. current learning target;
2. short explanation/example for the active unit;
3. retrieval/application question;
4. evaluation state after the learner answers;
5. specific gap or misconception;
6. next action;
7. end-of-session mastery summary.

## Fallback

If the topic, goal, or source material is too incomplete to teach responsibly:

- do not pretend the learner completed the topic;
- identify the smallest missing prerequisite or source;
- return `NOT_YET`;
- propose the next bounded learning step.

## Verification

Before advancing:
- require evidence of recall/application rather than confidence alone;
- keep source-dependent claims inside the supplied material unless external research is explicitly available;
- ensure feedback explains the specific reasoning gap;
- do not mark mastery after explanation alone.

## Boundaries

- Do not invent facts from source material that was not provided.
- If current/external facts matter and no research tools are available, state the limitation.
- Do not complete graded work deceptively on behalf of the learner; teach the reasoning needed to do it.
