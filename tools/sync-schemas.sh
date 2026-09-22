#!/usr/bin/env bash

set -Eeuo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

echo "Generating TypeScript types from Pydantic schemas..."

while IFS= read -r -d '' file; do
    rel_path="${file#"$repo_root/backend/app/schemas"}"
    ts_path="${rel_path%.py}.ts"
    out_file="$repo_root/frontend/src/types/api$ts_path"

    mkdir -p "$(dirname "$out_file")"

    echo "Compiling: $file -> $out_file"
    pydantic2ts --module "$file" --output "$out_file"
done < <(
    find "$repo_root/backend/app/schemas" \
        -type f \
        -name "*.py" \
        -print0
)

echo "TypeScript types generated successfully."