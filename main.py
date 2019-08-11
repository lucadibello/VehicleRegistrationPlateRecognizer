import argparse
import os

from modules import *

# OCR engine path
TESSERACT_PATH = r'D:\tesseract-ocr-engine\Tesseract'
TESSRACT_TRAINED_DATA = r'D:\tesseract-ocr-engine\tessdata'

def main():
    # Argument add parser
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('image', type=str)

    # '--crop' flag
    parser.add_argument(
        '--crop',
        action='store_true',
        help="the image will be cropped, only the vehicle plate will be in the image"
    )

    # '--show' flag
    parser.add_argument(
        '--show',
        action='store_true',
        help="show the results in a small window"
    )

    args = parser.parse_args()

    if os.path.exists(args.image):
        # ImageReader object, used to read the vehicle plate numbers
        reader = ImageReader(TESSERACT_PATH, TESSRACT_TRAINED_DATA)

        # PlateReader object, used to get only the plate as an image
        plate_scanner = PlateRecognizer(str(args.image))
        plate = plate_scanner.get_plate(plate_scanner.detect_plate_corners(), args.crop)

        if args.crop:
            print("Plate number: {}".format(reader.read(plate)))
        else:
            print("[!] Image not cropped, I can't read the number!")

        if args.show:
            plate_scanner.show_img(plate)
    else:
        print("[!] The image does NOT exists!")


if __name__ == '__main__':
    main()
