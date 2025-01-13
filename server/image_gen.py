from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
from io import BytesIO
from typing import List, Dict
from textwrap import fill as wrapfill

class Resolution:
    def __init__(self, width: int, height: int, scaling: int):
        self.width = width
        self.height = height
        self.scaling = scaling

    @property
    def dimensions(self):
        return self.width, self.height

resolution_list = [
    Resolution(1280, 720, 1),
    Resolution(1920, 1080, 2), 
    Resolution(2560, 1440, 3),
]

font_path = "static/fonts/ShadowsIntoLight-Regular.ttf"
image_dir = "static/images/"

def generate_image(character, quote, resolution=1):
    selected_resolution = resolution_list[resolution]

    quote_image = Image.new("RGB", selected_resolution.dimensions)

    center_point = (selected_resolution.width / 2, selected_resolution.height / 2)

    char_image_path = os.path.join(image_dir, character["img"])
    char_img = Image.open(char_image_path)

    if char_img.size[0] > 1920 or char_img.size[1] > 1080:  # make character 1080p reso or less
        char_img.thumbnail((selected_resolution.width, selected_resolution.height))
    else:
        char_img = char_img.resize((char_img.width * selected_resolution.scaling, char_img.height * selected_resolution.scaling))

    quote_image.paste(ImageOps.grayscale(char_img), (0, selected_resolution.height - char_img.height))

    font_size = 32 * selected_resolution.scaling
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(quote_image)

    wrapped_quote = wrapfill(quote, 35)

    quote_position = (center_point[0] - 200, center_point[1] - (100 * selected_resolution.scaling))
    draw.text(quote_position, wrapped_quote, font=font, fill="white")

    name_text = f"- {character['name']}"

    name_position = (quote_position[0], quote_position[1] + (200 * selected_resolution.scaling))
    draw.text(name_position, name_text, font=font, fill="white")

    img_io = BytesIO()
    quote_image.save(img_io, "PNG")
    img_io.seek(0)
    
    return img_io
