from PIL import Image, ImageDraw, ImageFont
from models import TextBoundary, TextBoundaryLine, Coord


def center_text(text: str, font: str, font_size: int) -> TextBoundary:
    try:
        image_font = ImageFont.truetype(font, font_size)
    except OSError:
        image_font = ImageFont.load_default()
    boundaries = get_boundaries(text, image_font)
    if boundaries[0] > 740:
        text = resize_text(text, image_font, 740)
        boundaries = get_boundaries(text, image_font)
    if boundaries[1] > 480:
        # TODO: Dynamically resize text to fit
        print("Warning, text boundaries may exceed the limits")
    x = int((800 - boundaries[0]) // 2)
    y = int((480 - boundaries[1]) // 2)

    text_lines: list[TextBoundaryLine] = []
    max_line_height = 0
    for line in text.splitlines():
        boundaries = get_boundaries(line, image_font)
        if int(boundaries[1]) > max_line_height:
            max_line_height = int(boundaries[1])
        text_lines.append(
            TextBoundaryLine(
                center_x=int((800 - boundaries[0]) // 2),
                boundary_x=int(boundaries[0]),
                boundary_y=int(boundaries[1]),
                text=line,
            )
        )

    return TextBoundary(
        origin_coord=Coord(x=x, y=y),
        text_lines=text_lines,
        boundary_x=int(boundaries[0]),
        boundary_y=int(boundaries[1]),
        max_line_height=max_line_height,
    )


def get_boundaries(text, image_font):
    image = Image.new("RGB", (800, 480), "white")
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=image_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    return text_width, text_height


def resize_text(text, font, max_width):
    words = text.split()
    if not words:
        return ""
    lines = []
    current_line = words[0]
    for word in words[1:]:
        test_line = current_line + " " + word
        test_line_width, _ = get_boundaries(test_line, font)
        if test_line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return "\n".join(lines)


# text = "Duty makes us do things well, but love makes us do them beautifully."
# font = "./assets/fonts/Steelworks.ttf"
# font_size = 72
# image = center_text(text, font, font_size)
# print(image)
