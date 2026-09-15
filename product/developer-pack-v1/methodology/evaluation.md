# Evaluation Method

Prompt evaluation should separate static inspection from runtime evidence.

## 1. Static inspection

Before execution, check:
- required inputs are explicit;
- instructions are internally consistent;
- important constraints are testable;
- output requirements are usable;
- uncertainty behavior is defined;
- claims do not exceed evidence.

A passing static inspection can support `VALID`.

## 2. Runtime observation

Execute the prompt against a defined task and record:
- target provider/model or configuration;
- exact prompt/version;
- task input;
- observed output;
- evaluation criteria;
- pass/fail or scored observations;
- unexpected failure modes.

Do not convert an expected behavior into an observation.

## 3. Comparative evaluation

When comparing a revision against a baseline:
- keep the task conditions comparable;
- define the metric or rubric before interpreting results;
- preserve both outputs;
- avoid declaring superiority from one convenient example.

## 4. Repetition and portability

Repeated same-target evidence and cross-provider evidence are separate questions. A prompt that behaves consistently on one model is not automatically portable.

## Practical rule

`Static quality tells you whether the prompt is well specified. Runtime evidence tells you how it actually behaved.`
