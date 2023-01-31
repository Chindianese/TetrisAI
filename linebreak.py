import sys
import numpy as np

def fix_line_break(fileName):
    np.set_printoptions(threshold=sys.maxsize)

    with open(fileName) as f:
        contents = f.read()
        # print(contents)
        replaced = contents.replace("\n", "")
        replaced = replaced.replace("]", "]\n")
        replaced = replaced.replace("255", "1")
        replaced = replaced.replace("0", ".")
        replaced = replaced.replace(" ", "")
        file = open(fileName, "w+")
        # Saving the array in a text file
        file.write(replaced)
        file.close()