# Agents on Blockchains: Reference Implementations

This repository contains the reference implementations and sample configurations for the systematic literature review: **"Autonomous Agents on Blockchains: Standards, Execution Models, and Trust Boundaries"** (Alqithami, 2026).

## Contents

### 1. Schemas (`/schemas`)

The schemas directory contains the JSON Schema (Draft-07) definitions for the proposed intent and policy frameworks:

- **`tis-schema.json`**: The Transaction Intent Schema (TIS). A chain-agnostic schema for expressing desired outcomes and constraints for on-chain execution.
- **`pdr-schema.json`**: The Policy Decision Record (PDR). A signed policy attestation regarding a specific TIS, binding the evaluated intent hash, decision outcome, and constraints.
- **`TIS_NOTES.md`**: Implementation notes regarding canonicalization, hashing, and the verification flow.

### 2. Sample Configurations (`/configs`)

The configs directory contains YAML examples illustrating how the concepts discussed in the survey translate into practical agent deployments across different conformance levels:

- **`conservative-defi-agent.yaml`**: Prioritizes safety over performance, suitable for managing significant value with minimal risk tolerance (L3 Conformance).
- **`active-trading-agent.yaml`**: Prioritizes performance and responsiveness, suitable for strategies requiring rapid execution (L2 Conformance).
- **`governance-agent.yaml`**: Manages voting and delegation across multiple DAOs with specialized policy controls.

## Usage

These schemas and configurations are provided as reference architectures for researchers and practitioners building autonomous agents that interact with blockchain networks. They are designed to be modular, extensible, and chain-agnostic.

## Citation

If you use these reference implementations in your research or systems, please cite the accompanying paper:

```bibtex
@article{alqithami2026agents,
  title={Autonomous Agents on Blockchains: Standards, Execution Models, and Trust Boundaries},
  author={Alqithami, S.},
  journal={TBD},
  year={2026}
}
```
