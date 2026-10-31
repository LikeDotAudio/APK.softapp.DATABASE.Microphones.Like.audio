# Part of the APK.audio project — http://APK.audio — made by Anthony Kuzub
# MIT Licence. Full text in LICENSE at the root.
#
# The Microphones page's generated data, built by this repo's own recipe.
#   context: this repository's root
#   last stage `dist` = the docs/data/ tree at /  (config.json, index.json, brands/, rf.json,
#   tags.json, x230.json, x230_report.json)
# A consumer (WEB.Frontend-Assets) copies it beside the committed docs/:
#   COPY --from=microphones-dist / /srv/www/Softapps/DATABASE/DATABASE.Microphones.Like.audio/docs/data
# build_data.py and check_data.py are standard library only; the schema gate
# (docs/validate_research.py, needs jsonschema) runs before deploy, not here.
FROM python:3.12-slim AS build
WORKDIR /src
COPY ["Research", "Research"]
COPY ["docs/*.py", "docs/"]
RUN python3 docs/build_data.py && python3 docs/check_data.py

FROM scratch AS dist
COPY --from=build ["/src/docs/data", "/"]
