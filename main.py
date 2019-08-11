from modules import *

# OCR engine path
TESSERACT_PATH = r'D:\tesseract-ocr-engine\Tesseract'


def main():
    # ImageReader object, used to read the vehicle plate numbers
    reader = ImageReader(TESSERACT_PATH)

    # PlateReader object, used to get only the plate as an image
    plate_scanner = PlateReader("assets/mini_image.jpg")
    plate_scanner.get_plate()

if __name__ == '__main__':
    main()
