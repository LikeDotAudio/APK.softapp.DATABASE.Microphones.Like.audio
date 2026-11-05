/* The SDK seam — window.APKSoftapp (vendor/apk-softapp, a classic script that
   index.html loads before this module). A failure becomes what happened / why /
   do this, with Retry; without the SDK every helper here says so by returning
   false and the caller keeps its own plain line. */

const sdk = () => window.APKSoftapp;

/* A non-2xx answer, carrying a problems-catalogue code (wire constants only). */
export function httpError(res, file) {
  const s = res.status;
  const code = s === 404 || s === 410 ? "http_not_found"
    : s === 401 || s === 403 ? "http_forbidden"
    : s === 408 || s === 504 ? "timeout"
    : s >= 500 ? "http_server_error" : "fetch_failed";
  return Object.assign(new Error("HTTP " + s + " loading " + file), { code, status: s });
}

export const BUILD_STEP = "Generate the data first: python3 docs/build_data.py (nothing under docs/data/ is committed).";

/* Draw `err` into `slot` (an element) as a problem card. → true when drawn. */
export function problemInto(slot, err, { subject, onRetry, fix = [BUILD_STEP], code } = {}) {
  const S = sdk();
  if (!S || !slot) return false;
  // explain() names the code; problem() is what carries our own first steps.
  const e = code ? null : S.explain(err, { subject });
  const p = S.problem(code || e.code, { detail: code ? err && err.message : e.detail, subject, fix });
  S.showProblem(p, { into: slot, onRetry });
  return true;
}

export function describeApp() {
  const S = sdk();
  if (!S) return;
  S.describe({
    name: "Microphones",
    does: "Browse microphones and wireless systems: polar patterns, frequency plots, signal chains, AES-X230 readings, tags, statistics and CSV export.",
    inputs: [
      { name: "Vocabulary (chips, columns, dropdowns)", from: "data/config.json — made by docs/build_data.py", kind: "file" },
      { name: "Model index and brand files", from: "data/index.json, data/brands/<brand>.json", kind: "file" },
      { name: "Tags, wireless systems, X230 profile", from: "data/tags.json, data/rf.json, data/x230.json, data/x230_report.json (fetched on first use)", kind: "file" },
      { name: "Search and filters", from: "the search box (/ focuses it), type/trait chips, form, price, X230 band, sort, pattern bar" },
    ],
    outputs: [
      { name: "CSV export", to: "microphones-<n>.csv in your Downloads folder (Explorer view)", kind: "file" },
      { name: "Permalinks", to: "the URL hash — every model, tag and view is a link" },
      { name: "Theme choice", to: "this browser (localStorage mic-theme)" },
    ],
    controls: [
      { name: "Browse / Gallery / Wireless / Tags / Statistics / X230", how: "top navigation" },
      { name: "Search", how: "type; / focuses it, Esc clears it" },
      { name: "Step through models", how: "ArrowUp / ArrowDown on the browse view" },
      { name: "Reset filters", how: "the Reset chip" },
      { name: "Theme", how: "the theme button cycles dark / light / system" },
      { name: "Install", how: "the install offer adds it as an app" },
    ],
    problems: ["unsupported_browser", "fetch_failed", "http_not_found", "bad_json"],
  });
}
