"""
wall_generator.py

Utility functions to draw architectural walls in DXF.
"""

WALL_THICKNESS_EXTERIOR = 230   # mm
WALL_THICKNESS_INTERIOR = 115   # mm


def draw_wall_rectangle(
    msp,
    x,
    y,
    width,
    length,
    wall_thickness=WALL_THICKNESS_EXTERIOR,
    layer="WALLS"
):
    """
    Draws a room with wall thickness.

    Parameters
    ----------
    msp : ezdxf.modelspace
        AutoCAD modelspace

    x, y : int
        Top-left corner

    width : int
        Room width in mm

    length : int
        Room length in mm

    wall_thickness : int
        Wall thickness in mm
    """

    # ---------------------------
    # Outside wall
    # ---------------------------

    outer = [
        (x, y),
        (x + width, y),
        (x + width, y - length),
        (x, y - length),
        (x, y)
    ]

    msp.add_lwpolyline(
        outer,
        close=True,
        dxfattribs={
            "layer": layer
        }
    )

    # ---------------------------
    # Inside wall line
    # ---------------------------

    ix = x + wall_thickness
    iy = y - wall_thickness

    inner = [
        (ix, iy),
        (x + width - wall_thickness, iy),
        (x + width - wall_thickness, y - length + wall_thickness),
        (ix, y - length + wall_thickness),
        (ix, iy)
    ]

    msp.add_lwpolyline(
        inner,
        close=True,
        dxfattribs={
            "layer": layer
        }
    )


def draw_room_label(
    msp,
    x,
    y,
    width,
    length,
    name,
    layer="TEXT"
):
    """
    Draw room name.
    """

    msp.add_text(
        name,
        dxfattribs={
            "height": 220,
            "layer": layer
        }
    ).set_placement(
        (
            x + width / 2,
            y - length / 2
        )
    )
