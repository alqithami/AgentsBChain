#!/usr/bin/env python3
"""Validate repository schemas and example artifacts.

This script is intentionally lightweight: it checks that JSON files parse,
that JSON Schemas are valid Draft-07 schemas, and that the provided example
TIS/PDR payloads conform to their schemas.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft7Validator, validate

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema(schema_path: Path) -> dict[str, Any]:
    schema = load_json(schema_path)
    Draft7Validator.check_schema(schema)
    print(f"[ok] schema is valid Draft-07: {schema_path.relative_to(ROOT)}")
    return schema


def validate_payload(payload_path: Path, schema: dict[str, Any]) -> None:
    payload = load_json(payload_path)
    validate(instance=payload, schema=schema)
    print(f"[ok] payload validates: {payload_path.relative_to(ROOT)}")


def validate_yaml(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)
    print(f"[ok] yaml parses: {path.relative_to(ROOT)}")


def main() -> int:
    tis_schema = validate_schema(ROOT / "schemas" / "tis-schema.json")
    pdr_schema = validate_schema(ROOT / "schemas" / "pdr-schema.json")

    validate_payload(ROOT / "examples" / "tis-swap-example.json", tis_schema)
    validate_payload(ROOT / "examples" / "pdr-approval-example.json", pdr_schema)

    for yaml_file in sorted((ROOT / "configs").glob("*.yaml")):
        validate_yaml(yaml_file)

    print("\nAll repository artifacts validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
