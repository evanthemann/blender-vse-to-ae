#!/bin/bash

# Ask for the .blend file path
read -rp "Enter the full path to your Blender file (.blend): " blend_file

# Remove escape characters (when dragging/dropping with backslashes)
blend_file="${blend_file//\\}"

# Check file exists and is .blend
if [[ ! -f "$blend_file" || "${blend_file##*.}" != "blend" ]]; then
    echo "❌ File does not exist or is not a .blend file: $blend_file"
    exit 1
fi

# Path to Blender executable
BLENDER_PATH="/Applications/Blender.app/Contents/MacOS/Blender"

# Run Blender headless with the export script
"$BLENDER_PATH" -b "$blend_file" --python vse_export.py

echo "✅ Done! Check the JSON export in the same folder as your .blend file."

