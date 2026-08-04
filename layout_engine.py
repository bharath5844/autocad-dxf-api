def generate_layout(plot_width, plot_length, rooms):
    """
    Returns room positions.

    Output:
    [
        {
            "name": "...",
            "x": ...,
            "y": ...,
            "width": ...,
            "length": ...
        }
    ]
    """

    layout = []

    x = 500
    y = plot_length - 500

    row_height = 0
    margin = 300

    for room in rooms:

        width = room["widthMm"]
        length = room["lengthMm"]

        if x + width > plot_width - 500:
            x = 500
            y -= row_height + margin
            row_height = 0

        layout.append({
            "name": room["name"],
            "x": x,
            "y": y,
            "width": width,
            "length": length
        })

        x += width + margin
        row_height = max(row_height, length)

    return layout
