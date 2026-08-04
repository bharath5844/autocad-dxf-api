def generate_layout(plot_width, plot_height, rooms):
    """
    Generates room positions on the plot.
    Returns:
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
    y = plot_height - 500

    margin = 300
    row_height = 0

    for room in rooms:

        width = int(room.get("widthMm", 3000))
        length = int(room.get("lengthMm", 3000))

        if x + width > plot_width - 500:
            x = 500
            y -= row_height + margin
            row_height = 0

        layout.append({
            "name": room.get("name", "Room"),
            "x": x,
            "y": y,
            "width": width,
            "length": length
        })

        x += width + margin
        row_height = max(row_height, length)

    return layout
