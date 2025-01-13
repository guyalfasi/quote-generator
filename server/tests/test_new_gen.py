import json
from PIL import Image, ImageFont, ImageDraw, ImageOps
from textwrap import fill as wrapfill
import os

class Resolution:
    def __init__(self, width: int, height: int, scaling: int):
        self.width = width
        self.height = height
        self.scaling = scaling

    @property
    def dimensions(self):
        return self.width, self.height

resolution_list = [Resolution(1920, 1080, 2), Resolution(2560, 1440, 3)]

font_path = "static/fonts/ShadowsIntoLight-Regular.ttf"
image_dir = "static/images/"

with open('data/characters.json', 'r') as f:
    characters = json.load(f)

def new_image_gen(character, quote, resolution):
    quote_image = Image.new("RGB", resolution.dimensions)

    center_point = (resolution.width / 2, resolution.height / 2)

    char_image_path = os.path.join(image_dir, character["img"])
    char_img = Image.open(char_image_path)

    if char_img.size[0] > 1920 or char_img.size[1] > 1080:  # make character 1080p reso or less
        char_img.thumbnail((resolution.width, resolution.height))
    else:
        char_img = char_img.resize((char_img.width * resolution.scaling, char_img.height * resolution.scaling))

    quote_image.paste(ImageOps.grayscale(char_img), (0, resolution.height - char_img.height))

    font_size = 32 * resolution.scaling
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(quote_image)

    wrapped_quote = wrapfill(quote, 35)

    quote_position = (center_point[0] - 200, center_point[1] - (100 * resolution.scaling))
    draw.text(quote_position, wrapped_quote, font=font, fill="white")

    name_text = f"- {character['name']}"

    name_position = (quote_position[0], quote_position[1] + (200 * resolution.scaling))
    draw.text(name_position, name_text, font=font, fill="white")

    quote_image.show()

if __name__ == "__main__":
    new_image_gen(next((c for c in characters if c['name'] == 'Peter Griffin'), None), "hey", resolution_list[0])
