import pytesseract



class ImageReader:
    def __init__(self, path, trained_set):
        pytesseract.pytesseract.tesseract_cmd = path
        self.tessdata_dir_config = r'--tessdata-dir "{}"'.format(trained_set)

    def read(self, image) -> str:
        return pytesseract.image_to_string(image, config=self.tessdata_dir_config)
