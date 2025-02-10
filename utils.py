from PIL import Image, ImageDraw, ImageFont


def center_text(text, font, font_size):
    image = Image.new("RGB", (800, 400), "white")
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(font, font_size)
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (800 - text_width) // 2
    y = (400 - text_height) // 2
    return (x, y)
