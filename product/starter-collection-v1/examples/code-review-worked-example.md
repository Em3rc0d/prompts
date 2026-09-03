# Worked Example — Evidence-first Code Review

**SYNTHETIC EXAMPLE — NOT A RUNTIME OBSERVATION — NOT CUSTOMER EVIDENCE**

Purpose: demonstrate how to supply a bounded Code Review task and what an evidence-disciplined result should look like.

The response below is authored as an illustrative fixture. It is not evidence that a model produced this result.

---

## Example input

### Code / change

```ts
export async function updateEmail(req, res) {
  const account = await db.account.findUnique({
    where: { id: req.params.accountId },
  });

  if (!account) {
    return res.status(404).json({ error: "not_found" });
  }

  await db.account.update({
    where: { id: account.id },
    data: { email: req.body.email },
  });

  return res.json({ ok: true });
}
```

### Change intent / acceptance criteria

Add an authenticated endpoint that lets a signed-in user update **their own** account email. Administrators may update any account.

### Runtime / language context

- TypeScript;
- Express-style request handler;
- authentication middleware supplies `req.user.id` and `req.user.role`;
- `req.params.accountId` is controlled by the caller.

### Expected invariants

A non-admin user must not modify another user's account.

### Observed test evidence

No authorization test result was supplied.

---

## Illustrative expected result shape

### 1. Review state

`REVIEWABLE`

### 2. Executive assessment

The handler updates the account selected directly by `req.params.accountId`, but the supplied acceptance criteria require ownership or administrator authorization. The material risk is an authorization bypass allowing a normal authenticated user to target another account. Ship recommendation: `BLOCK` until the target account is checked against the authenticated principal or an authorized administrator path.

### 3. Material findings

**HIGH — Account ownership is not enforced before the update**

- Evidence level: `CONFIRMED`
- Location: `updateEmail` — lookup/update using `req.params.accountId`
- Evidence: the caller-controlled account ID selects the account; the supplied context says authentication provides `req.user.id`/`req.user.role`; no comparison or admin authorization check exists in the handler.
- Failure mechanism: a normal authenticated user can submit another account ID and the handler proceeds to update that account.
- Impact: unauthorized modification of another user's account email.
- Recommended fix: before updating, require either `req.user.id === account.id` or the explicitly authorized administrator condition; fail closed otherwise.
- Verification: add a regression test proving user A cannot update user B, while self-update and the authorized admin path still succeed.
- Invalidating context: an upstream authorization layer that already proves ownership/admin rights for this exact account ID could invalidate the finding, but no such evidence was supplied.
- Confidence: `high`

### 4. Missing material context

- Whether an upstream route/policy already authorizes `accountId` against the authenticated principal.

This unknown does not erase the finding because no such control appears in the supplied material; it identifies the evidence that could invalidate it.

### 5. Verification plan

1. authenticated user updates own account → allowed;
2. authenticated non-admin user targets another account → denied;
3. authorized administrator targets another account → allowed;
4. nonexistent account → remains a bounded not-found response;
5. regression test executes through the same authorization path used in production.

### 6. Ship recommendation

`BLOCK`

The supplied handler lacks the required ownership/admin authorization check for a caller-controlled account identifier.

---

## Why this example matters

The useful behavior is not merely finding the security issue. The workflow also:

- points to exact supplied evidence;
- explains the mechanism;
- identifies context that could invalidate the finding;
- does not invent a test result;
- keeps the actual ship decision outside the model.

Again: this file is a **synthetic worked example**, not behavioral evidence for the Starter workflow.
