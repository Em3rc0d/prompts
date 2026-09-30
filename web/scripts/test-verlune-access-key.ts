import assert from "node:assert/strict";

import {
  createVerluneAccessKeyWithSecret,
  deriveVerluneEntitlementIdWithSecret,
  verifyVerluneAccessKeyWithSecret,
  VERLUNE_ACCESS_KEY_PATTERN
} from "../lib/verlune-access-key.ts";

const secret = "test-only-secret-1234567890-abcdefghijklmnopqrstuvwxyz";
const product = "verlune-premium-v1";
const canonicalEmail = "buyer@example.com";

const keyA = createVerluneAccessKeyWithSecret("  Buyer@Example.com  ", secret, product);
const keyB = createVerluneAccessKeyWithSecret(canonicalEmail, secret, product);
const entitlementA = deriveVerluneEntitlementIdWithSecret("BUYER@example.com", secret, product);
const entitlementB = deriveVerluneEntitlementIdWithSecret(canonicalEmail, secret, product);
const otherKey = createVerluneAccessKeyWithSecret("other@example.com", secret, product);

assert.equal(keyA, keyB, "trim + lowercase must preserve the canonical Access Key");
assert.equal(entitlementA, entitlementB, "trim + lowercase must preserve the entitlement identity");
assert.notEqual(keyA, otherKey, "different emails must not share an Access Key");
assert.match(keyA, VERLUNE_ACCESS_KEY_PATTERN, "Access Key must match the VLK1 format");
assert.equal(verifyVerluneAccessKeyWithSecret(canonicalEmail, keyA, secret, product), true);
assert.equal(verifyVerluneAccessKeyWithSecret("other@example.com", keyA, secret, product), false);
assert.equal(
  verifyVerluneAccessKeyWithSecret(canonicalEmail, keyA.slice(0, -1) + (keyA.endsWith("A") ? "B" : "A"), secret, product),
  false,
  "mutated key must fail verification"
);

console.log("VERLUNE ACCESS KEY DETERMINISM: PASS");
console.log("identity=product+normalized_email+versioned_secret");
console.log("same_email_same_key=true");
console.log("different_email_different_key=true");
