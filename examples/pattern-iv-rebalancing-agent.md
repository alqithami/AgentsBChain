# Pattern IV: Autonomous Portfolio Rebalancing Agent (Autonomous Signing)

## Goal

An agent that manages a user's DeFi portfolio, targeting a desired allocation (e.g., 50% ETH, 25% WBTC, 25% USDC) by rebalancing when deviations exceed a threshold.

## Architecture

This use case aligns with **Pattern IV: Autonomous Signing**. It demands stronger controls than Pattern III because the agent is empowered to initiate economically meaningful actions. The recommended architecture is a **defense-in-depth** stack combining distributed custody (MPC), policy enforcement (off-chain policy engine), and MEV-aware execution (private relays and intent-based venues).

## Detailed Setup and Configuration

1. **Custody and Signing (Distributed Control):** Funds are held in a **2-of-3 MPC wallet**:
   - **Share 1 (Agent-side):** Held in a hardened environment (e.g., HSM or enclave-backed service).
   - **Share 2 (User-side):** Held on the user's mobile device with biometric approval.
   - **Share 3 (Recovery):** Stored on a hardware wallet as a recovery/quorum path.

2. **Policy Engine (Contextual Constraints):** The user configures an off-chain policy engine (e.g., Turnkey-like controls) with:
   - target allocation and deviation thresholds (rebalance when deviation >2%);
   - allowlist of protocols and routes (e.g., Uniswap V3, Aave V3);
   - daily turnover caps (e.g., ≤25% of portfolio value).

## Detailed Execution Flow (TIS/PDR Model)

This execution uses the proposed **TIS/PDR separation of duties**: the agent proposes a bounded intent (TIS), the policy engine produces a signed compliance artifact (PDR), and the signer enforces both before producing a signature.

### Agent Log (Example)

```
[14:00:05] INFO: Allocation observed: 47.5% ETH, 26.0% WBTC, 26.5% USDC.
[14:00:06] WARN: ETH below threshold (48%). Rebalance required.
[14:00:08] INFO: Proposed action: swap 5,000 USDC for WETH via Uniswap V3.
[14:00:09] INFO: Constructing TIS.
[14:00:10] INFO: Submitting TIS to policy engine.
[14:00:12] INFO: Received signed PDR (APPROVE).
[14:00:13] INFO: Submitting TIS+PDR to MPC signing workflow.
[14:00:25] INFO: User approved on mobile (2-of-3 met).
[14:00:26] INFO: Submitting signed transaction to private relay for MEV mitigation.
[14:00:41] INFO: Confirmed execution; updated allocation: 49.8% ETH.
```

### TIS Payload (Example)

```json
{
  "intentId": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
  "action": "SWAP",
  "inputs": [
    { "token": "0xa0b8..", "amount": "5000000000", "constraint": "EXACT" }
  ],
  "outputs": [
    { "token": "0xc02a..", "amount": "1500000000000000000", "constraint": "MINIMUM" }
  ],
  "constraints": { "deadline": 1767230000 },
  "preview": "Swap exactly 5,000 USDC for a minimum of 1.5 WETH to rebalance portfolio."
}
```

### PDR Payload (Decoded Example)

```json
{
  "iss": "https://policy.turnkey.com",
  "sub": "0xUserAddress",
  "aud": "https://signer.fireblocks.com",
  "exp": 1767229800,
  "intent_hash": "0xkeccak256(TIS_payload)",
  "decision": "APPROVE",
  "bound_constraints": { "max_gas_fee": "60000000000" }
}
```

## Security Analysis

- **Defense-in-Depth:** A single compromise (agent runtime, one MPC share, or a tool) is insufficient to drain funds. Adversaries must defeat multiple independent controls.
- **Auditability:** TIS and PDR provide durable artifacts for forensic review and compliance: the proposed intent, the policy rationale, and the signed decision can be retained and re-verified.
- **Operational Kill Switch:** The user can revoke the agent share, tighten policy thresholds, or invalidate the policy issuer key, immediately reducing authority without redeploying on-chain code.
