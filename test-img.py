from app.img_gen import CardGenerator
import os
from pathlib import Path

#c = CardGenerator()
#c.set_id('85653').set_first_name('Palo').create_image()

current_dir = os.path.dirname(__file__)
person_images_path = os.path.join(current_dir, 'app', 'cards_images', 'upload')
files = [file for file in Path(person_images_path).glob('*.jpg') if os.path.basename(file.with_suffix('')) == 'default']
print(files[0].with_suffix(''))