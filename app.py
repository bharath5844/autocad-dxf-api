from flask import Flask, request, jsonify
import ezdxf
import os

app = Flask(__name__)

OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return "AutoCAD DXF API Running"


@app.route("/generate", methods=["POST"])
def generate():

    data = request.json

    project = data.get("project", "Project")
    rooms = data.get("rooms", [])

    doc = ezdxf.new("R2018")
    msp = doc.modelspace()

    # Outer plot (temporary)
    plot_width = 23774
    plot_height = 10668

    msp.add_lwpolyline([
        (0, 0),
        (plot_width, 0),
        (plot_width, plot_height),
        (0, plot_height),
        (0, 0)
    ])

    x = 500
    y = plot_height - 500

    row_height = 0
    margin = 300

    for room in rooms:

        name = room.get("name", "Room")

        width = int(room.get("widthMm", 3000))
        length = int(room.get("lengthMm", 3000))

        # Move to next row if required
        if x + width > plot_width - 500:
            x = 500
            y -= row_height + margin
            row_height = 0

        # Draw room
        msp.add_lwpolyline([
            (x, y),
            (x + width, y),
            (x + width, y - length),
            (x, y - length),
            (x, y)
        ])

        # Room name
        msp.add_text(
            name,
            height=250
        ).set_placement(
            ((x + width / 2), (y - length / 2))
        )

        x += width + margin

        row_height = max(row_height, length)

    filename = project.replace(" ", "_") + ".dxf"

    filepath = os.path.join(OUTPUT_FOLDER, filename)

    doc.saveas(filepath)

    return jsonify({
        "success": True,
        "file": filepath
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
