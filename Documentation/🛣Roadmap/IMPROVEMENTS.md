# 🛣 Improvements — DATABASE.Microphones.Like.audio (from the 2026-10-30 architecture audit)

What this repo should change to meet the standard, most valuable first. Source: [🔍Audits/ARCHITECTURE-AUDIT.md](../%F0%9F%94%8DAudits/ARCHITECTURE-AUDIT.md).
← [Roadmap](INDEX.md)

Delivered items are in [🌍Publishing/DELIVERY.md](../%F0%9F%8C%8DPublishing/DELIVERY.md#delivered-from-the-2026-10-30-audit). Still open:

| # | Improvement | Category | Effort (S/M/L) | Evidence |
|---|---|---|---|---|
| 1 | Strip from `Research/microphones.json` the 82 RF copies and the build-derived `x230`/`kit` blocks, and settle the two duplicated Universal Audio models. **Needs owner** (research data). The build already ignores/recomputes them and `validate_research.py` warns. | Change management | S | `python3 docs/validate_research.py` warnings |
