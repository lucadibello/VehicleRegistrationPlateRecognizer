import cv2
import imutils

class PlateReader:

    def __init__(self, image: str):
        self.image = self._get_image(image)

    def get_plate(self):
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

        # loop over our contours
        for c in contours:
            # Approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)

            # if our approximated contour has four points, then
            # we can assume that we have found the plate. We check if
            # it has 4 points because a vehicle plate has 4 corners (is a rectangle).
            if len(approx) == 4:
                screenCnt = approx
                break

    @staticmethod
    def _get_image(path):
        """
        This method is used to read an image using OpenCV
        :param path: Path of the image that will be read by OpenCV
        :return: Image object
        """
        return cv2.imread(path)
