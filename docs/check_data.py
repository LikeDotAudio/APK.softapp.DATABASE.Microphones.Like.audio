#!/usr/bin/env python3
# Part of the APK.audio project — http://APK.audio — made by Anthony Kuzub
# MIT Licence. Full text in LICENSE at the root.
"""Check the built docs/data/ — the contract the page reads — after build_data.py.

    python3 docs/build_data.py && python3 docs/check_data.py    exit 0 = shippable

  config.json   every vocabulary the page builds from is present and non-empty, and
                the corpus stamp (built, source_sha256, counts) is there
  index.json    totals are non-zero and agree with the brand list; every brand's
                detail file brands/<file>.json exists and holds that brand's count
  rf.json, tags.json, x230.json, x230_report.json   present and parse
Standard library only.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
# What docs/js reads off config at boot (config.js, filters.js, explorer.js, csv.js, stats.js).
CONFIG_LISTS = ("types", "forms", "kinds", "sorts", "patterns", "explorerColumns", "csvColumns",
                "priceBands", "availability", "statAttributes", "typeSeriesKeys")


def load(name, failures):
    path = os.path.join(DATA, name)
    if not os.path.isfile(path):
        failures.append(f"data/{name} is missing")
        return None
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except ValueError as e:
        failures.append(f"data/{name} is not JSON: {e}")
        return None


def main():
    failures = []
    config = load("config.json", failures)
    if config is not None:
        for key in CONFIG_LISTS:
            if not config.get(key):
                failures.append(f"config.json: `{key}` is missing or empty")
        if not isinstance(config.get("page"), int) or config["page"] <= 0:
            failures.append("config.json: `page` is not a positive integer")
        corpus = config.get("corpus") or {}
        for key in ("built", "source_sha256", "microphones", "rf", "brands"):
            if key not in corpus:
                failures.append(f"config.json: corpus stamp lacks `{key}`")
    index = load("index.json", failures)
    if index is not None:
        brands = index.get("brands") or []
        if not index.get("total_models") or not brands:
            failures.append("index.json: no models or no brands")
        if index.get("total_brands") != len(brands):
            failures.append(f"index.json: total_brands {index.get('total_brands')} != {len(brands)} listed")
        if sum(b.get("count", 0) for b in brands) != index.get("total_models"):
            failures.append("index.json: brand counts do not add up to total_models")
        for b in brands:
            detail = load(os.path.join("brands", b["file"] + ".json"), failures)
            if detail is not None and len(detail) != b["count"]:
                failures.append(f"brands/{b['file']}.json holds {len(detail)} records, index says {b['count']}")
    for name in ("rf.json", "tags.json", "x230.json", "x230_report.json"):
        load(name, failures)
    for f in failures[:40]:
        print("FAIL", f)
    if failures:
        print(f"{len(failures)} problem(s) in docs/data/")
        return 1
    print(f"OK docs/data/ is complete: {index['total_models']} models in {len(brands)} brand files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
