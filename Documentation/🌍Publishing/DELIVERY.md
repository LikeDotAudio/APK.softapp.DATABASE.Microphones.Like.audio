# Delivery — Microphones.Like.audio

## Build and test
`python3 docs/validate_research.py` (needs `jsonschema`) validates every Research record against its schema; `python3 docs/build_data.py` regenerates `docs/data/` (checked 2026-10-30: 214 brands, 1,983 microphones + 81 RF systems, 105 kits; exits 0 with label warnings); `python3 docs/check_data.py` checks the built tree. `deploy.yml` runs all three before the FTPS step. `Docker/dist.Dockerfile` builds the same `docs/data/` as an image stage (`dist`), for WEB.Frontend-Assets.

## Where it lands
| Where | How | URL |
|---|---|---|
| **microphones.like.audio** | `.github/workflows/deploy.yml` on a push to `main` touching `docs/**`, the three source JSONs or the workflow (or on demand, with an optional **full_sync**): Python 3.12 runs `docs/validate_research.py` (with `jsonschema==4.23.0`), `docs/build_data.py` and `docs/check_data.py`, then `SamKirkland/FTP-Deploy-Action@v4.3.5` syncs `docs/` over FTPS using `FTP_SERVER` / `FTP_USERNAME` / `FTP_PASSWORD` and the optional `FTP_SERVER_DIR` variable. Excluded: `.git*`, `**/*.py`, `__pycache__/`, `README.md`. Concurrency group `ftps-deploy`. `.apk.scripts/deploy_all.py` at the APK.audio root re-runs it. | https://microphones.like.audio/ |
| **apk.audio** | the root repo's `ci.yml` FTPS deploy of the Softapps tree (after a submodule bump). `docs/data/` is not committed; since 2026-10-30 `ci.yml` runs `docs/build_data.py` (step *Build the Microphones data*) before the upload. | `https://apk.audio/APK:Softapps/DATABASE/DATABASE.Microphones.Like.audio/docs/index.html` (`docs/data/index.json` was 404 on 2026-10-30, before the next root deploy) |
| **A node** | copied with the Softapps tree into WEB.Frontend-Assets and Storage-Portal; same missing `docs/data/`. The launcher opens the folder (no `entry`, no root page). | — |

## Not automated
- Removing files already on the server: until 2026-10-30 the exclude list was by name, so `kits.py`, `x230_read.py`, `build_logo.py` and `fetch_media.py` are live at microphones.like.audio; a **full_sync** run (or a manual delete) clears them.
- `docs/fetch_media.py` and `docs/build_logo.py` are run by hand.
- Nothing builds `docs/data/` for the apk.audio or node copies.

## Delivered from the 2026-10-30 audit

- **Research validated against its schemas, as a gate** — `docs/validate_research.py` (microphones → `microphone.schema.json`, RF records → `rf_component.schema.json`, `build_rf.load()` output → `rf_component.schema.json`, the X230 profile and all 2,148 X230 readings → their schemas). All 2,067 microphone records failed the stale schema, so `microphone.schema.json` and `rf_component.schema.json` were brought up to the data (additive: fields from the post-scrape imports, observed enum values, the build-derived `x230`/`kit`/`is_kit`/`transducer_types` declared as such). `deploy.yml` runs it before the build and FTPS. Kept out of `build_data.py` so the build stays standard-library (the image stage has no pip). Verified: OK on the real data; a copy with `transducer_type: "laser"` and a string `msrp_amount` → 2 FAILs.
- **Post-build check of `docs/data/`** — `docs/check_data.py`; it found a real bug: the 82 RF records committed inside `microphones.json` were counted twice (index 18 Lectrosonics rows, brand file 9). `build_data.py` now ignores RF copies in the microphone dataset (RF comes from its own source) and keeps the last of a duplicated brand/model (as the brand file already did), with warnings. Verified: `build_data.py && check_data.py` → OK, 2,064 models in 214 brand files.
- **Corpus stamp** — `config.json` `corpus` = build date, source SHA-256 (12 hex), counts; shown on the Statistics view.
- **One AES proposal** — `Documentation/🧩Manual and Artifacts/AES_proposal.md` is now a pointer to `Proposal/AES proposal.md`.
- **Inert `topic` dropped** from `display.json`, and the counts in its description removed (they live in the corpus stamp).
- **Theme** — Kept by design: the APK shell publishes no theme to follow (no shared key or message); the page follows `prefers-color-scheme` like the shell and keeps `mic-theme` only for a visitor's own toggle on microphones.like.audio.
- **dist build contract for WEB.Frontend-Assets (W09 handoff)** — `Docker/dist.Dockerfile` (context = this repo; `.dockerignore` beside it), last stage `FROM scratch AS dist` = `docs/data/` at `/`, built by `build_data.py` and checked by `check_data.py`. Verified: `docker build --target dist` succeeds and the image holds `brands/…`, `config.json` etc.
- **WS-07 accent token** (from the SDK/contracts audit) — `docs/css/app.css` `--accent`/`--accent-text` read `var(--apk-accent)` from `docs/vendor/apk-contracts/apk-tokens.css` (vendored with `.apk.scripts/vendor_contract_web.py`, `--check`: ok), linked before `app.css` and precached by `sw.js` (cache `mic-v2`). Verified: headless Chrome computes `--accent` = `#f4902c`; the page renders 2,064 models.
- **Source dataset cleaned** (owner decision) — `Research/microphones.json` lost the 82 RF records that duplicated `Wireless Microphone_RF_Components.json`, the derived `x230` (1,982) and `kit` (105) blocks with the kit-derived `classification.is_kit`/`transducer_types`, and the earlier copy of each duplicated Universal Audio model (SD-1, Sphere DLX; same `added_date`, so the later one in the file was kept; the dropped copies differed only in the derived `x230`). 2,067 → 1,983 records, ~32 → ~24 MB. `build_data.py` keeps its guards in case copies return. Verified: `validate_research.py` OK with no source warnings; `build_data.py && check_data.py` OK, 2,064 models in 214 brand files (unchanged from what the guarded build already served).

## Delivered 2026-11-11 – 2026-11-12

From this repository's own commits (the commit message is the record):

- vendor: apk-contracts web bundle refreshed from contracts/generated/web (report.ts: LogLine + ProblemRecord, System/Problems family) (`7e9d366`)
- vendor/apk-softapp: re-vendored — every problem card is reported through the SDK (ROAD-3695 step 2) (`a2250f3`)
- vendor: apk-contracts web bundle refreshed from contracts/generated/web (five report codes, ROAD-3695; unit-gate, ROAD-3684) (`d91fe78`)
- re-vendor apk-contracts web bundle: contracts 2.4.0 retires APK.audio/Tests/{suite} (ROAD-3729) (`fbeda5c`)

## Releases
- **Released `2.0.0`, tag `v2.0.0`** (2026-11-01, ROAD-3452, the owner's V2) — no SDK pin; every manifest says 2.0.0; GitHub release `v2.0.0`.
