# blender-vse-to-ae

> **🗄️ Archived — this tool has moved.**
>
> The actively maintained version now lives inside the
> [**video-intake-pipeline**](https://github.com/evanthemann/video-intake-pipeline)
> repo as the optional `after-effects/` add-on. See
> [**`after-effects/README.md`**](https://github.com/evanthemann/video-intake-pipeline/blob/main/after-effects/README.md)
> for current install + usage.
>
> The version over there has been standardized to match the rest of the
> pipeline's idioms (drag-and-drop input, `find_blender` auto-discovery,
> ANSI status output, end-of-script next-step hints, embedded Blender
> Python payload pattern — same shape as the other pipeline scripts).
> The code below is the original proof-of-concept; this repo is kept
> read-only for history.

---

Simple tool to export Blender Video Sequence Editor (VSE) timeline to JSON to import into After Effects composition.

## Features

- Exports clip info (file path, timing) from all Blender VSE tracks
- Outputs JSON for AE import
- Converts frame data to seconds based on Blender project FPS

## Usage

1. Open Blender and your VSE project.
2. Go to Python Console.
3. Paste: `exec(open("/path/to/vse_export.py").read())`
4. A JSON file will be created with timeline and clip info.
5. Open After Effects and go to File > Run Scripts.
6. Run (`import_blender.jsx`).

## Configuration

- Update filepaths in `vse_export.py` and `import_blender.jsx`

## Requirements

- Blender 
- After Effects 

---