# Implementation Examples

This directory contains detailed implementation examples that illustrate the integration patterns described in the companion survey. Each example includes architecture descriptions, sample payloads, execution flows, and security analysis.

## Examples

### 1. Simple Payment Agent (Pattern III)

**File:** `pattern-iii-payment-agent.md`

A recurring payment agent using ERC-4337 smart accounts with session keys and on-chain policy modules. Demonstrates bounded delegation with minimal attack surface.

### 2. Portfolio Rebalancing Agent (Pattern IV)

**File:** `pattern-iv-rebalancing-agent.md`

An autonomous portfolio rebalancing agent using MPC custody, off-chain policy engines, and the TIS/PDR workflow. Demonstrates defense-in-depth with distributed signing authority.

### 3. Multi-Agent DAO Treasury Management (Pattern V)

**File:** `pattern-v-dao-treasury.md`

A multi-agent governance pipeline for DAO treasury management with specialized strategy, risk, and execution agents. Demonstrates separation of duties with on-chain governance enforcement.
