import cv2
import numpy as np


def LocateTemplate(imagePath, tempPath, conf, multiple, yOff=0):
    """
    Locates within an image the template provided.
    Will locate as many of that template that it finds - unless multiple is set to false

    :param imagePath: string or numpy image for the file path of the image
    :param tempPath: string for the file path of the template
    :param conf: float giving the confidence 1.0 means perfect match 0.0 means anything
    :param multiple: boolean True if many results, false if first result
    :param yOff: int moving the y value; + value is down, - value is up
    :return: A list of tuples or a tuple, the templates width and height
    """
    # check if provided image is a path or not
    if isinstance(imagePath, str):
        img_rgb = cv2.imread(imagePath)
    else:
        img_rgb = imagePath

    # Convert it to grayscale
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    # Read the template
    template = cv2.imread(tempPath, 0)

    # Store width and height of template in w and h
    w, h = template.shape[::-1]

    # Perform match operations.
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    # Specify a threshold
    threshold = conf

    # Store the coordinates of matched area in a numpy array
    loc = np.where(res >= threshold)
    location = []
    # Draw a rectangle around the matched region.
    for pt in zip(*loc[::-1]):
        if multiple:
            if len(location) > 0:
                # loop to ensure only one entry is added for close by positives
                for j in location:
                    # good case
                    if abs(pt[0] - j[0]) <= 5 and abs(pt[1] - j[1] <= 5):
                        passed = False
                        break
                    # good case
                    else:
                        passed = True
                if passed:
                    location.append((pt[0], pt[1] + yOff))
            else:
                location.append((pt[0], pt[1] + yOff))
        else:
            location = (pt[0], pt[1] + yOff)

    return location, w, h


def DrawImages(imagePath, pointsArray, xOff=0, yOff=0):
    """
    Draws a Circle on the image provided at the points provided.

    :param pointsArray: List contain the points that are to be drawn
    :param xOff: x offset of the template
    :param yOff: y offset of the template
    :param imagePath: string for the image location
    :return: the resized image with the circles drawn
    """
    if isinstance(imagePath, str):
        img_rgb = cv2.imread(imagePath)

        for points in pointsArray:
            x = int(points[0] + (xOff / 2))
            y = int(points[1] + (yOff / 2))

            cv2.circle(img_rgb, (x, y), 5, (0, 0, 255), 4)

        return img_rgb

    else:
        for points in pointsArray:
            x = int(points[0] + (xOff / 2))
            y = int(points[1] + (yOff / 2))

            cv2.circle(imagePath, (x, y), 5, (0, 255, 0), 2)

        return imagePath

def DrawLines(image, pointA, points, colour=(0,0,255)):
    '''
    Draw a line between one point and one/many points

    :param image: OpenCv2 image
    :param pointA: starting point for the line
    :param points: points to be drawn to
    :return: a OpenCV2 image that has been drawn on
    '''

    thickness = 2

    for pt in points:
        if pt:
            cv2.line(image, pointA, pt, colour, thickness)

    return image


def DisplayImage(image, title='Display Image', xWindow=None, yWindow=None, wait=False):
    """
    Display the image in a new window
    Can be resized if given new window dimensions

    :param image: provided a cv2 image
    :param title: provide a string title
    :param xWindow: width of new window
    :param yWindow: height of new window
    """

    if not wait:
        if xWindow is not None:
            dim = (xWindow, yWindow)
            resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            cv2.imshow(title, resized)
            cv2.waitKey(1)
        else:
            cv2.imshow(title, image)
            cv2.waitKey(1)
    else:
        cv2.imshow(title, image)
        cv2.waitKey(0)

