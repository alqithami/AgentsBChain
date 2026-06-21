# Agents on Blockchains: Reference Implementations

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2601.04583-b31b1b.svg)](https://arxiv.org/abs/2601.04583)

This repository contains the reference implementations, schemas, validation utilities, and configurations for the systematic literature review: **"Autonomous Agents on Blockchains: Standards, Execution Models, and Trust Boundaries"** (Alqithami, 2026).

## Contents

### 1. Schemas (`/schemas`)

The schemas directory contains JSON Schema (Draft-07) definitions for the proposed intent and policy frameworks:

- **`tis-schema.json`**: The Transaction Intent Schema (TIS). A chain-agnostic schema for expressing desired outcomes and constraints for on-chain execution.
- **`pdr-schema.json`**: The Policy Decision Record (PDR). A signed policy attestation regarding a specific TIS, binding the evaluated intent hash, decision outcome, and constraints.
- **`TIS_NOTES.md`**: Implementation notes regarding canonicalization, hashing, and the verification flow.

### 2. Sample Configurations (`/configs`)

The configs directory contains YAML examples illustrating how the concepts discussed in the survey translate into practical agent deployments across different conformance levels:

- **`conservative-defi-agent.yaml`**: Prioritizes safety over performance, suitable for managing significant value with minimal risk tolerance (L3 Conformance).
- **`active-trading-agent.yaml`**: Prioritizes performance and responsiveness, suitable for strategies requiring rapid execution (L2 Conformance).
- **`governance-agent.yaml`**: Manages voting and delegation across multiple DAOs with specialized policy controls.

### 3. Implementation Examples (`/examples`)

Detailed implementation walkthroughs and machine-readable payloads for the integration patterns identified in the survey:

- **`pattern-iii-payment-agent.md`**: Simple recurring payment agent using ERC-4337 smart accounts with session keys and on-chain policy enforcement (Pattern III: Delegated Execution).
- **`pattern-iv-rebalancing-agent.md`**: Autonomous portfolio rebalancing agent using MPC custody, off-chain policy engines, and the TIS/PDR workflow (Pattern IV: Autonomous Signing).
- **`pattern-v-dao-treasury.md`**: Multi-agent DAO treasury management pipeline with specialized strategy, risk, and execution agents (Pattern V: Multi-Agent Workflows).
- **`tis-swap-example.json`**: A concrete TIS swap intent payload that validates against `schemas/tis-schema.json`.
- **`pdr-approval-example.json`**: A concrete PDR approval payload that validates against `schemas/pdr-schema.json`.

### 4. Validation (`/scripts` and GitHub Actions)

The repository includes a lightweight validation workflow to make the artifacts auditable and easier to reuse.

Run locally:

```bash
python -m pip install -r requirements.txt
python scripts/validate_artifacts.py
```

The same checks run through GitHub Actions on push and pull request via `.github/workflows/validate-artifacts.yml`.

## Usage

These schemas, configurations, and examples are provided as reference architectures for researchers and practitioners building autonomous agents that interact with blockchain networks. They are designed to be modular, extensible, and chain-agnostic.

Recommended implementation flow:

1. Construct a TIS object from the agent's proposed action.
2. Canonicalize and hash the TIS object.
3. Submit the TIS to a policy engine.
4. Emit a signed PDR that binds the policy decision to the TIS hash.
5. Require the signer or execution environment to verify the PDR before authorizing any transaction.
6. Log the TIS, PDR, transaction hash, and post-execution receipt for audit and replay.

## Citation

If you use these reference implementations in your research or systems, please cite the accompanying paper:

```bibtex
@misc{alqithami2026agents,
      title={Autonomous Agents on Blockchains: Standards, Execution Models, and Trust Boundaries},
      author={Saad Alqithami},
      year={2026},
      eprint={2601.04583},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2601.04583},
}
```
