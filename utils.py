from PIL import Image, ImageDraw, ImageFont


def center_text(text, font, font_size):
    image = Image.new("RGB", (800, 480), "white")
    draw = ImageDraw.Draw(image)
    try:
        image_font = ImageFont.truetype(font, font_size)
    except OSError:
        image_font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=image_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    if text_width > 760:
        return resize_text(text, font, font_size)  # recursively resize
    x = (800 - text_width) // 2
    y = (480 - text_height) // 2
    text = text.splitlines()
    return ((x, y), text, text_height // 2)


def resize_text(text, font, font_size):
    final_text = ""
    text = text.splitlines()
    for line in text:
        split_idx = split_text(line)
        final_text += f"{line[:split_idx]}\n{line[split_idx + 1 :]}"
    return center_text(final_text, font, font_size)


def split_text(text):
    split_idx = len(text) // 2
    split = text[split_idx]
    if split != " ":
        split_idx = text[:split_idx].rfind(" ")
    return split_idx
