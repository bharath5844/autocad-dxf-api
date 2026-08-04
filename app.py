from flask import Flask, request, jsonify, send_file
import ezdxf
import os
import re

app = Flask(__name__)

OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return "AutoCAD DXF API Running"


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json(silent=True) or {}

    project = data.get("project", "Project")
    rooms = data.get("rooms", [])

    plot = data.get("plot", {})
    plot_width = int(plot.get("width", 23774))
    plot_height = int(plot.get("length", 10668))

    doc = ezdxf.new("R2018")
    msp = doc.modelspace()

    # Plot boundary
    msp.add_lwpolyline([
        (0, 0),
        (plot_width, 0),
        (plot_width, plot_height),
        (0, plot_height),
        (0, 0)
    ], close=True)

    # Plot title
    msp.add_text(
        f"Project : {project}",
        height=300
    ).set_placement((500, plot_height + 600))

    x = 500
    y = plot_height - 500

    row_height = 0
    margin = 300

    for room in rooms:

        name = room.get("name", "Room")

        width = int(room.get("widthMm", 3000))
        length = int(room.get("lengthMm", 3000))

        # Next row if room exceeds plot width
        if x + width > plot_width - 500:
            x = 500
            y -= row_height + margin
            row_height = 0

        # Draw room rectangle
        msp.add_lwpolyline([
            (x, y),
            (x + width, y),
            (x + width, y - length),
            (x, y - length),
            (x, y)
        ], close=True)

        # Room label
        msp.add_text(
            f"{name}\n{width} x {length} mm",
            height=220
        ).set_placement(
            (x + width / 4, y - length / 2)
        )

        x += width + margin

        row_height = max(row_height, length)

    # Safe filename
    safe_project = re.sub(r'[^A-Za-z0-9_-]', '_', project)

    filename = safe_project + ".dxf"

    filepath = os.path.join(OUTPUT_FOLDER, filename)

    doc.saveas(filepath)

    return jsonify({
        "success": True,
        "file": filename,
        "download_url": f"/download/{filename}"
    })


@app.route("/download/<filename>")
def download(filename):

    filepath = os.path.join(OUTPUT_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({
            "success": False,
            "message": "File not found"
        }), 404

    return send_file(
        filepath,
        as_attachment=True,
        download_name=filename,
        mimetype="application/dxf"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
