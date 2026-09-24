# Verlune v1 — Portability Operator Instructions

Status: `READY FOR EXTERNAL EXECUTION`

Date: 2026-09-23

## Goal

Run the same frozen 12-case portability batch once on ChatGPT and once on Gemini, without modifying the batch between hosts.

Batch:
`product/verlune-v1/evaluation/PORTABILITY_12_CASE_SINGLE_CHAT_BATCH_2026-09-23.txt`

Review contract:
`product/verlune-v1/evaluation/PORTABILITY_12_CASE_REVIEW_CONTRACT_2026-09-23.json`

## Run A — ChatGPT

1. Open a brand-new Temporary Chat / clean conversation with personalization disabled when the product allows it.
2. Before pasting the batch, record outside the model response:
   - host: ChatGPT
   - exact model label visible in the UI
   - thinking/mode label if visible
   - temporary/clean chat: yes/no
   - local date/time
3. Paste the complete frozen batch as one message.
4. Do not add coaching or follow-up instructions.
5. If output truncates because of response length, send only:
   `Continue from the next unfinished CASE. Preserve the exact response delimiters and do not revise completed cases.`
6. Save the full transcript.

## Run B — Gemini

Repeat the same procedure in a brand-new Gemini conversation.

Record:
- host: Gemini
- exact model label visible in the UI
- mode/config if visible
- clean/new conversation: yes/no
- local date/time

Paste the exact same frozen batch. Do not adapt wording for Gemini.

If output truncates, use the same continuation sentence and preserve completed cases.

## Return evidence

Bring back:
- ChatGPT model/config metadata + transcript;
- Gemini model/config metadata + transcript.

The two transcripts may be uploaded together.

## Evidence boundary

A qualifying result permits only a bounded statement such as:

> Tested on the exact recorded ChatGPT model/config and the exact recorded Gemini model/config using the frozen representative portability sample.

It does not support:
- “works with every ChatGPT model”;
- “works with every Gemini model”;
- “works with all leading AI assistants”;
- universal portability;
- certification of customer-generated artifacts.

No host/model is promoted to tested status until its transcript is reviewed against the pre-frozen contract.
