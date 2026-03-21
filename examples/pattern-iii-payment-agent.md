# Pattern III: Simple Payment Agent (Delegated Execution)

## Goal

An agent that executes a recurring payment on behalf of a user, such as paying a monthly 10 USDC subscription to a streaming service.

## Architecture

This use case exemplifies **Pattern III: Delegated Execution**. The agent should not have unconditional signing authority. It only requires narrowly scoped authority to perform a single action under strict, smart-contract-enforced constraints. The recommended architecture is an **ERC-4337 smart account** with a policy module (e.g., a session-key module or a Zodiac Roles modifier) that bounds agent authority on-chain.

## Detailed Setup and Configuration

1. **Smart Account:** The user controls an ERC-4337 smart account (e.g., a Safe{Wallet}-based account abstraction implementation).

2. **Session Key Generation:** During subscription enrollment, the dApp generates a fresh keypair locally (browser or mobile secure enclave). The public key, denoted `0xAgentSessionKey`, will be authorized as a limited session key.

3. **Policy Module Installation:** The dApp prepares a transaction to install and configure an on-chain policy module (e.g., Zodiac Roles or a bespoke session-key module). The user approves a single transaction that:
   - installs the module on the smart account;
   - registers `0xAgentSessionKey` as an authorized delegate; and
   - encodes hard constraints that the module enforces on every delegated execution.

### Illustrative On-Chain Constraints

```solidity
require(recipient == 0xStreamingServiceAddress);
require(amount <= 10 * 1e6);        // 10 USDC
require(block.timestamp >= lastPaymentTimestamp + 30 days);
require(block.timestamp < keyExpiryTimestamp);
```

These constraints form the core security boundary: even if the agent is compromised, the maximum damage is bounded by on-chain logic that it cannot bypass.

## Detailed Execution Flow

On the due date, the agent (e.g., a constrained backend job operated by the streaming service) constructs and submits a `UserOperation` under ERC-4337.

### Agent Log (Example)

```
[2026-07-15 08:00:00] INFO: Triggered billing cycle for account 0xUserSmartAccountAddress.
[2026-07-15 08:00:02] INFO: Payment due (last payment: 2026-06-15).
[2026-07-15 08:00:03] INFO: Constructing UserOperation: transfer 10 USDC to 0xStreamingServiceAddress.
[2026-07-15 08:00:04] INFO: Signing UserOperation with session key 0xAgentSessionKey.
[2026-07-15 08:00:05] INFO: Submitting UserOperation to bundler endpoint.
[2026-07-15 08:00:20] INFO: Awaiting receipt..
[2026-07-15 08:00:35] INFO: SUCCESS: Included in block 21000000.
[2026-07-15 08:00:36] INFO: Updating subscription status in application database.
```

### UserOperation Payload (Schematic)

```json
{
  "sender": "0xUserSmartAccountAddress",
  "nonce": "0x..",
  "callData": "0x..",
  "signature": "0x..",
  "paymasterAndData": "0xPaymasterAddress.."
}
```

### On-Chain Verification (ERC-4337 Path)

1. A bundler includes the `UserOperation` in a bundle to the `EntryPoint`.
2. `EntryPoint` calls `validateUserOp` on `0xUserSmartAccountAddress`.
3. The smart account delegates validation to the installed policy module.
4. The policy module verifies:
   - the signature corresponds to `0xAgentSessionKey`; and
   - the execution satisfies all constraints (recipient, amount cap, cadence, expiry).
5. If valid, `EntryPoint` executes the call (USDC `transfer`) via the smart account.

## Security Analysis

- **Attack Surface:** Minimal and sharply bounded. The worst-case loss is capped at 10 USDC per interval, enforced by immutable on-chain checks.
- **Key Management:** The agent never touches the user's master key. Session keys are single-purpose and time-limited.
- **Trust Boundary:** Trust is anchored in audited on-chain modules rather than in the correctness of the agent runtime.
