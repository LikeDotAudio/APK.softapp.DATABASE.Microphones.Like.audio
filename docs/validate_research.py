#!/usr/bin/env python3
# Part of the APK.audio project — http://APK.audio — made by Anthony Kuzub
# MIT Licence. Full text in LICENSE at the root.
"""Validate Research/*.json against the tracked JSON Schemas — the pre-deploy gate.

    pip install 'jsonschema>=4.10'      (the build itself stays standard-library only)
    python3 docs/validate_research.py   exit 0 = valid, 1 = a record breaks its schema

What is checked, and against which schema:
  Research/microphones.json            every record: an RF record (classification.kind
                                       "rf") against rf_component.schema.json, every other
                                       against microphone.schema.json
  Wireless Microphone_RF_Components    as build_rf.load() normalises it, against
                                       rf_component.schema.json (the raw file is a nested
                                       string tree the schema does not describe)
  aes_x230_profile.json                against aes_x230_profile.schema.json
  every record's AES-X230 reading      x230_read.Reader.read(), against
                                       aes_x230_device.schema.json
and every *.schema.json is itself checked as a valid 2020-12 schema.

Warnings (printed, never fatal): derived blocks the build recomputes (x230, kit) that
are also committed in the source file, and RF records sitting inside microphones.json.
"""
import glob
import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RESEARCH = os.path.join(ROOT, "Research")
sys.path.insert(0, HERE)

try:
    import jsonschema
except ImportError:
    sys.exit("validate_research.py needs jsonschema: pip install 'jsonschema>=4.10'")

import build_rf as rf          # noqa: E402  (the build's own normaliser)
import build_x230 as x230      # noqa: E402
import x230_read               # noqa: E402

MAX_SHOWN = 25


def load(name):
    with open(os.path.join(RESEARCH, name), encoding="utf-8") as fh:
        return json.load(fh)


def validator(name):
    schema = load(name)
    jsonschema.Draft202012Validator.check_schema(schema)
    return jsonschema.Draft202012Validator(schema)


def main():
    errors, warnings = [], []
    for path in sorted(glob.glob(os.path.join(RESEARCH, "*.schema.json"))):
        try:
            validator(os.path.basename(path))
        except jsonschema.SchemaError as e:
            errors.append(f"{os.path.basename(path)}: not a valid schema: {e.message}")
    if errors:
        return report(errors, warnings)

    mic_v, rf_v = validator("microphone.schema.json"), validator("rf_component.schema.json")
    profile_v, device_v = validator("aes_x230_profile.schema.json"), validator("aes_x230_device.schema.json")

    mics = load("microphones.json")
    derived, rf_inside = Counter(), 0
    for i, rec in enumerate(mics):
        is_rf = (rec.get("classification") or {}).get("kind") == "rf"
        rf_inside += is_rf
        for key in ("x230", "kit"):
            derived[key] += key in rec
        name = (rec.get("identity") or {}).get("full_name") or f"#{i}"
        for e in (rf_v if is_rf else mic_v).iter_errors(rec):
            where = "/".join(str(p) for p in e.absolute_path)
            errors.append(f"microphones.json {name}: {where}: {e.message[:200]}")
    for key, n in derived.items():
        if n:
            warnings.append(f"microphones.json: {n} records carry the derived `{key}` block; "
                            "the build recomputes it, so the committed copy is stale by construction")
    keys = Counter(((r.get("source") or {}).get("brand_slug"), (r.get("source") or {}).get("model_slug"))
                   for r in mics if (r.get("classification") or {}).get("kind") != "rf")
    for (brand, model), n in sorted(keys.items(), key=lambda kv: str(kv[0])):
        if n > 1:
            warnings.append(f"microphones.json: {brand}/{model} is listed {n} times with different content; "
                            "the build keeps the last — decide which is right")
    if rf_inside:
        warnings.append(f"microphones.json: {rf_inside} RF records are committed inside the microphone "
                        "dataset; build_rf.py also loads RF from its own source")

    build_warnings = []
    rf_records = rf.load(build_warnings.append)
    for rec in rf_records:
        for e in rf_v.iter_errors(rec):
            errors.append(f"RF (normalised) {rec['identity'].get('full_name')}: "
                          f"{'/'.join(map(str, e.absolute_path))}: {e.message[:200]}")

    profile_doc = load("aes_x230_profile.json")
    for e in profile_v.iter_errors(profile_doc):
        errors.append(f"aes_x230_profile.json: {'/'.join(map(str, e.absolute_path))}: {e.message[:200]}")

    profile = x230.load(build_warnings.append)
    readings = 0
    if profile:
        reader = x230_read.Reader(profile)
        for rec in mics + rf_records:
            readings += 1
            for e in device_v.iter_errors(reader.read(rec)):
                errors.append(f"X230 reading of {(rec.get('identity') or {}).get('full_name')}: "
                              f"{'/'.join(map(str, e.absolute_path))}: {e.message[:200]}")
    else:
        errors.append("aes_x230_profile.json could not be loaded by build_x230.load()")
    warnings.extend(f"build: {w}" for w in build_warnings)

    print(f"checked {len(mics)} microphone-dataset records, {len(rf_records)} normalised RF records, "
          f"the X230 profile and {readings} X230 readings")
    return report(errors, warnings)


def report(errors, warnings):
    for w in warnings:
        print("WARN", w)
    for e in errors[:MAX_SHOWN]:
        print("FAIL", e)
    if len(errors) > MAX_SHOWN:
        print(f"FAIL … and {len(errors) - MAX_SHOWN} more")
    if errors:
        print(f"{len(errors)} schema error(s)")
        return 1
    print("OK every Research record conforms to its schema")
    return 0


if __name__ == "__main__":
    sys.exit(main())
