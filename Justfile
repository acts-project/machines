build:
  #!/bin/bash
  files=$(find . -maxdepth 2 -type f -name "Dockerfile")
  for f in $files; do
    context=$(dirname $f)
    docker build $context -f $f
  done


bump:
  #!/usr/bin/env python3
  from pathlib import Path
  import re
  for dir in Path.cwd().iterdir():
    if not dir.is_dir(): continue
    dockerfile = dir / "Dockerfile"
    if not dockerfile.exists(): continue
    print(dockerfile)

    raw = dockerfile.read_text()
    m = re.search(r"LABEL version=\"(\d+)\"", raw)
    assert m is not None, f"{dockerfile} does not have a version label"
    version = int(m.group(1))

    next_version = version + 1

    updated = re.sub(r"LABEL version=\"(\d+)\"", f"LABEL version=\"{next_version}\"", raw)

    dockerfile.write_text(updated)

