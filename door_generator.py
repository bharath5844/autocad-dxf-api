"""
door_generator.py
Draw simple door openings in room walls.
"""

MAIN_DOOR = 1200
ROOM_DOOR = 900
BATH_DOOR = 750
POOJA_DOOR = 750


def get_door_width(room_name: str) -> int:
    room = room_name.lower()

    if "wash" in room or "toilet" in room or "bath" in room:
        return BATH_DOOR

    if "pooja" in room:
        return POOJA_DOOR

    if "living" in room:
        return MAIN_DOOR

    return ROOM_DOOR


def draw_door(
    msp,
    x,
    y,
    width,
    room_name,
    layer="DOORS"
):
    """
    Draw a simple door opening on the bottom wall.
    """

    door_width = get_door_width(room_name)

    start_x = x + (width - door_width) / 2
    end_x = start_x + door_width

    # Left wall segment
    msp.add_line(
        (x, y),
        (start_x, y),
        dxfattribs={"layer": layer}
    )

    # Right wall segment
    msp.add_line(
        (end_x, y),
        (x + width, y),
        dxfattribs={"layer": layer}
    )
