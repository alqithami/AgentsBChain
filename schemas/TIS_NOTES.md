# Transaction Intent Schema (TIS) -- Implementation Notes

## Canonicalization and Hashing

Implementations SHOULD canonicalize TIS objects prior to hashing and signing (e.g., stable JSON serialization with deterministic key ordering per [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785)). This is required to ensure that different clients compute the same hash for the same semantic intent.

## Extension Points

Future extensions can be added by introducing additional action types under `definitions/actions/*` and by extending `metadata`, `constraints`, or `preferences` with new fields. Backward compatibility SHOULD be maintained via versioning.

## Verification and Execution Flow (TIS + PDR)

The TIS and PDR together support a multi-stage execution flow:

1. **Intent Creation:** The agent constructs a TIS object.
2. **Policy Evaluation:** The agent submits the TIS to the policy engine.
3. **PDR Generation:** The policy engine evaluates the TIS and, if approved, emits a signed PDR.
4. **Execution Request:** The agent submits the TIS and PDR to the signing environment (e.g., MPC service, HSM, or TEE).
5. **Signer Verification:** The signing environment verifies:
   - The signature on the PDR against a trusted policy-engine public key.
   - The hash of the canonicalized TIS matches `tisHash`.
   - `expiresAt` has not elapsed and `audience` matches the signer identity.
   - Any `boundConstraints` and `modifiedParameters` are enforced prior to signing.
