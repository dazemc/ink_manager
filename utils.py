from PIL import Image, ImageDraw, ImageFont


def center_text(text, font, font_size: int):
    try:
        image_font = ImageFont.truetype(font, font_size)
    except OSError:
        image_font = ImageFont.load_default()
    boundaries = get_boundaries(text, image_font)
    if boundaries[0] > 720:
        text = resize_text(text, image_font)
        boundaries = get_boundaries(text, image_font)
    x = (800 - boundaries[0]) // 2
    y = (480 - boundaries[1]) // 2
    return ((x, y), text.splitlines(), boundaries[1] // 2)


def get_boundaries(text, image_font):
    image = Image.new("RGB", (800, 480), "white")
    draw = ImageDraw.Draw(image)
    bbox = draw.textbbox((0, 0), text, font=image_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    return text_width, text_height


def resize_text(text, font):
    image = Image.new("RGB", (800, 480), "white")
    draw = ImageDraw.Draw(image)
    words = text.split()
    leftover_words = text.split()
    line = ""
    lines = []
    for word in words:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        if line_width > 720:
            lines.append(line + "\n")
            line = ""
        line += word + " "
        leftover_words.pop(0)
    for word in leftover_words:
        line += word + " "
    lines.append(line)
    quote = ""
    for line in lines:
        quote += line
    return quote


# text = "Duty makes us do things well, but love makes us do them beautifully."
# font = "./assets/fonts/Font.ttc"
# font_size = 36
# image = center_text(text, font, font_size)
# print(image)
