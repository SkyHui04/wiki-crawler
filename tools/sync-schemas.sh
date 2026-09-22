#!/usr/bin/env bash

set -Eeuo pipefail

json2ts_cmd="${JSON2TS_CMD:-./node_modules/.bin/json2ts}"

if [[ ! -x "$json2ts_cmd" ]]; then
    echo "Cannot find json2ts at: $json2ts_cmd" >&2
    exit 1
fi

echo "Generating TypeScript types from Pydantic schemas..."

find ./backend/app/schemas/ \
    -type f \
    -name "*.py" \
    -print0 |
while IFS= read -r -d '' file; do
    rel_path="${file#./backend/app/schemas}"
    ts_path="${rel_path%.py}.ts"
    out_file="./frontend/src/types/api/$ts_path"

    mkdir -p "$(dirname "$out_file")"

    echo "Compiling: $file -> $out_file"

    pydantic2ts \
        --module "$file" \
        --output "$out_file" \
        --json2ts-cmd "$json2ts_cmd"
done

echo "TypeScript types generated successfully!"