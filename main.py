import os

import imagehash
import numpy
import scipy
import self as self
from PIL import Image
from pathlib import Path
from typing import List
from PIL import Image
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
global variables
"""
imagepaths_test_images = getTestImagePaths()

imagepaths = getImagePaths()

# Erstmal eine unschöne Lösung, weil "imageHashSet" und "imagepathsHashDict" nicht geupdated werden,
# falls die Inhalte vom "Images" oder "TestImages" Ordner verändert werden.
# Aber es ermöglicht, dass get O(1) ist
#
# Ermöglicht es zu prüfen, ob ein Hash im "Images" Ordner enthalten ist ohne zu iterieren
imageHashSet = set()
# Ermöglicht mit einem Hash nach dem Image Path zu suchen ohne zu iterieren
imagepathsHashDict = {}


def fill_set():
    for path in imagepaths:
        imageHashSet.add(imagehash.dhash(Image.open(path)))


def fill_dictionary():
    for path in imagepaths:
        imagepathsHashDict[imagehash.dhash(Image.open(path))] = path


"""
real functions
"""


def get_image_hash(image):
    return imagehash.dhash(image)


def hamming_distance(imagehash, imagehash2):
    score = scipy.spatial.distance.hamming(imagehash, imagehash2)
    return score


def get(image):
    imghash = get_image_hash(image)
    if imghash in imageHashSet:
        return Image.open(imagepathsHashDict[imghash])
    return Image.open(getNotFoundImagePath()[0])


# diese Funktion müssen wir nicht implementieren für DHash
def getMostSimilar(image):
    imghash = get_image_hash(image)
    for path in imagepaths:
        if hamming_distance(imghash.hash.flat, get_image_hash(Image.open(path)).hash.flat) < .10:
            return Image.open(path)
    return Image.open(getNotFoundImagePath()[0])  # gibt image not found bild zurück


def create_tree():
    tree = AVLTree()
    for path in imagepaths:
        if (tree.find(str(get_image_hash(Image.open(path)))) != None):
            tree.updateNode(tree.find(str(get_image_hash(Image.open(path)))), path)
        tree.insert(str(get_image_hash(Image.open(path))), path)
    return tree


def get_image_avl(image, tree):
    imghash = get_image_hash(image)
    if tree.search(str(imghash)):
        return Image.open(imagepathsHashDict[imghash]) # image durch dict ersetzen
    else:
        return Image.open(getNotFoundImagePath()[0])


def get_most_similar_avl(image, tree):
    imghash = get_image_hash(image)
    if tree.search(str(imghash)):
        raise Exception("This image is already in the dataset and cannot be used as similar image")
    return Image.open(_get_most_similar_avl(imghash, tree.root, tree.root.pBucket[0]))


def _get_most_similar_avl(imghash, node, most_similar_path):
    # Basisfall
    if node.left_child is None and node.right_child is None:
        return most_similar_path
    hamming_most_similar_node = hamming_distance(imghash.hash.flat,
                                                 get_image_hash(Image.open(most_similar_path)).hash.flat)
    hash_most_similar = str(get_image_hash(Image.open(most_similar_path)))

    if node.left_child is not None:
        hash_left = str(get_image_hash(Image.open(node.left_child.pBucket[0])))
        hamming_left = hamming_distance(imghash.hash.flat,
                                        get_image_hash(Image.open(node.left_child.pBucket[0])).hash.flat)
    else:
        hash_left = float("inf")
        hamming_left = float("inf")

    if node.right_child is not None:
        hash_right = str(get_image_hash(Image.open(node.right_child.pBucket[0])))
        hamming_right = hamming_distance(imghash.hash.flat,
                                         get_image_hash(Image.open(node.right_child.pBucket[0])).hash.flat)
    else:
        hash_right = float("inf")
        hamming_right = float("inf")
    # entscheiden ob wir nach links oder nach rechts gehen sollen
    if str(hash_right) < str(hash_left):
        if hamming_right < hamming_most_similar_node:
            most_similar_path = node.right_child.pBucket[0]
        return _get_most_similar_avl(imghash, node.right_child, most_similar_path)
    else:
        if hamming_left < hamming_most_similar_node:
            most_similar_path = node.left_child.pBucket[0]
        return _get_most_similar_avl(imghash, node.left_child, most_similar_path)


"""
Testing
"""


def main():
    """ Testen der Bilder in Testimage-Ordner zahl durch 0-4 ersetzbar erst wird das gesuchte Bild angezeigt und nach
    dem Drücken von enter das Ergebnis der Funktion (Bild aus Images-Ordner oder notFound)
    # zum Testen von funktion entfernen
    """

    # Hash Scores for all of the images
    for path in imagepaths_test_images:
        print(path, imagehash.dhash(Image.open(path)))

    for path in imagepaths:
        print(path, imagehash.dhash(Image.open(path)))
    fill_set()
    fill_dictionary()

    ################ DHash Hund Nr.13 ##########
    zahl = 1
    # show chosen picture
    Image.open(imagepaths_test_images[zahl]).show()
    # input("Press Enter to continue...")
    # find picture in Images
    get(Image.open(imagepaths_test_images[zahl])).show()

    # AVL Baum
    tree = create_tree()
    tree.print_tree()

    ############## AVL orange cat ##############
    zahl =1
    Image.open(getTestImagePaths()[zahl]).show()
    get_image_avl(Image.open(getTestImagePaths()[zahl]), tree).show()
    get_most_similar_avl(Image.open(getTestImagePaths()[zahl]), tree).show()

    ############## AVL 13:hund ##############
    zahl = 1
    Image.open(getTestImagePaths()[zahl]).show()
    get_image_avl(Image.open(getTestImagePaths()[zahl]), tree).show()
    get_most_similar_avl(Image.open(getTestImagePaths()[zahl]), tree).show()


    # does changing the foto changes the hash score?
    # rotating -> changes the hash
    """
    zahl = 1
    image_to_change = getTestImagePaths()[zahl]
    Image.open(image_to_change).show()
    print("Image Hash of the image to be rotated: ", imagehash.dhash(Image.open(image_to_change)))
    rotated_image = Image.open(getTestImagePaths()[zahl]).rotate(180)
    rotated_image.show()
    print("Image Hash of the rotated: ", imagehash.dhash(rotated_image))
    """
if __name__ == '__main__':
    main()
