from flask import Flask, request, jsonify
import ezdxf
import os

app = Flask(__name__)

OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "Python DXF Server Running"

@app.route("/generate", methods=["POST"])
def generate():
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Draw a simple rectangle (78 ft × 35 ft converted to mm approximately)
    msp.add_lwpolyline([
        (0,0),
        (23774,0),
        (23774,10668),
        (0,10668),
        (0,0)
    ])

    msp.add_text("Sample Floor Plan", height=300).set_placement((500,11000))

    file = os.path.join(OUTPUT_FOLDER,"sample.dxf")
    doc.saveas(file)

    return jsonify({
        "success": True,
        "file": file
    })

if __name__ == "__main__":
    app.run(port=5000)