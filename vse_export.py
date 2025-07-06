"""
Blender VSE → JSON timeline export
"""
import bpy, json, os, math

# ========= CONFIG =========
output_path = "/Users/evanmann/blender_vse_to_ae_comp/vse_export.json"
# ==========================

scene = bpy.context.scene
fps = scene.render.fps / scene.render.fps_base     # true FPS (handles 23.976)
width  = scene.render.resolution_x
height = scene.render.resolution_y

# Ensure VSE exists
if not scene.sequence_editor:
    bpy.ops.sequencer.sequencer_toggle()

clips_json = []
max_out_sec = 0.0

for s in scene.sequence_editor.sequences_all:
    if s.type != 'MOVIE':
        continue

    # -------- raw frame values --------
    frame_start        = s.frame_start
    offset_start       = s.frame_offset_start
    duration           = s.frame_final_duration

    # -------- convert to seconds --------
    timeline_start_s   = (frame_start + offset_start) / fps
    in_point_s         = offset_start / fps
    out_point_s        = (offset_start + duration) / fps

    # Track comp duration
    max_out_sec = max(max_out_sec, timeline_start_s + (out_point_s - in_point_s))

    clips_json.append({
        "name": s.name,
        "filepath": bpy.path.abspath(s.filepath),
        "timeline_start": round(timeline_start_s, 3),
        "in_point": round(in_point_s, 3),
        "out_point": round(out_point_s, 3)
    })

# -------- assemble full JSON --------
export_data = {
    "fps": round(fps, 3),
    "comp_width": width,
    "comp_height": height,
    "comp_duration": round(max_out_sec, 3),
    "clips": clips_json
}

# -------- write file --------
try:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=4)
    print(f"✅ Exported {len(clips_json)} clips from VSE")
    print(f"→ {output_path}")
except Exception as e:
    print("❌ Failed to write JSON:", e)
