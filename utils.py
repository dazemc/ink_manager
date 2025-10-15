from PIL import Image, ImageDraw, ImageFont
from models import TextBoundary, TextBoundaryLine, Coord
from lib.ink_display import LOGGER


def get_font(font, font_size):
    image_font = None
    try:
        image_font = ImageFont.truetype(font, font_size)
    except OSError:
        image_font = ImageFont.load_default()
    return image_font


def get_max_line_height(lines, image_font):
    max_line_height = 0
    for line in lines:
        b = get_boundaries(line, image_font)
        line_height = b[1]
        if line_height > max_line_height:
            max_line_height = line_height
    return max_line_height


def center_text(text: str, font: str, font_size: int) -> TextBoundary:
    isConstrained = False
    while not isConstrained:
        image_font = get_font(font, font_size)
        text = split_text(text, image_font, 740)
        max_line_height = get_max_line_height(text.splitlines(), image_font)
        y_total = max_line_height * len(text.splitlines())
        bounds = get_boundaries(text, image_font)
        isXConstrained = False
        isYConstrained = False
        if y_total < 460:
            isYConstrained = True
        if bounds[0] < 740:
            isXConstrained = True
        if not isXConstrained or not isYConstrained:
            font_size -= 1
        if isXConstrained and isYConstrained:
            isConstrained = True
        LOGGER.info(
            f"Font size {font_size} → lines: {len(text.splitlines())}, width: {bounds[0]}, height: {y_total}, isXConstrained: {isXConstrained}, isYConstrained: {isYConstrained}"
        )

    image_font = get_font(font, font_size)
    boundaries = get_boundaries(text, image_font)
    x = int((800 - boundaries[0]) // 2)
    y = int((480 - boundaries[1]) // 2)

    text_lines: list[TextBoundaryLine] = []
    for line in text.splitlines():
        boundaries = get_boundaries(line, image_font)
        text_lines.append(
            TextBoundaryLine(
                center_x=int((800 - boundaries[0]) // 2),
                boundary_x=int(boundaries[0]),
                boundary_y=int(boundaries[1]),
                text=line,
            )
        )

    max_line_height = int(get_max_line_height(text.splitlines(), image_font))

    return TextBoundary(
        origin_coord=Coord(x=x, y=y),
        text_lines=text_lines,
        boundary_x=int(boundaries[0]),
        boundary_y=int(boundaries[1]),
        max_line_height=max_line_height,
        font_size=font_size,
    )


def get_boundaries(text, image_font):
    image = Image.new("RGB", (800, 480), "white")
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=image_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    return text_width, text_height


def split_text(text, font, max_width):
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
