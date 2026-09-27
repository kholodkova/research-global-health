#!/usr/bin/env bash
# HTTP 200, expected source SHA, and a real result page; retry CDN propagation.
set -euo pipefail
base=${1%/}
version=$2
sha=$3
attempts=${HEALTHCHECK_ATTEMPTS:-18}
for attempt in $(seq 1 "$attempts"); do
  if python - "$base" "$version" "$sha" <<'PY'
import json, sys
from urllib.request import Request, urlopen
base, version, sha = sys.argv[1:]
def read(path):
    req = Request(f'{base}/{path}', headers={'Cache-Control': 'no-cache'})
    with urlopen(req, timeout=15) as response:
        if response.status != 200:
            raise ValueError(f'HTTP {response.status}')
        return response.read().decode('utf-8')
try:
    assert json.loads(read(f'{version}/release.json')) == {'version': version, 'commit': sha}
    assert 'DALY' in read(f'{version}/lab2/p5/results/')
    versions = json.loads(read('versions.json'))
    assert any(v['version'] == version for v in versions)
except Exception as error:
    print(f'Healthcheck failed: {type(error).__name__}: {error}', file=sys.stderr)
    sys.exit(1)
print(f'Healthcheck passed: {version} {sha}')
PY
  then exit 0; fi
  if [ "$attempt" -lt "$attempts" ]; then sleep 10; fi
done
exit 1
