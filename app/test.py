import os

if __name__ == '__main__':
    current_dir = os.path.dirname(__file__)
    path_store_image = os.path.join(current_dir, 'cards_images', 'store')
    print(path_store_image)