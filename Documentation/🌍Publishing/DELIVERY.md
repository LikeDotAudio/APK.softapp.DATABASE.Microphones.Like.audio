# Delivery — Microphones.Like.audio

## Build and test
`python3 docs/build_data.py` regenerates `docs/data/` (checked 2026-10-30: 215 brands, 2,067 microphones + 81 RF systems, 105 kits, 9 of 38 X230 parameters ever answered, median score 44.0%; exits 0 with label warnings). No test suite; the build's own cross-reference checks (and `jsonschema`, if installed) are the checks.

## Where it lands
| Where | How | URL |
|---|---|---|
| **microphones.like.audio** | `.github/workflows/deploy.yml` on a push to `main` touching `docs/**`, the three source JSONs or the workflow (or on demand, with an optional **full_sync**): Python 3.12 runs `docs/build_data.py`, then `SamKirkland/FTP-Deploy-Action@v4.3.5` syncs `docs/` over FTPS using `FTP_SERVER` / `FTP_USERNAME` / `FTP_PASSWORD` and the optional `FTP_SERVER_DIR` variable. Excluded: `.git*`, `**/*.py`, `__pycache__/`, `README.md`. Concurrency group `ftps-deploy`. `.apk.scripts/deploy_all.py` at the APK.audio root re-runs it. | https://microphones.like.audio/ |
| **apk.audio** | the root repo's `ci.yml` FTPS deploy of the Softapps tree (after a submodule bump). `docs/data/` is not committed; since 2026-10-30 `ci.yml` runs `docs/build_data.py` (step *Build the Microphones data*) before the upload. | `https://apk.audio/APK:Softapps/DATABASE/DATABASE.Microphones.Like.audio/docs/index.html` (`docs/data/index.json` was 404 on 2026-10-30, before the next root deploy) |
| **A node** | copied with the Softapps tree into WEB.Frontend-Assets and Storage-Portal; same missing `docs/data/`. The launcher opens the folder (no `entry`, no root page). | — |

## Not automated
- Removing files already on the server: until 2026-10-30 the exclude list was by name, so `kits.py`, `x230_read.py`, `build_logo.py` and `fetch_media.py` are live at microphones.like.audio; a **full_sync** run (or a manual delete) clears them.
- `docs/fetch_media.py` and `docs/build_logo.py` are run by hand.
- Nothing builds `docs/data/` for the apk.audio or node copies.
