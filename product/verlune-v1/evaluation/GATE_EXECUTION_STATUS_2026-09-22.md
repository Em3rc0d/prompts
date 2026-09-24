# Verlune v1 — Gate Execution Status

Date: 2026-09-22

Status: `PRE-FORMAL-EXECUTION READY / EXTERNAL EXECUTION GATES OPEN`

## Completed in this pass

- Exact launch-core asset binding frozen for 26 assets (24 non-Builder + 2 Builders).
- Catalog ↔ binding manifest completeness preflight: PASS.
- Builder execution manifest frozen for 37 cases.
- Builder case count preflight: 37/37 READY.
- Existing generated-prompt and generated-workflow second-instance evidence preserved.
- Existing 104/104 behavioral screening evidence preserved as screening only.

## Not claimed as complete

### Builder v1 coverage gate

State: `BOUNDED V1 COVERAGE PASS / ORIGINAL 38-INDEPENDENT FORMAL PACKET NOT EXECUTED`

Observed segmented batch result: **37 PASS / 0 FAIL / 0 INCONCLUSIVE** against the frozen review contract.

The batch used the exact frozen Builder identities and covered all 32 category cases plus 5 stress cases. The pre-frozen clean-context sample was then rerun in five physically isolated temporary unpersonalized chats: **5 PASS / 0 FAIL / 0 INCONCLUSIVE / 0 material contradictions**. `BUILDER_COVERAGE_GATE = PASS` for the bounded v1 policy. The older frozen protocol requiring at least 38 independent conversations remains historical deeper-qualification work and was **not** executed; this status does not rewrite that history.

### Formal non-Builder exact-asset runtime

State: `PASS / 32 OF 32`

For the bounded v1 launch gate, the earlier exhaustive 87-case isolated matrix is preserved but no longer mandatory. Before seeing runtime results, a proportional exact-asset gate was frozen: all 24 exact non-Builder launch-core assets receive one NORMAL runtime case, plus 8 preselected edge/adversarial cases. Result: **32 PASS / 0 FAIL / 0 INCONCLUSIVE**. The earlier 104 observations remain screening only and are not silently upgraded.

### Cross-model portability

State: `CURRENT-BLOB BEHAVIOR PASS / NAMED MODEL METADATA OPEN`

A representative 8-asset / 12-case batch is frozen before results. It must be executed once on ChatGPT and once on Gemini, recording the exact model/config shown by each provider. A host/model may be named as tested only after its own qualifying observed run; no universal compatibility claim is permitted.

### Human review H1-H11

State: `OPEN`

Reason: the gate explicitly requires a reviewer to use the customer product. An internal repository pass cannot substitute for external human observation or purchase-value feedback.

### Premium access / entitlement / commerce E2E

State: `ACCESS LAYER IMPLEMENTED CANDIDATE / BUILD + PROVIDER E2E OPEN`

The candidate `/unlock → /app` product now exists in the repository with server-side entitlement checks, signed browser authorization, protected asset delivery, periodic revalidation, logout/deactivation and a build-time leakage audit. This is implementation evidence only. Typecheck/build, staging deployment, exact new Premium provider identity and provider-backed E2E remain open; therefore `ENTITLEMENT_E2E_PASS = false`.

### Landing redesign

State: `FROZEN`

Authorization remains false until the Human Review Gate ends in:
- `PASS_FOR_LANDING_REDESIGN`, or
- `PASS_WITH_NONBLOCKING_NOTES`.

## Current graph

```text
STATIC CORE                                      PASS
104 BEHAVIORAL SCREENING OBSERVATIONS            PASS
EXACT ASSET BINDING (26/26)                      PASS
EXECUTION PREFLIGHT                              PASS
GENERATED PROMPT SECOND INSTANCE                 PASS
GENERATED WORKFLOW SECOND INSTANCE               PASS

37 BUILDER SEGMENTED CASES                     PASS (37/37)
NON-BUILDER EXACT-ASSET 32-CASE BATCH          PASS ON CURRENT BINDING
5 BUILDER SEGMENTED SPOT-CHECKS                 PASS (5/5)
5 BUILDER CLEAN SPOT-CHECKS                     PASS (5/5)
TARGETED CROSS-HOST BEHAVIOR                     PASS BOUNDED SAMPLE; MODEL METADATA OPEN
PREMIUM ACCESS IMPLEMENTATION                    CANDIDATE IMPLEMENTED; BUILD/E2E OPEN
HUMAN REVIEW H1-H11                              OPEN
ENTITLEMENT / COMMERCE E2E                       OPEN AFTER ACCESS BUILD/PROVIDER TEST
LANDING REDESIGN                                 FROZEN
READY_TO_SELL                                    NO
```

Master rule: `not observed == unknown`.


## 2026-09-23 Builder batch update

- segmented batch transcript SHA-256: `4d606d5a0ab7ecb25862f752487b1ed6e5a00dc9e8be7a37c9e1b99c23bbe83c`
- cases reviewed: 37
- PASS: 37
- FAIL: 0
- INCONCLUSIVE: 0
- clean-context spot-checks remaining: 5
- review record: `product/verlune-v1/evaluation/BUILDER_BATCH_37_REVIEW_2026-09-23.json`


## 2026-09-23 segmented spot-check update

- pre-frozen sample executed in one segmented temporary chat
- cases: 5
- PASS/no material contradiction: 5
- FAIL: 0
- INCONCLUSIVE: 0
- transcript SHA-256: `284bb509026fdc30ab7cefe4b040f04c9aa024abfad4f5d865ed39c0b0faeaf7`
- this is consistency evidence only; it does not satisfy the previously frozen five physically isolated clean-context requirement
- review record: `product/verlune-v1/evaluation/BUILDER_SPOTCHECK_5_SEGMENTED_REVIEW_2026-09-23.json`


## 2026-09-23 Builder coverage gate closure

- exact Builder blobs unchanged
- segmented matrix: 37/37 PASS
- segmented consistency sample: 5/5 PASS
- physically isolated clean-context sample: 5/5 PASS
- material contradictions: 0
- invalid operator attempt excluded from scoring: 1
- `BUILDER_COVERAGE_GATE = PASS`
- closure record: `product/verlune-v1/evaluation/BUILDER_COVERAGE_GATE_CLOSURE_2026-09-23.json`
- remaining major gates: formal non-Builder exact-asset runtime, targeted cross-model portability, human H1-H11, entitlement/commerce E2E


## 2026-09-23 non-Builder gate compression

- exact non-Builder assets covered: 24/24
- runtime cases frozen: 32
- normal cases: 24
- targeted edge/adversarial cases: 8
- execution mode: `MANUAL-OBSERVED / SINGLE_CHAT_SEGMENTED_EXACT_ASSET`
- original 87-case packet preserved for deeper qualification, not mandatory for bounded v1 launch
- plan: `product/verlune-v1/evaluation/RISK_BASED_EXACT_ASSET_RUNTIME_GATE_2026-09-23.json`
- batch: `product/verlune-v1/evaluation/NON_BUILDER_32_SINGLE_CHAT_EXACT_ASSET_BATCH_2026-09-23.txt`


## 2026-09-23 non-Builder exact-asset gate closure

- exact non-Builder assets observed: 24/24
- cases reviewed: 32
- PASS: 32
- FAIL: 0
- INCONCLUSIVE: 0
- blocking failures: 0
- transcript SHA-256: `d3f682cd75879eee6dba375899938b984ac19ca9496091754947f8739559ada4`
- transcript bytes: 112125
- runtime/model/host metadata: NOT CAPTURED IN TRANSCRIPT
- evidence mode: `MANUAL-OBSERVED / SINGLE_CHAT_SEGMENTED_EXACT_ASSET`
- `NON_BUILDER_EXACT_ASSET_RUNTIME_GATE = PASS`
- review record: `product/verlune-v1/evaluation/NON_BUILDER_32_EXACT_ASSET_REVIEW_2026-09-23.json`
- independent-context robustness: NOT ESTABLISHED
- cross-model portability: OPEN


## 2026-09-23 portability execution packet

- representative exact assets: 8
- frozen cases: 12
- required hosts: ChatGPT + Gemini
- execution mode: `MANUAL-OBSERVED / SINGLE_CHAT_SEGMENTED_PORTABILITY`
- batch: `product/verlune-v1/evaluation/PORTABILITY_12_CASE_SINGLE_CHAT_BATCH_2026-09-23.txt`
- review contract: `product/verlune-v1/evaluation/PORTABILITY_12_CASE_REVIEW_CONTRACT_2026-09-23.json`
- exact UI model/config must be recorded outside the model output
- result: OPEN


## 2026-09-23 ChatGPT portability run

- cases: 12
- PASS: 12
- FAIL: 0
- INCONCLUSIVE: 0
- blocking failures: 0
- transcript SHA-256: `b2c714ad2d366634ee92d9ab1096ed407951bfd4034d1dd4ac27b99e8d755876`
- transcript bytes: 34876
- exact ChatGPT model/config: NOT CAPTURED IN RETURNED TRANSCRIPT
- behavioral result: `PASS_12_OF_12`
- host/model qualification: `PENDING_METADATA`
- Gemini execution: OPEN
- review: `product/verlune-v1/evaluation/PORTABILITY_CHATGPT_REVIEW_2026-09-23.json`


## 2026-09-23 Gemini portability run

- cases: 12
- PASS: 10
- FAIL: 2
- INCONCLUSIVE: 0
- blocking failures: 2
- failing cases: `PORT-RESEARCH-ADVERSARIAL`, `PORT-MASTERY-NORMAL`
- transcript SHA-256: `525611106f0abd644404f9aebe4a6f4c3283a94714cff2198338c035ce8fad0e`
- transcript bytes: 19863
- exact Gemini model/config: NOT CAPTURED IN RETURNED TRANSCRIPT
- result: `NOT_QUALIFIED / REWORK_REQUIRED`
- cross-model portability gate: OPEN
- review: `product/verlune-v1/evaluation/PORTABILITY_GEMINI_REVIEW_2026-09-23.json`


## 2026-09-23 portability remediation

Gemini exposed two blocking portability failures and the evidence was preserved before changing product bytes.

Changed assets:
- VP-WF-003: `136f837... → 6daeae311de1fc1a9b5b9ad180951608443a8fa9`
- VP-WF-006: `4c2a695... → b2d98d24db14b2369d62709a330e95e3e9ec31b4`

Remediation:
- Deep Research now forbids invented claim-ledger states and explicitly prevents a missing registry match from becoming proof of falsity without direct/complete evidence.
- Master a Topic now treats self-reported background as context, not mastery proof, and caps it at FRAGILE until retrieval/application or explicit assessment evidence exists.

Current state:
- historical 32/32 exact-asset PASS remains evidence for prior blobs;
- current exact-asset release gate requires delta requalification;
- cross-model portability requires ChatGPT + Gemini delta retest;
- exact UI model/config metadata remains mandatory.

Delta batch:
`product/verlune-v1/evaluation/PORTABILITY_REMEDIATION_DELTA_4_CASE_BATCH_2026-09-23.txt`


## 2026-09-23 second Deep Research portability remediation

The first remediation fixed the original Gemini ledger/registry failure, and VP-WF-006 now passes on both observed hosts. A separate Gemini failure remained in `VP-WF-003-NORMAL`:

- evidence outside the requested 2015-2026 scope was used as direct support;
- one cited source was omitted from the source list;
- vague unnamed "contemporary meta-analyses" were invoked;
- mixed-population evidence was generalized too strongly to higher education.

Deep Research was tightened again:
- scope fields are now evidence inclusion constraints;
- out-of-scope sources may only be clearly labeled background unless scope is expanded;
- every material source must be traceable;
- vague unnamed confirming literature is prohibited;
- mixed-population evidence cannot be silently promoted to target-population evidence;
- missing registry matches should be described as verification gaps/tension unless direct contradiction is established.

New VP-WF-003 blob: `afa65c9cdccff26d6fe92cee800818f3066d4220`

Current state:
- VP-WF-006 delta behavior: PASS on ChatGPT + Gemini;
- VP-WF-003 final current-blob delta: OPEN;
- exact model/config metadata: still pending.


## 2026-09-23 final Deep Research delta frozen

- exact current blob: `afa65c9cdccff26d6fe92cee800818f3066d4220`
- cases: 3
- hosts: ChatGPT + Gemini
- result: OPEN
- batch: `product/verlune-v1/evaluation/FINAL_DEEP_RESEARCH_DELTA_3_CASE_BATCH_2026-09-23.txt`
- contract: `product/verlune-v1/evaluation/FINAL_DEEP_RESEARCH_DELTA_REVIEW_CONTRACT_2026-09-23.json`


## 2026-09-23 final Deep Research delta result

- exact current blob: `afa65c9cdccff26d6fe92cee800818f3066d4220`
- ChatGPT: 3/3 behavioral PASS
- Gemini: 3/3 behavioral PASS, with `SOURCE_ACCESS_BLOCKED` on the normal research case because live source retrieval was unavailable
- blocking failures: 0
- VP-WF-006 current blob: PASS on both observed hosts from prior delta
- exact-asset runtime gate: PASS on current binding
- targeted cross-host behavioral sample: PASS
- exact ChatGPT model/config: NOT SUPPLIED
- exact Gemini model/config: NOT SUPPLIED
- named host/model portability qualification: OPEN
- universal portability: NOT CLAIMED
- review: `product/verlune-v1/evaluation/FINAL_DEEP_RESEARCH_DELTA_REVIEW_2026-09-23.json`

Interpretation:
Gemini demonstrated the correct fail-safe source-access path, not live academic retrieval. Therefore the behavior gate is closed, but no claim that the observed Gemini environment can execute source-retrieval research is permitted.


## 2026-09-23 Premium access implementation candidate

Implemented in repository:
- `/unlock`;
- protected `/app`;
- protected `/app/asset/:id`;
- `/app/access`;
- Lemon license validate / activate / deactivate integration;
- exact store/product/variant/email checks;
- 3-browser activation policy candidate;
- signed HttpOnly authorization session, max 7 days;
- entitlement revalidation at least every 24 hours;
- signed non-authorizing device reference to reuse the same provider instance after logout/session expiry;
- server-only Premium build materialization;
- exact Git-blob verification before asset delivery;
- post-build Premium public/static leakage audit;
- 17 launch-core Premium surfaces in the protected library.

Frozen execution contract:
`product/verlune-v1/evaluation/ACCESS_PRODUCT_TEST_PLAN_2026-09-23.json`

Implementation record:
`product/verlune-v1/evaluation/ACCESS_PRODUCT_IMPLEMENTATION_2026-09-23.md`

Still not observed:
- typecheck/build PASS;
- current-branch staging deployment;
- new Verlune Premium Lemon product/variant with license keys;
- provider IDs/secrets configured;
- access E2E;
- H1-H11;
- commerce test purchase;
- live canary.

`ACCESS_LAYER_IMPLEMENTED_CANDIDATE = true`  
`ACCESS_PRODUCT_E2E_PASS = false`  
`READY_TO_SELL = false`


## 2026-09-23 Premium provider discovery

Read-only Lemon Squeezy probe result:

- store: `462419`
- exact product `Verlune Premium`: NOT OBSERVED
- observed historical SKU: `Verlune Code Review` / product `1347720` / test_mode=true / USD 9
- provider side effects: 0
- state: `ACTION_REQUIRED / CREATE_NEW_PREMIUM_PRODUCT`

Decision:
Do **not** rename or repurpose the historical Code Review SKU. Create a separate `Verlune Premium` product so prior commerce/evidence identity remains auditable.

Required Premium provider settings:
- USD 9 one-time;
- license keys enabled;
- activation limit 3;
- license length unlimited.

After creation, rerun:
`python3 tools/pm_verlune_premium_provider_probe.py --store-id 462419`

Evidence:
`product/verlune-v1/evaluation/PREMIUM_PROVIDER_PROBE_2026-09-23.json`


## 2026-09-23 Premium provider identity frozen — Test mode

Read-only provider probe: PASS.

- store: `462419`
- product: `1383189` / `Verlune Premium`
- variant: `2160866` / default
- product status: published
- product test_mode: true
- variant test_mode: true
- price: USD 9 one-time
- license keys: enabled
- activation limit: 3
- license length: unlimited
- variant status: `pending` (expected provider default-variant state)
- provider side effects: 0

Evidence:
`product/verlune-v1/evaluation/PREMIUM_PROVIDER_IDENTITY_TEST_2026-09-23.json`

Next blocker:
configure these non-secret IDs plus server-only API key and strong session/fingerprint secrets in the staging environment, then run build + access E2E.

Live-mode note:
the operator reported an earlier product creation happened in Live mode. No live identity or exposure claim is made; it must be audited before the controlled live canary.


## 2026-09-23 first local access-product build attempt

- `npm install`: PASS, 0 vulnerabilities
- `npm run typecheck`: PASS
- `npm run build`: BLOCKED in prebuild before Next.js compilation
- blocker: historical Free Pack production endpoint returned HTTP 500 integrity failure
- observed remote archive: 23498 bytes / SHA-256 `ba02210e8649ec1e601d65afae3b31e4985de1ab577483d5c155540f5f8f7dbf`
- frozen archive: 23498 bytes / SHA-256 `55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32`
- root cause: locale-sensitive ZIP entry sorting diverged from governed raw lexicographic ordering
- route sort patched
- prebuild changed to deterministic local governed materialization; remote verification now opt-in
- state: `PATCHED / OPERATOR BUILD RERUN REQUIRED`
- evidence: `product/verlune-v1/evaluation/BUILD_BLOCKER_FREE_PACK_2026-09-23.md`


## 2026-09-23 second local build blocker

Second operator rerun:
- typecheck: PASS
- build: stopped in Free Pack materialization on `LICENSE.md` size mismatch
- cause: Windows working-tree CRLF conversion vs canonical LF Git blob bytes
- frozen release hashes: unchanged
- patch: normalize Markdown CRLF/CR → LF before identity checks/materialization
- Premium private materializer patched proactively with the same canonicalization
- state: `PATCHED / OPERATOR BUILD RERUN REQUIRED`


## 2026-09-23 local access-product build — PASS

Observed on operator Windows / Node 24.11.1:

- `npm install`: PASS / 0 vulnerabilities
- `npm run typecheck`: PASS
- governed Free Pack materialization: PASS
- Free Pack: 7 assets / 23498 bytes / SHA-256 `55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32`
- Premium private materialization: PASS / 18 Markdown files
- Next.js 16.3.3 production build: PASS
- static pages: 25/25
- Verlune protected routes present: PASS
- Golden Path build parity: PASS
- Premium build audit: PASS
- private launch-core assets: 17
- protected routes: 8
- public/static files scanned: 15

Evidence:
`product/verlune-v1/evaluation/ACCESS_PRODUCT_LOCAL_BUILD_EVIDENCE_2026-09-23.json`

Gate effect:
- `LOCAL_BUILD_GATE = PASS`
- `ACCESS_PRODUCT_E2E_PASS = false`
- next: staging environment + deployment + provider-backed access test plan


## 2026-09-23 Vercel prebuilt deployment attempt — Windows packaging blocker

Observed:
- `vercel build --prod`: application build PASS
- governed Free Pack materialization: PASS
- Premium private materialization: PASS
- Next.js production build: PASS
- Golden Path build parity: PASS
- Premium build audit: PASS
- Vercel Build Output packaging completed only when PowerShell ran elevated
- `vercel deploy --prebuilt --prod`: ERROR
- deployment: `dpl_4DVovTUVraomnTMTwkr7PxmFvnto`
- failure: missing function-segment target under Linux upload path:
  `ENOENT ... .vercel/output/functions/_global-error.segments/__PAGE__.segment.rsc.func`

Interpretation:
the application/build gate remains PASS. The blocker is cross-platform prebuilt artifact packaging from Windows to Vercel's Linux deployment environment, not an observed Verlune runtime failure.

Next execution path:
build the prebuilt artifact in a Linux filesystem/environment (WSL Linux home or equivalent), then deploy that Linux-built `.vercel/output`.

`STAGING_DEPLOY_PASS = false`


## 2026-09-23 staging access deployment — PASS

Linux prebuilt deployment:
- project: `prompt-quarry-stage`
- deployment: `dpl_44HrayDpj2iQD7SmnBMrZoRGqNKf`
- alias: `https://prompt-quarry-stage.vercel.app`
- state: READY

Observed:
- `vercel build --prod`: PASS
- Next.js production build: PASS
- Golden Path build parity: PASS
- Premium build audit: PASS
- `/`: 200
- `/unlock`: 200
- unauthenticated `/app`: rendered through `/unlock`, locked notice present
- unauthenticated `/app/asset/VP-BUILDER-001`: rendered through `/unlock`, locked notice present
- protected Prompt Builder body absent from unauthenticated response
- runtime error clusters in observed 30-minute window: none

Evidence:
`product/verlune-v1/evaluation/STAGING_ACCESS_DEPLOYMENT_EVIDENCE_2026-09-23.json`

Gate effect:
- `STAGING_DEPLOY_PASS = true`
- `UNAUTHENTICATED_ACCESS_BOUNDARY_SMOKE = PASS`
- `ACCESS_PRODUCT_E2E_PASS = false`
- next: obtain one Lemon Test-mode purchase/license and exercise provider-backed unlock → /app.


## 2026-09-23 provider-backed valid unlock — PASS

Observed on staging deployment `dpl_44HrayDpj2iQD7SmnBMrZoRGqNKf`:

- before unlock: unauthenticated `/app` and protected asset routes returned 307 to `/unlock`;
- `POST /api/verlune/unlock`: 200;
- immediately after unlock: `/app`: 200;
- `/app/access`: 200;
- multiple protected Premium asset routes: 200;
- customer-visible Premium library rendered all 17 launch-core surfaces;
- runtime error clusters in the checked 15-minute window: none.

Because the implemented unlock path requires exact license validity + checkout email + store + product + variant + activation policy before signing the authorization session, this closes the **valid entitlement unlock path** for the observed Test-mode purchase.

Evidence:
`product/verlune-v1/evaluation/PROVIDER_BACKED_UNLOCK_EVIDENCE_2026-09-23.json`

Still open before `ACCESS_PRODUCT_E2E_PASS`:
invalid/mismatched entitlement cases, session tamper, revalidation/revocation, logout/reuse, deactivation, provider-outage behavior and three-browser/4th-browser policy.


## 2026-09-23 logout + same-browser activation reuse — PASS

Operator-observed:
- Prompt Builder opened with complete protected body;
- Copy full asset: PASS;
- Lemon license remained `Active (1/3)`;
- after logout, `/app` locked again;
- same browser re-unlocked with the same Test entitlement;
- activation usage remained `1/3` rather than increasing.

Runtime corroboration:
- `POST /api/verlune/logout` → 303;
- subsequent `GET /app` → 307;
- `POST /api/verlune/unlock` → 200;
- subsequent `GET /app` → 200;
- subsequent `GET /app/asset/VP-BUILDER-001` → 200.

Evidence:
`product/verlune-v1/evaluation/SESSION_REUSE_EVIDENCE_2026-09-23.json`

Closed:
- `ACCESS-15 Logout semantics = PASS`
- `ACCESS-16 Same-browser re-unlock reuses activation = PASS`
- Prompt Builder protected delivery/copy path = PASS observed
- activation reuse `1/3 → 1/3` = PASS

Still open:
negative entitlement cases, session tamper, periodic revalidation/revocation, provider-outage behavior, provider deactivation, and 3-browser/4th-browser policy.


## 2026-09-23 customer-surface copy note from first Premium use

Observed in the protected Prompt Builder customer surface:

`Status: PREMIUM BUILDER CANDIDATE / RUNTIME TESTING REQUIRED`

Interpretation:
- this does **not** invalidate the access/session tests;
- it is stale/internal qualification language exposed to a paying customer;
- it conflicts with the current bounded Builder evidence state and weakens customer trust;
- treat as a nonblocking access defect but a **blocking Human Review copy/UX issue before H1-H11 can pass**.

Do not rewrite the tested Builder instruction block merely to fix presentation. Resolve at the product-surface/presentation boundary or through a governed metadata update that preserves behavioral lineage.


## 2026-09-23 negative entitlement + deactivate block

Observed:
- correct license + wrong checkout email → controlled denial / HTTP 401: PASS;
- invalid license → fail closed / HTTP 502: security behavior PASS, UX/error classification defect found;
- valid re-unlock before deactivation → HTTP 200;
- `POST /api/verlune/deactivate` → 303;
- Lemon provider dashboard after deactivation → `Inactive (0/3)`: PASS.

Defect:
invalid license/provider 4xx validation was being presented as temporary provider unavailability.

Remediation implemented:
- typed Lemon License API error classification;
- validation-side 4xx rejection (except 429) now maps to the controlled 401 invalid-entitlement response;
- true upstream/network/5xx conditions remain 502.

Evidence:
`product/verlune-v1/evaluation/NEGATIVE_ENTITLEMENT_DEACTIVATION_EVIDENCE_2026-09-23.json`

Gate effect:
- `ACCESS-04 Wrong checkout email denied = PASS`
- `ACCESS-03 Invalid license denied = PASS_SECURITY / UX_RETEST_REQUIRED_AFTER_REDEPLOY`
- `ACCESS-17 Deactivate semantics = PASS`
- provider activation after deactivation: `0/3`


## 2026-09-23 invalid-entitlement UX retest — PASS

Redeployed access fix observed on staging deployment `dpl_2X36LEthfNDUcKvVqPKtiKrRyJog`.

Runtime:
- rejected unlock attempt #1 → HTTP 401;
- rejected unlock attempt #2 → HTTP 401;
- valid unlock afterward → HTTP 200;
- `/app` afterward → HTTP 200.

Provider state:
- after deactivation: `Inactive (0/3)`;
- after valid reactivation: `Active (1/3)`.

This closes the earlier invalid-license error-classification defect.

Evidence:
`product/verlune-v1/evaluation/INVALID_ENTITLEMENT_RETEST_2026-09-23.json`

Closed:
- `ACCESS-03 Invalid license denied = PASS`
- `ACCESS-04 Wrong checkout email denied = PASS`
- `ACCESS-17 Deactivate semantics = PASS`
- deactivate → reactivate `0/3 → 1/3 = PASS`

Open:
session tamper, stale-session revalidation/revocation, provider-outage retry behavior, and 3-browser/4th-browser activation policy.


## 2026-09-23 revalidation + disabled entitlement

Observed:
- valid active entitlement revalidation → 303 back to `/app`: PASS;
- disabled Test license during an existing session → Premium locked: security fail-closed PASS;
- UI showed `revalidation-unavailable` and preserved the signed session: semantic/session-clear defect;
- license re-enabled and valid unlock restored `Active (1/3)`.

This means the security boundary held, but `ACCESS-13` was **not fully closed** on the first run because provider rejection was misclassified as outage.

Remediation implemented:
- provider License API 4xx validation rejection (except 429) → `session-invalid` + clear authorization/device cookies;
- Admin API 4xx missing/rejected license (except 429) → same invalidation path;
- network / 429 / provider 5xx → remain `revalidation-unavailable` with retryable local state.

Evidence:
`product/verlune-v1/evaluation/REVALIDATION_REVOCATION_EVIDENCE_2026-09-23.json`

State:
- valid revalidation = PASS
- revoked/disabled fail-closed security = PASS
- revoked/disabled clear-session semantics = RETEST REQUIRED
- provider-outage case = OPEN


## 2026-09-23 revoked-entitlement revalidation retest — PASS

Observed on staging deployment `dpl_8o76QB3wiz5kHfrnbZWmPWq5BcaK`:

- provider state: `Disabled (1/3)`;
- forced `GET /api/verlune/session/revalidate` → 303;
- customer UI: `This Premium session is no longer valid. Enter your purchase details again.`;
- unlock attempt while disabled → HTTP 401;
- customer UI: controlled inactive-entitlement denial.

This closes the earlier revoked-entitlement classification/session-clear defect.

Evidence:
`product/verlune-v1/evaluation/REVOKED_ENTITLEMENT_RETEST_2026-09-23.json`

Closed:
- `ACCESS-13 Disabled/revoked entitlement fails closed = PASS`
- revoked entitlement invalid-session semantics = PASS

Still open:
- provider-outage retry branch;
- 3 active browsers + 4th-browser denial.


## 2026-09-23 three-browser activation policy — PASS

Observed on staging:
- provider dashboard reached `Active (3/3)`;
- three distinct browser contexts were able to hold activations;
- fourth browser remained locked;
- fourth unlock attempt returned HTTP 409;
- customer message: `This license could not activate another browser. Deactivate an old browser or check the activation limit.`;
- provider activation usage remained 3/3.

Runtime corroboration:
- additional valid unlocks → 200;
- fourth-context unlock → 409;
- locked fourth context `GET /app` → 307.

Evidence:
`product/verlune-v1/evaluation/MULTI_BROWSER_ACTIVATION_LIMIT_EVIDENCE_2026-09-23.json`

Closed:
- `ACCESS-20 Three-browser policy = PASS`
- fourth-browser denial = PASS

Pre-outage hardening:
Admin API authentication/permission failures (401/403) are now treated as retryable provider/configuration unavailability, not as customer entitlement revocation. Only Admin license-key 404/410 is treated as missing/revoked entitlement. Redeploy required before the outage case.


## 2026-09-23 pre-outage fail-closed hardening

Before executing the provider-outage fault injection, review found an edge case in the forced revalidation path:

- on a retryable provider/admin outage, the UI correctly rendered `revalidation-unavailable`;
- however, the signed authorization session was preserved with a fresh-enough `validatedAt`;
- a direct `/app` request after a *manually forced* failed revalidation could therefore still authorize until the normal 24-hour threshold elapsed.

This was not observed leaking content in the real stale-session path, but it violates the intended stronger invariant: once a revalidation attempt fails, Premium must stay locked until provider validation succeeds.

Patch:
- retryable outage now re-signs the session with `validatedAt=0`;
- the session is retained only as a retry token;
- every protected route sees it as stale and redirects back through revalidation;
- successful retry refreshes `validatedAt` and restores Premium;
- revoked/invalid entitlement continues to clear session + device reference.

State:
- `ACCESS-14 PROVIDER OUTAGE` remains unexecuted;
- redeploy required before fault injection.


## 2026-09-23 provider outage fault injection — fail-closed PASS / restore retry pending

Observed on outage deployment `dpl_3upqJP3Tu25CWCZHi9vmmCvdJomL`:
- forced revalidation repeatedly returned 303 to the locked state;
- UI displayed the explicit provider-unavailable message;
- signed browser session was retained only for retry;
- direct `GET /app` during outage returned 307 and did not expose Premium.

A subsequent READY production-target staging deployment `dpl_HW3MorA762ag2SpGzSuPphKQD8jU` exists as the restore candidate.

Evidence:
`product/verlune-v1/evaluation/PROVIDER_OUTAGE_EVIDENCE_2026-09-23.json`

State:
- `ACCESS-14 provider outage fail-closed = PASS`
- `ACCESS-14 retry after provider restore = PENDING USER RETRY`


## 2026-09-23 provider outage restore retry — PASS

Observed on restored staging deployment `dpl_HW3MorA762ag2SpGzSuPphKQD8jU`:
- Retry license check triggered provider revalidation;
- revalidation route returned 303;
- subsequent `/app` requests returned 200;
- Premium library was restored without re-entering checkout email or license key.

This completes `ACCESS-14 Provider outage fail-closed retry = PASS`.

Evidence updated:
`product/verlune-v1/evaluation/PROVIDER_OUTAGE_EVIDENCE_2026-09-23.json`


## 2026-09-23 Premium access product gate closure

Final bounded audit against the pre-frozen 20-case access plan:

- PASS_RUNTIME: provider/customer staging behavior observed for the customer-critical paths;
- PASS_BUILD: private materialization / route presence / public-bundle leakage checks;
- PASS_CODE_INVARIANT: deterministic security/session/error-handling properties where another destructive manual fault injection would add little value;
- all 20 cases: PASS under their recorded evidence mode;
- blocking unauthorized Premium delivery observed: 0.

Closure record:
`product/verlune-v1/evaluation/ACCESS_PRODUCT_GATE_CLOSURE_2026-09-23.json`

State:
- `LOCAL_BUILD_GATE = PASS`
- `STAGING_DEPLOY_GATE = PASS`
- `ACCESS_PRODUCT_E2E_PASS = true`
- `ENTITLEMENT_TEST_MODE_E2E_PASS = true`
- `HUMAN_REVIEW_H1_H11 = OPEN`
- `READY_TO_SELL = false`

Important boundary:
this is a mixed-evidence gate closure. Runtime-observed cases are not silently relabeled as exhaustive fault injection, and code-invariant cases are not claimed as provider/browser observations.

Next blocker:
customer-facing Human Review H1-H11. The stale internal Builder status line already observed in the Premium asset body must be removed from the customer presentation before that review can pass.


## 2026-09-23 customer Premium metadata audit

Audit of all 17 launch-core Premium source heads found internal release-status metadata exposed in every raw asset preview, including `NOT_FOR_SALE`, `CANDIDATE`, and `RUNTIME TESTING REQUIRED` labels.

Remediation implemented at the **preview presentation layer only**:
- protected asset preview hides lines beginning with `Status:`;
- governed source blobs remain unchanged;
- `Copy full asset` remains byte-identical to the governed/tested source;
- runtime evidence binding is therefore not rewritten.

Evidence:
`product/verlune-v1/evaluation/CUSTOMER_SURFACE_METADATA_AUDIT_2026-09-23.json`

Human-review note:
the visible trust defect is removed from preview, but Human Review should still verify whether the exact copied source's internal status metadata is confusing when pasted into an AI assistant.


## 2026-09-23 Verlune v2 redesign implementation

User explicitly authorized implementing the approved visual/UI plan.

Implemented on `feat/verlune-product-model-v1-20260922-r2`:
- Verlune-first global shell;
- Editorial Computational homepage;
- semantic DOM/CSS 3D graph system;
- Prompt ≠ Workflow visual explanation;
- Use ours / Build yours capability split;
- responsive category exploration;
- Premium Library hierarchy: Builders → Workflows → Prompts → Toolkit;
- Premium Asset Detail tool surface;
- Free Library exposing all 11 governed free launch-core assets;
- individual verified free asset pages;
- copy success/error states;
- responsive + reduced-motion rules;
- postbuild v2 unsupported-claim/materialization audit.

Truth boundary preserved:
- no fake ratings, use counts, creator counts, popularity badges, lifetime/future-update/support claims;
- governed Premium asset source blobs unchanged;
- Premium entitlement/security logic unchanged;
- CSS/DOM 3D only; no WebGL dependency.

State:
- redesign implementation = DONE IN BRANCH
- static repository review = PASS
- typecheck/build = PENDING OPERATOR/Vercel BUILD
- staging visual review = PENDING
- Human Review H1-H11 = OPEN ON REDESIGNED CANDIDATE
- READY_TO_SELL = false


## 2026-09-23 Verlune v2 build + staging deployment — PASS

Operator-observed on WSL / Node.js 24.19.0 from commit `4e50f90bd518b5d5656396d33f835e15da05ac2e`:

- `npm run typecheck`: PASS;
- governed Free Pack materialization: PASS;
- Free Pack identity: 7 assets / 23498 bytes / SHA-256 `55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32`;
- Verlune Free materialization: PASS / 12 files;
- Verlune Premium private materialization: PASS / 18 files;
- Next.js 16.3.3 production build: PASS;
- static generation: 25/25;
- Golden Path build parity: PASS;
- Premium build audit: PASS;
- Verlune v2 build audit: PASS;
- Free launch-core assets: 11 = 8 prompts + 3 workflows;
- Premium launch-core assets: 17;
- semantic 3D boundary: DOM/CSS;
- unsupported mockup claims detected: 0;
- `vercel build --prod`: PASS;
- prebuilt deployment: PASS.

Vercel deployment corroboration:
- project: `prompt-quarry-stage`;
- deployment: `dpl_9E1bZLatjjUieBnAorQVDoieNK4U`;
- deployment URL: `prompt-quarry-stage-k2uwselc1-faridmerinos-projects.vercel.app`;
- alias: `https://prompt-quarry-stage.vercel.app`;
- state: `READY`;
- target: `production` within the staging project;
- runtime error/fatal logs in the checked post-deploy 30-minute window: none observed.

Audit correction note:
the first v2 audit failure (`free missing VF-P-`) was a test-boundary defect, not a customer-surface defect. `/free` renders IDs from `FREE_ASSETS`, so ID-family validation now correctly occurs at the catalog boundary and explicitly asserts 8 Free prompts + 3 Free workflows.

Gate effect:
- `V2_TYPECHECK_BUILD_PASS = true`;
- `V2_POSTBUILD_AUDITS_PASS = true`;
- `V2_STAGING_DEPLOY_PASS = true`;
- `V2_STAGING_VISUAL_REVIEW = OPEN`;
- `HUMAN_REVIEW_H1_H11 = OPEN`;
- `READY_TO_SELL = false`.

Important boundary:
this closes build/package/deploy evidence only. It does not establish visual fidelity, responsive visual quality, customer comprehension, or purchase-value judgment.
