import os
import Imagehash
from pathlib import Path
from typing import List

def getImagePaths():
    projectDir = os.path.dirname(os.path.realpath('__file__'))

    moduleName = "Images"

    pathToFile= os.path.join(projectDir, moduleName)
    listOfAllImagePaths : List = []

    for path in Path(pathToFile).rglob('*.jpg'):
     listOfAllImagePaths.append(os.path.join(pathToFile, path))

    return listOfAllImagePaths

def get(image):
    print(Imagehash.dhash(os.open(getImagePaths()[0])))
    return


def getMostSimilar(image):
    #todo
    return

def main():
    print(getImagePaths().__len__())
    # test


# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    main()

