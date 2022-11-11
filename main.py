import os

import imagehash
import numpy
import scipy
from PIL import Image
from pathlib import Path
from typing import List

from AVLTree import AVLTree

"""
Path functions
"""


def getNotFoundImagePath():
    projectDir = os.path.dirname(os.path.realpath('__file__'))

    moduleName = "notFound"

    pathToFile = os.path.join(projectDir, moduleName)
    listOfAllImagePaths: List = []

    for path in Path(pathToFile).rglob('*.png'):
        listOfAllImagePaths.append(os.path.join(pathToFile, path))

    return listOfAllImagePaths


def getTestImagePaths():
    projectDir = os.path.dirname(os.path.realpath('__file__'))

    moduleName = "TestImages"

    pathToFile = os.path.join(projectDir, moduleName)
    listOfAllImagePaths: List = []

    for path in Path(pathToFile).rglob('*.jpg'):
        listOfAllImagePaths.append(os.path.join(pathToFile, path))

    return listOfAllImagePaths


def getImagePaths():
    projectDir = os.path.dirname(os.path.realpath('__file__'))

    moduleName = "Images"

    pathToFile = os.path.join(projectDir, moduleName)
    listOfAllImagePaths: List = []


    for path in Path(pathToFile).rglob('*.jpg'):
        listOfAllImagePaths.append(os.path.join(pathToFile, path))

    return listOfAllImagePaths


"""
real functions
"""


def hamming_distance(imagehash, imagehash2):
    score = scipy.spatial.distance.hamming(imagehash, imagehash2)
    return score


def get(image):
    imghash = imagehash.dhash(image)
    imagepaths = getImagePaths()
    for path in imagepaths:
        if imghash == imagehash.dhash(Image.open(path)):
            return Image.open(path)
    return Image.open(getNotFoundImagePath()[0])  # gibt image not found bild zurück


def getMostSimilar(image):
    imghash = imagehash.dhash(image)
    imagepaths = getImagePaths()
    for path in imagepaths:
        if hamming_distance(imghash.hash.flat, imagehash.dhash(Image.open(path)).hash.flat) < .10:
            return Image.open(path)
    return Image.open(getNotFoundImagePath()[0])  # gibt image not found bild zurück



"""
Testing
"""


def main():
    # print(getImagePaths()[0])

    """ Testen der Bilder in Testimage-Ordner zahl durch 0-4 ersetzbar erst wird das gesuchte Bild angezeigt und nach
    dem Drücken von enter das Ergebnis der Funktion (Bild aus Images-Ordner oder notFound)
    # zum Testen von funktion entfernen
    """

    # Hash Scores for all of the images
    imagepaths_test_images = getTestImagePaths()
    for path in imagepaths_test_images:
        print(path, imagehash.dhash(Image.open(path)))

    imagepaths_images = getImagePaths()
    for path in imagepaths_images:
        print(path, imagehash.dhash(Image.open(path)))

    zahl = 2
    # show chosen picture
    Image.open(getTestImagePaths()[zahl]).show()
    input("Press Enter to continue...")
    # find picture in Images
    #get(Image.open(getTestImagePaths()[zahl])).show()

    # find the most similar picture to the chosen one
    #getMostSimilar(Image.open(getTestImagePaths()[zahl])).show()


if __name__ == '__main__':
    main()
