import cv2
import imutils
import numpy as np

class PlateReader:

    def __init__(self, image: str):
        self.image = self._get_image(image)

    def detect_plate_corners(self):
        # Convert image to grey scale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)  # convert to grey scale

        # Remove useless information (noise) from the image using cv2.bilateralFilter
        gray = cv2.bilateralFilter(gray, 11, 17, 17)

        # Get object edges using canny edge method (the most popular and easy)
        edged = cv2.Canny(gray, 30, 200)

        # Get all the contours of the object in the image, we make a copy of the image because the cv2.findContours
        # function will alter the image
        nts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Return the actual contours array using 'imutils' module.
        # (cv2.findContours return tuples changes from the version)
        contours = imutils.grab_contours(nts)

        # Return a new list containing all items from the iterable in ascending order.
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        plate_points = []

        # loop over our contours to get the plate points
        for c in contours:
            # Approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)

            # if our approximated contour has four points, then
            # we can assume that we have found the plate. We check if
            # it has 4 points because a vehicle plate has 4 corners (is a rectangle).
            if len(approx) == 4:
                plate_points = approx
                break

        return plate_points

    def get_plate(self, plate_points, crop=True):
        img = self.image.copy()

        # Convert image to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if crop:
            # Masking the part other than the number plate
            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(img, [plate_points], 0, 255, -1)
            new_image = cv2.bitwise_and(img, img, mask=mask)

            # Crop image
            (x, y) = np.where(mask == 255)
            (top_x, top_y) = (np.min(x), np.min(y))
            (bottom_x, bottom_y) = (np.max(x), np.max(y))
            cropped_img = gray[top_x:bottom_x + 1, top_y:bottom_y + 1]

            return cropped_img
        else:
            # Draw contours on image
            new_image = cv2.drawContours(img, [plate_points], 0, 255, 5, )
            return new_image

    @staticmethod
    def show_img(img, title="Image"):
        cv2.imshow(title, img)
        cv2.waitKey()

    @staticmethod
    def _get_image(path):
        """
        This method is used to read an image using OpenCV
        :param path: Path of the image that will be read by OpenCV
        :return: Image object
        """
        return cv2.imread(path)
