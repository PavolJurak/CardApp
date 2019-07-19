import os
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw

class CardGenerator():
    FIRST_NAME = 0
    LAST_NAME = 1
    PROGRAM = 2
    ID = 3

    background = None
    image = None
    default_background = 'default.jpg'
    default_person = 'default.jpg'

    id = 'NO SET'
    first_name = 'NO SET'
    last_name = 'NO SET'
    study_field = 'NO SET'

    current_dir = os.path.dirname(__file__)
    path_person_image = os.path.join(current_dir, 'cards_images', 'person-image')
    path_background_image = os.path.join(current_dir, 'cards_images', 'background')
    path_store_image = os.path.join(current_dir, 'static', 'images')
    font_path = "/usr/share/fonts/truetype/freefont/FreeSerif.ttf"

    def __init__(self):
        self.set_background(self.default_background)
        self.set_person_image(self.default_person)

    def set_background(self, background):
        if os.path.isfile(os.path.join(self.path_background_image, background)):
            self.background = os.path.join(self.path_background_image, background)
            print(self.background)
        else:
            self.background = os.path.join(self.path_background_image, self.default_background)
            print(self.background)
        return self

    def set_person_image(self, person):
        if os.path.isfile(os.path.join(self.path_person_image, person)):
            self.person = os.path.join(self.path_person_image, person)
        else:
            self.person = os.path.join(self.path_person_image, self.default_person)
        return self

    def set_id(self, id):
        self.id = id
        return self

    def set_first_name(self, first_name):
        self.first_name = first_name
        return self

    def set_last_name(self, last_name):
        self.last_name = last_name
        return self

    def set_study_field(self, study_field):
        self.study_field = study_field
        return self

    def create_image(self):
        background = Image.open(self.background)
        person = Image.open(self.person).resize((649, 803), Image.ANTIALIAS)

        # Nastavenie fontov
        font = ImageFont.truetype(self.font_path, 80)
        fontName = ImageFont.truetype(self.font_path, 90)
        fontIdDescription = ImageFont.truetype(self.font_path, 70)
        fontId = ImageFont.truetype(self.font_path, 75)

        # PAST PERSON IMAGE TO BACKGROUND
        background.paste(person, (344, 320))

        # Vlozenie popisneho textu do backgroundu
        draw = ImageDraw.Draw(background)
        draw.text((1050, 400), "Meno", (0, 0, 0), font=font)
        draw.text((1050, 700), "Odbor", (0, 0, 0), font=font)
        draw.text((400, 1200), "Identifikačné číslo:", (0, 0, 0), font=fontIdDescription)

        #Vlozenie id value
        draw.text((950, 1200), self.id, (0, 0, 0), font=fontId)

        #Vlozenie mena a priezviska value do obrazku
        draw.text((1050, 525), self.first_name + " " + self.last_name, (0, 0, 0), font=fontName)

        #Vlozenie odboru value
        if (self.study_field in "Laboratórne vyšetrovacie metódy v zdravotníctve"):
            draw.text((1050, 825), "Laboratórne vyšetrovacie", (0, 0, 0), font=fontName)
            draw.text((1050, 925), "metódy v zdravotníctve", (0, 0, 0), font=fontName)
        else:
            draw.text((1050, 825), self.study_field, (0, 0, 0), font=fontName)

        #SAVE NEW IMAGE
        new_image_name = str(int(datetime.timestamp(datetime.now())))
        background.save(self.path_store_image + "/" + new_image_name + ".jpg")

        return new_image_name
