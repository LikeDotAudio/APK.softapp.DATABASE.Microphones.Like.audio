# Principles — Microphones.Like.audio

Each principle with the code that keeps it. Ecosystem rules: the APK.audio root's `Documentation/🏛Philosophy/` (cited by path).

| Principle | Kept by |
|---|---|
| **Unknown is NULL, and printed as one.** A parameter that applies but nothing answers is `unknown`, never a guess. Root: `Doctrine/readme.Refusal over fabrication.md`. | `docs/x230_read.py` six-state reading |
| **Do not mark a record down for a question never asked of it.** Non-instantiated blocks, unbound draft parameters and per-unit values leave the denominator; the per-unit keys are named in data, not code. | `docs/x230_read.py:67` `not_scorable` from `Research/aes_x230_profile.json` `crosswalk.not_scorable` |
| **No box without data.** A signal-chain block appears only when an extractor finds its record field; the table under the drawing cites that field. | `docs/js/chain.js`; `vocabulary.MIC_CHAIN` / `RF_CHAIN` |
| **The page ships no vocabulary of its own.** Chips, columns, bands come from `data/config.json`, counted against the corpus; a facet with count 0 never reaches the page. | `docs/build_data.py:105` `build_config()` |
| **Compute once, where it must exist first.** The X230 score is read at build time because the list filters and sorts on it; the browser renders the report, never a second copy. | `docs/build_data.py`; `docs/js/x230view.js` |
| **Inherit only what is unanimous.** | `docs/kits.py:67` `_unanimous()`, `:124` `_inherit()` |
| **Someone else's work stays theirs.** Attribution in the README; images mirrored only to a gitignored `Media/`; the fetcher honours `robots.txt` and goes slowly; the service worker never caches the image CDN. | `.gitignore` (`Media/`); `docs/fetch_media.py`; `docs/sw.js` |
| **Network first.** A cache answers only when the network cannot. | `docs/sw.js` |
| **Publish the site, not the tools.** Every `.py` under `docs/` is excluded from the upload by pattern. | `.github/workflows/deploy.yml` `exclude: **/*.py` |

## Where it falls short
- The dataset is used without the source's permission (stated plainly in the README, with a takedown promise).
- The build warns on form factors with no label in `vocabulary.FORM_LABELS` and still exits 0.
- The apk.audio copy under `APK:Softapps/` has no `docs/data/` (it is not committed and nothing there builds it), so that copy loads no data.
