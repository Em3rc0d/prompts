# Style Profile Extractor

**Artifact type:** template  
**Status:** derived-analysis  
**Use when:** multiple writing samples need to be converted into an explicit, reusable style specification without copying their subject matter.

## Variables

- `samples`
- `target_audience`
- `purpose`
- `preserve`
- `avoid`

## Prompt template

```text
ROLE
Act as a writing-style analyst. Your task is to infer recurring stylistic behavior from the supplied samples and convert it into a reusable specification. Analyze how the writing works; do not imitate factual content, personal stories or unique phrases from the samples.

INPUT
Writing samples:
{{samples}}

Target audience: {{target_audience}}
Future writing purpose: {{purpose}}
Traits that must be preserved: {{preserve}}
Traits to avoid: {{avoid}}

INTAKE
If fewer than two meaningful samples are supplied, explain that confidence will be limited and ask for additional material only if the style distinction matters. Otherwise proceed.

RULES
- Separate observed evidence from interpretation.
- Do not infer personal identity, demographics or private traits from writing style.
- Do not reuse memorable phrases, anecdotes or topic-specific facts as style rules.
- Prefer measurable or observable tendencies over vague labels such as “professional” or “engaging.”
- Mark weak conclusions as low-confidence.
- Distinguish deliberate style from artifacts that may come from one sample's topic or format.

ANALYSIS DIMENSIONS
Inspect:
- sentence-length distribution and variation
- paragraph rhythm
- openings and transitions
- directness vs. qualification
- first/second/third-person usage
- vocabulary density and technicality
- use of examples, analogies and questions
- punctuation habits
- structural patterns
- emotional intensity
- calls to action
- recurring tendencies to avoid

OUTPUT
Return:

1. **Style fingerprint**
   5–8 concise traits, each supported by an observed pattern.

2. **Rhythm rules**
   Concrete guidance for sentence and paragraph cadence.

3. **Voice rules**
   What to favor and what to avoid.

4. **Vocabulary profile**
   Preferred vocabulary characteristics, technicality and banned tendencies. Do not list source-specific catchphrases for reuse.

5. **Structure profile**
   Typical openings, development patterns and endings.

6. **Confidence map**
   High / medium / low confidence for each inferred rule, with the reason.

7. **Reusable style preamble**
   A compact instruction block that can be placed before a future writing task.

8. **Self-check rubric**
   Five checks a generated draft should pass before it is considered aligned.
```

## Design notes

The extractor is intentionally a **specification generator**, not a mimicry engine. The reusable output should describe transferable behaviors while excluding source-specific phrases and facts.

## Source family

Derived from theme/structure observations on the public Alpacka generator surface: https://www.alpackaai.xyz/generador

The wording, evidence/confidence model and privacy boundary above are repository-authored.
