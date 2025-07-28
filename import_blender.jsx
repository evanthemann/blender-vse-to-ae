/* ------------------------------------------------------------------
   json2.js  (tiny JSON.parse polyfill for ExtendScript)
   Only the parse part is included.
------------------------------------------------------------------- */
if (typeof JSON !== 'object') { JSON = {}; }
(function () {
    if (typeof JSON.parse !== 'function') {
        JSON.parse = function (text) {
            text = String(text);
            var cx = /[\u0000-\u001F\u007F-\u009F]/g;
            if (cx.test(text)) { text = text.replace(cx, ''); }
            return eval('(' + text + ')');
        };
    }
}());

/* ---------------- ASK FOR JSON FILE ---------------- */
var jsonFile = File.openDialog("Select the VSE export JSON", "*.json");
if (!jsonFile) {
    alert("❌ No file selected. Exiting.");
    throw new Error("User cancelled");
}
var jsonPath = jsonFile.fsName;

/* ---------------- CONFIG ---------------- */
var compName = "Blender_VSE";
/* ---------------------------------------- */

/* ---------- READ THE JSON FILE ---------- */
var f = File(jsonPath);
if (!f.exists) {
    alert("JSON file not found:\n" + jsonPath);
    throw new Error("JSON not found");
}
f.open("r");
var jsonStr = f.read();
f.close();

var data = JSON.parse(jsonStr);     // now safe even in old AE

/* --------- GLOBAL PROJECT INFO ---------- */
var fps          = data.fps || 30;
var compW        = data.comp_width  || 1920;
var compH        = data.comp_height || 1080;
var compDuration = data.comp_duration || 60.0;
var clips        = data.clips || [];

if (clips.length === 0) {
    alert("No clips found in JSON.");
    throw new Error("No clips.");
}

/* ------------ CREATE COMP --------------- */
var proj = app.project || app.newProject();
var comp  = proj.items.addComp(compName, compW, compH, 1.0, compDuration, fps);

/* ------------ SORT CLIPS FIRST ----------- */
// Channel: lowest first (bottom), highest last (top)
// Timeline: earliest first
clips.sort(function(a, b) {
    if (a.channel !== b.channel) {
        return a.channel - b.channel;
    }
    return a.timeline_start - b.timeline_start;
});

/* ------------- IMPORT & PLACE ----------- */
app.beginUndoGroup("Import Blender Timeline");

for (var i = 0; i < clips.length; i++) {
    var c = clips[i];
    var srcFile = File(c.filepath);

    if (!srcFile.exists) {
        alert("Missing media:\n" + c.filepath);
        continue;
    }
    var footage   = proj.importFile(new ImportOptions(srcFile));
    var layer     = comp.layers.add(footage);

    var timelineStart = c.timeline_start;   // seconds
    var inPoint       = c.in_point;         // seconds
    var outPoint      = c.out_point;        // seconds
    var duration      = outPoint - inPoint; // seconds

    // --- Scale ---
    var scaleX = (c.scale_x || 1.0) * 100; // AE scale is in %
    var scaleY = (c.scale_y || 1.0) * 100;
    layer.property("Scale").setValue([scaleX, scaleY]);

    // --- Position ---
    var translateX = c.translate_x || 0.0;
    var translateY = c.translate_y || 0.0;

    // Blender’s VSE origin is bottom-left, AE’s is center. Adjust accordingly.
    var pos = layer.property("Position").value;
    pos[0] += translateX; 
    pos[1] -= translateY;  // Flip Y axis
    layer.property("Position").setValue(pos);

    layer.startTime = timelineStart - inPoint;
    layer.inPoint   = timelineStart;
    layer.outPoint  = timelineStart + duration;
}

app.endUndoGroup();
alert("✅ Imported " + clips.length + " clips into comp: " + compName);
