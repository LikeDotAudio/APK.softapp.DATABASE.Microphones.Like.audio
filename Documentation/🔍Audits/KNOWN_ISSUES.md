# Known Issues — Microphones.Like.audio

Measured 2026-10-30.

- **Stale tool files on the live site.** `https://microphones.like.audio/kits.py`, `x230_read.py`, `build_logo.py` and `fetch_media.py` answer 200 — uploaded before `deploy.yml` excluded `**/*.py`. A full_sync deploy removes them.
- **The APK:Softapps copy has no data.** `docs/data/` is generated and not committed; on apk.audio and in the node images the page loads but `data/index.json` is 404.
- **Unlabelled form factors.** `build_data.py` warns for form factors such as `wireless_capsule` and `End-address Yoke Mount` that `vocabulary.FORM_LABELS` does not name.
- **Launcher opens the folder.** `display.json` has no `entry` and the repo root has no page, so the OS walker lists it as a folder app; `app: docs/index.html` is not read by that walker.
