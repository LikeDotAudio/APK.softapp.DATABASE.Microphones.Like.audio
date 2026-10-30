# Architecture — Microphones.Like.audio

A static browser app (`docs/`) over JSON that a Python build generates from the research datasets (`Research/`). No server code, no framework, no bundler.

## Use it
```bash
python3 docs/build_data.py              # ~1 s; writes docs/data/ (not committed)
python3 -m http.server -d docs 8000     # then http://localhost:8000/
```
HTTP is required: `fetch()` and ES modules are blocked under `file://`, where the page shows a notice instead of data. `pip install jsonschema` is optional (the build then validates the X230 profile against its schema).

## Data flow
```
Research/microphones.json ─┐
Research/Wireless …RF….json ├─► docs/build_data.py ──► docs/data/
Research/aes_x230_profile.json ┘    │  uses vocabulary.py   index.json, brands/<brand>.json,
                                    │       kits.py         tags.json, rf.json, config.json,
                                    │       build_rf.py     x230.json, x230_report.json
                                    │       build_x230.py
                                    └─ x230_read.py (one X230 reading per record)
                                                  │
docs/index.html ── docs/js/main.js ── fetch data/config.json, data/index.json (boot)
                                       data/brands/<brand>.json (on demand)
                                       data/x230_report.json (X230 tab only)
```
- **`build_data.py`** (`main()` at line 289) splits the corpus, builds `config.json` from `vocabulary.py` with every facet counted against the data (`build_config()`, line 105), and prints a warning for each pattern/type/form factor that has no label.
- **`kits.py`** resolves 105 set records to their members; `_inherit()` takes a fact only when every member agrees (`_unanimous()`), and unions patterns/tags/traits.
- **`x230_read.py`** reads each record against the profile into six states (mapped, not implemented, unknown, n/a, open in draft, per-device); the score is mapped ÷ applicable. Keys that only exist on a live unit come from the profile's `crosswalk.not_scorable` (line 67).
- **The browser** (`docs/js/`, one ES module per job: `tree.js`, `models.js`, `detail.js`, `chain.js`/`diagram.js`, `gallery.js`, `tagview.js`, `rfview.js`, `stats.js`, `x230view.js`, …) renders what it is handed; selection lives in the URL hash (`hash.js`).
- **Installable** — `docs/sw.js` (network first, cache `mic-v1`, this origin only) and `docs/js/install.js`.

## Views
Browse (brands → models → device, with polar-pattern and facet filters), Gallery, Tags, Wireless, Statistics (with CSV export of the filtered set), and the X230 tab (the profile explained, both schemas, corpus coverage). Each device page draws its signal chain from `vocabulary.MIC_CHAIN` / `RF_CHAIN`, a block appearing only when an extractor finds the record field behind it.

## Bench tools (never published)
`docs/build_logo.py` draws `docs/icon.svg` and `docs/icons/`; `docs/fetch_media.py` mirrors catalogue images into `Media/` (gitignored), resumable, four workers, `robots.txt` honoured.

## Files
| Path | Role |
|---|---|
| `Research/*.json` | source datasets and schemas (`microphones.json` ~32 MB) |
| `Proposal/AES proposal.md` | concept note: an AES directivity-reporting convention |
| `docs/index.html`, `docs/css/app.css`, `docs/js/` | the app |
| `docs/*.py` | build and bench tools |
| `docs/data/` | generated, not committed |
| `display.json` | launcher manifest (`app: docs/index.html`) |
