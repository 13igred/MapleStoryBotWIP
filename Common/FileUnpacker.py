import os
import json
import cv2


def Unpack(folderName):
    """
    Given a folder name for the map, will unpack the contents

    :param folderName: a string with the name of the folder to open
    :return: a json data object, a image temple and the flipped template.
    """

    path = 'Resources/Maps/' + folderName

    j = open(path + '/details.json')
    data = json.load(j)
    im1 = cv2.imread(path + '/M.png')
    im2 = cv2.imread(path + '/MF.png')

    return data, im1, im2
