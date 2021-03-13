import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, ImageColor

TEMPLATE_PATH = 'files/ticket_base.png'
FONT_PATH = 'files/roboto-regular.ttf'
FONT_SIZE = 20

BLACK = (0, 0, 0, 255)
NAME_OFFSET = (300, 220)
EMAIL_OFFSET = (300, 260)
AVATAR_SIZE = 100
AVATAR_OFFSET = (100, 200)


def generate_ticket(dep_city, dest_city, flight, fio):
    base = Image.open('files/ticket_template.png').convert('RGBA')
    font_path = os.path.join("files", "roboto-regular.ttf")
    font = ImageFont.truetype(font_path, size=15)
    draw = ImageDraw.Draw(base)

    draw.text((47, 126), fio.upper(), font=font, fill=ImageColor.colormap['black'])
    draw.text((45, 195), dep_city.upper(), font=font, fill=ImageColor.colormap['black'])
    draw.text((45, 261), dest_city.upper(), font=font, fill=ImageColor.colormap['black'])
    draw.text((286, 261), flight.upper(), font=font, fill=ImageColor.colormap['black'])

    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)

    return temp_file


if __name__ == '__main__':
    generate_ticket(dep_city='Лондон', dest_city='Москва', flight='24-05-2020', fio='someone')
