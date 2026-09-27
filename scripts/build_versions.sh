#!/usr/bin/env bash
# Build known releases from immutable tags; no remote writes.
set -euo pipefail
output=$1
site_url=$2
repo=$(pwd)
mkdir -p "$output"
output=$(cd "$output" && pwd)
preview=$(mktemp -d)
trap 'rm -rf "$preview"' EXIT
export GIT_AUTHOR_NAME='Site builder' GIT_COMMITTER_NAME='Site builder'
export GIT_AUTHOR_EMAIL='site@example.invalid' GIT_COMMITTER_EMAIL='site@example.invalid'
git -C "$preview" init -q -b source
for version in v1.0 v1.1 v1.2; do
  if ! git rev-parse --verify "refs/tags/$version" >/dev/null 2>&1; then
    continue
  fi
  sha=$(git rev-parse "refs/tags/$version^{commit}")
  git merge-base --is-ancestor "$sha" origin/master
  # Overwrite the entire source snapshot; never mix files from two versions.
  if [ -d "$preview/docs" ]; then rm -rf "$preview/docs"; fi
  git archive "$sha" docs mkdocs.yml | tar -x -C "$preview"
  python - "$preview/mkdocs.yml" "$site_url" <<'PY'
import sys
from pathlib import Path
import yaml
path = Path(sys.argv[1])
config = yaml.safe_load(path.read_text())
config['site_url'] = sys.argv[2]
config['strict'] = True
path.write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False))
PY
  git -C "$preview" add docs mkdocs.yml
  git -C "$preview" -c core.hooksPath=/dev/null commit -qm "Source $version" --allow-empty
  (cd "$preview" && "$repo/.venv/bin/mike" deploy --update-aliases "$version" latest)
  latest=$version
done
: "${latest:?No supported release tags found}"
(cd "$preview" && "$repo/.venv/bin/mike" set-default latest)
git -C "$preview" archive gh-pages | tar -x -C "$output"
# Identify both the release and source commit for post-deploy verification.
python - "$output" "$repo" <<'PY'
import json, subprocess, sys
from pathlib import Path
out, repo = Path(sys.argv[1]), sys.argv[2]
for item in json.loads((out / 'versions.json').read_text()):
    version = item['version']
    sha = subprocess.check_output(['git', '-C', repo, 'rev-parse', f'{version}^{{commit}}'], text=True).strip()
    (out / version / 'release.json').write_text(json.dumps({'version': version, 'commit': sha}))
PY
