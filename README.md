# blender-vse-to-ae

Simple tool to export Blender Video Sequence Editor (VSE) timeline data to JSON for After Effects timeline reconstruction.

## Features

- Exports clip info (file path, timing) from one or all Blender VSE tracks
- Outputs JSON formatted for easy AE scripting import
- Converts frame data to seconds based on Blender project FPS

## Usage

1. Open Blender and your VSE project.
2. Adjust and run the Python exporter script (`vse_exporter.py`).
3. The script outputs a JSON file with timeline and clip info.
4. Run the After Effects JSX importer script (`import_blender_timeline.jsx`) to rebuild the timeline.

## Configuration

- Set `channel_to_export` in the Blender script to choose VSE track(s).
- Set `output_path` to where JSON is saved.
- Set JSON file path in AE JSX script accordingly.

## Requirements

- Blender with scripting enabled
- After Effects with ExtendScript support

---

Happy editing!  
— Evan Mann
