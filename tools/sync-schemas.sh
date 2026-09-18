#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🔄 Generating TypeScript types from Pydantic schemas..."

# Ensure we are tracking files recursively
find ./backend/app/schemas/ -type f -name "*.py" | while read -r file; do
    # Extract relative path and replace extension
    rel_path="${file#./backend/app/schemas}"
    ts_path="${rel_path%.py}.ts"
    out_file="./frontend/src/types/api/$ts_path"
    
    # Create the matching directory structure in frontend
    mkdir -p "$(dirname "$out_file")"
    
    # Run the compiler
    echo "  📄 Compiling: $file -> $out_file"
    pydantic2ts --module "$file" --output "$out_file"
done

echo "✅ TypeScript types generated successfully!"