import cv2

class PlateReader:

    def __init__(self, image):
        self.image = image

    def get_plate(self):
        print("WIP: {}".format(self.image))

    @staticmethod
    def get_image(path):
        """
        This method is used to read an image using OpenCV
        :param path: Path of the image that will be read by OpenCV
        :return: Image object
        """
        return cv2.imread(path)
