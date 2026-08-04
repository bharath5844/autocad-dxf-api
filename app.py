from flask import Flask, request, jsonify, send_file
import ezdxf
import os
import re

from layout_engine import generate_layout
from wall_generator import draw_wall_rectangle, draw_room_label

app = Flask(__name__)

OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return "AutoCAD DXF API Running"


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json(silent=True) or {}

    print("REQUEST DATA:", data)

    project = data.get("project", "Project")
    rooms = data.get("rooms", [])

    # Plot Size (78 x 35 ft)
    plot_width = 23774
    plot_height = 10668

    # Create DXF
    doc = ezdxf.new("R2018")
    msp = doc.modelspace()

    # -----------------------------
    # Create Layers
    # -----------------------------
    if "WALLS" not in doc.layers:
        doc.layers.add("WALLS")

    if "TEXT" not in doc.layers:
        doc.layers.add("TEXT")

    # -----------------------------
    # Draw Plot Boundary
    # -----------------------------
    msp.add_lwpolyline(
        [
            (0, 0),
            (plot_width, 0),
            (plot_width, plot_height),
            (0, plot_height),
            (0, 0)
        ],
        close=True,
        dxfattribs={
            "layer": "WALLS"
        }
    )

    # -----------------------------
    # Project Title
    # -----------------------------
    msp.add_text(
        f"Project : {project}",
        dxfattribs={
            "height": 300,
            "layer": "TEXT"
        }
    ).set_placement(
        (500, plot_height + 600)
    )

    # -----------------------------
    # Generate Room Layout
    # -----------------------------
    layout = generate_layout(
        plot_width,
        plot_height,
        rooms
    )

    # -----------------------------
    # Draw Rooms
    # -----------------------------
    for room in layout:

        draw_wall_rectangle(
            msp=msp,
            x=room["x"],
            y=room["y"],
            width=room["width"],
            length=room["length"]
        )

        draw_room_label(
            msp=msp,
            x=room["x"],
            y=room["y"],
            width=room["width"],
            length=room["length"],
            name=room["name"]
        )

    # -----------------------------
    # Save File
    # -----------------------------
    filename = re.sub(
        r"[^A-Za-z0-9_-]",
        "_",
        project
    ) + ".dxf"

    filepath = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    doc.saveas(filepath)

    return jsonify({
        "success": True,
        "file": filename,
        "download_url": f"/download/{filename}"
    })


@app.route("/download/<filename>")
def download(filename):

    filepath = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

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
    app.run(
        host="0.0.0.0",
        port=port
    )
