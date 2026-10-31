# 🔍 Architecture audit — DATABASE.Microphones.Like.audio (2026-10-30)

Audited against the APK.audio multi-repo architecture standard: coupling, boundaries, duplication, contracts.
← [Audits](INDEX.md) · Improvements: [🛣Roadmap/IMPROVEMENTS.md](../%F0%9F%9B%A3Roadmap/IMPROVEMENTS.md)

## Bounded context
The microphone and wireless-RF catalogue published at microphones.like.audio and as an APK Softapp: a ~33 MB research corpus (`Research/microphones.json` + RF + AES-X230 profile, each with a JSON Schema), Python build scripts that derive `docs/data/` from it, and a vanilla ES-module PWA (`docs/js/`, 27 modules). **Sampled:** `.github/workflows/deploy.yml`, `display.json`, `docs/index.html`, `docs/js/{config,theme}.js`, `docs/build_data.py` (imports, schema use), `Research/` listing, Documentation tree.

## Context map
| Talks to | How (topic / endpoint / file / import) | Relationship |
|---|---|---|
| microphones.like.audio (FTPS host) | `deploy.yml`: `python3 docs/build_data.py`, then `SamKirkland/FTP-Deploy-Action@v4.3.5` uploads `docs/` | delivery |
| WEB.OsApi project-app walker | `display.json` (`app: APK:Softapps/DATABASE/…/docs/index.html`) | Customer–Supplier (OsApi supplies) |
| WEB.Frontend-Assets image | carries the folder with the other Softapps | baked in by design |
| Manufacturer sites | `docs/fetch_media.py` (offline, polite, robots.txt honoured) | none at runtime |
| MQTT bus | none (the inert `topic` was dropped) | — |

## Scorecard
| Category | Score (0–3) | Finding |
|---|---|---|
| Coupling & Cohesion | 3 | Self-contained: no references into other repos; the page fetches only its own `data/*.json`; deploys on its own. |
| Boundary Integrity | 3 | The schemas are enforced at the Research boundary (`validate_research.py`) and the built tree at the page boundary (`check_data.py`) (delivered). |
| Duplication Control | 3 | One AES proposal; the accent is the contracts token (delivered). The theme key is kept by design. |
| Testing & Contracts | 3 | Schema gate + post-build check run in `deploy.yml` before FTPS (delivered). |
| Change management | 2 | Corpus stamp in `config.json`, shown on the page (delivered). The source file still carries copies the build ignores, and two duplicate models — needs owner. |
Score key: 3 meets the standard · 2 minor gaps · 1 significant gaps · 0 absent / violated.

## Findings
1. **Good — vocabulary is data, not code.** `docs/js/config.js`: "Nothing here is a literal: change a facet in vocabulary.py, rebuild, and the UI follows"; facets with zero count never reach the page.
2. **The source dataset carries derived and foreign copies.** `Research/microphones.json` holds 82 RF records (duplicates of what `build_rf.py` reads from its own source; they made every wireless brand's index count double until the build began ignoring them), `x230` on 2,064 records and `kit` on 105 (both recomputed by the build), and Universal Audio SD-1 / Sphere DLX twice with different content. `validate_research.py` warns on each. **Needs owner:** strip the copies from the source and pick the right duplicate.
3. **Pre-existing audit notes** (`Deep Research Audit.md`, `Missing *.md`, `KNOWN_ISSUES.md`) cover data completeness, not architecture; they are left as they are.

Delivered items were removed from this page; see [🌍Publishing/DELIVERY.md](../%F0%9F%8C%8DPublishing/DELIVERY.md#delivered-from-the-2026-10-30-audit).
