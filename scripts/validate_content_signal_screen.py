#!/usr/bin/env python3
"""Mechanical validator for Content Signal Screen v0.1 artifacts."""

import argparse
import json
import sys
from pathlib import Path

SCHEMA_VERSION = "0.1"
RISKS = {"low", "medium", "high", "indeterminate"}
COVERAGE = {"metadata_only", "sampled_content", "full_content", "other"}
RATINGS = {"strong", "mixed", "weak", "unknown"}
CONFIDENCE = {"low", "medium", "high"}
SIGNALS = {
    "concrete_takeaway",
    "source_specificity",
    "author_footprint",
    "cognitive_progress",
}
FORBIDDEN_KEYS = {
    "ai_generated",
    "truth_score",
    "author_intent",
    "automatic_action",
    "telemetry",
    "upload_source",
    "durable_writeback",
    "install_skill",
    "project_route",
}
REQUIRED = {
    "schema_version",
    "source",
    "slop_risk",
    "basis",
    "input_coverage",
    "inspected_sections",
    "signals",
    "uncertainty",
    "not_inferred",
    "recommended_next_gate",
    "writeback_status",
}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def report(status, errors=None, warnings=None):
    return {
        "status": status,
        "schema_version": SCHEMA_VERSION,
        "errors": errors or [],
        "warnings": warnings or [],
    }


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return report("invalid", ["root must be a JSON object"])

    forbidden = sorted(FORBIDDEN_KEYS.intersection(data))
    if forbidden:
        errors.append("forbidden top-level keys: " + ", ".join(forbidden))

    missing = sorted(REQUIRED - set(data))
    if missing:
        errors.append("missing required keys: " + ", ".join(missing))

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append("unsupported schema_version: expected 0.1")

    source = data.get("source")
    if not isinstance(source, dict):
        errors.append("source must be an object")
    else:
        for key in ("title", "path_or_url", "source_type", "sensitivity"):
            if not nonempty(source.get(key)):
                errors.append(f"source.{key} must be a nonempty string")

    if data.get("slop_risk") not in RISKS:
        errors.append("slop_risk must be one of: low, medium, high, indeterminate")

    if data.get("input_coverage") not in COVERAGE:
        errors.append("input_coverage must be one of: metadata_only, sampled_content, full_content, other")

    inspected = data.get("inspected_sections")
    if not isinstance(inspected, list) or not all(nonempty(item) for item in inspected):
        errors.append("inspected_sections must be a list of nonempty strings")
    elif data.get("input_coverage") != "metadata_only" and not inspected:
        errors.append("inspected_sections must be nonempty unless input_coverage is metadata_only")

    for key in ("basis", "uncertainty", "not_inferred", "recommended_next_gate"):
        if not nonempty(data.get(key)):
            errors.append(f"{key} must be a nonempty string")

    signals = data.get("signals")
    if not isinstance(signals, dict):
        errors.append("signals must be an object")
    else:
        missing_signals = sorted(SIGNALS - set(signals))
        extra_signals = sorted(set(signals) - SIGNALS)
        if missing_signals:
            errors.append("missing signals: " + ", ".join(missing_signals))
        if extra_signals:
            errors.append("unsupported signals: " + ", ".join(extra_signals))
        for name in SIGNALS.intersection(signals):
            item = signals[name]
            if not isinstance(item, dict):
                errors.append(f"signals.{name} must be an object")
                continue
            if not nonempty(item.get("evidence")):
                errors.append(f"signals.{name}.evidence must be a nonempty string")
            if item.get("rating") not in RATINGS:
                errors.append(f"signals.{name}.rating must be one of: strong, mixed, weak, unknown")
            if item.get("confidence") not in CONFIDENCE:
                errors.append(f"signals.{name}.confidence must be one of: low, medium, high")

    if data.get("writeback_status") != "none":
        errors.append("writeback_status must be none")

    if errors:
        return report("invalid", errors)
    return report("valid")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate a Content Signal Screen v0.1 JSON artifact")
    parser.add_argument("artifact", help="path to a JSON artifact")
    args = parser.parse_args(argv)
    try:
        with Path(args.artifact).open("r", encoding="utf-8-sig") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps(report("usage_or_io_error", [str(exc)]), ensure_ascii=False))
        return 1
    result = validate(data)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "valid" else 2


if __name__ == "__main__":
    sys.exit(main())
