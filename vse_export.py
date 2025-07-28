"""
Blender VSE → JSON timeline export
"""
import bpy, json, os

scene = bpy.context.scene
fps = scene.render.fps / scene.render.fps_base
width = scene.render.resolution_x
height = scene.render.resolution_y

# Ensure VSE exists
if not scene.sequence_editor:
    bpy.ops.sequencer.sequencer_toggle()

# Dynamically set export path based on .blend file
blend_path = bpy.data.filepath
if not blend_path:
    print("❌ Please save the .blend file before running.")
    exit(1)

blend_dir = os.path.dirname(blend_path)
blend_name = os.path.splitext(os.path.basename(blend_path))[0]
output_path = os.path.join(blend_dir, f"{blend_name}_vse_export.json")

clips_json = []
max_out_sec = 0.0

for s in scene.sequence_editor.sequences_all:
    if s.type != 'MOVIE':
        continue

    frame_start = s.frame_start
    offset_start = s.frame_offset_start
    duration = s.frame_final_duration

    timeline_start_s = (frame_start + offset_start) / fps
    in_point_s = offset_start / fps
    out_point_s = (offset_start + duration) / fps

    max_out_sec = max(max_out_sec, timeline_start_s + (out_point_s - in_point_s))

    clips_json.append({
        "name": s.name,
        "filepath": bpy.path.abspath(s.filepath),
        "timeline_start": round(timeline_start_s, 3),
        "in_point": round(in_point_s, 3),
        "out_point": round(out_point_s, 3),
        "channel": s.channel,  # Track number
        # Add transform properties if they exist
        "scale_x": getattr(s.transform, "scale_x", 1.0),
        "scale_y": getattr(s.transform, "scale_y", 1.0),
        "translate_x": getattr(s.transform, "offset_x", 0.0),
        "translate_y": getattr(s.transform, "offset_y", 0.0)
    })

export_data = {
    "fps": round(fps, 3),
    "comp_width": width,
    "comp_height": height,
    "comp_duration": round(max_out_sec, 3),
    "clips": clips_json
}

try:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=4)
    print(f"✅ Exported {len(clips_json)} clips from VSE")
    print(f"→ {output_path}")
except Exception as e:
    print("❌ Failed to write JSON:", e)
