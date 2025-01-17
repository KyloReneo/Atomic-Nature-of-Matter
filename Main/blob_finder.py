import os
import sys
from blob import Blob
from Libs import Stdarray
from Libs import Luminance
from Libs.Picture import Picture


class BlobFinder:
    """
    A data type for identifying blobs in a picture.
    """

    def __init__(self, pic, tau):
        """
        Constructs a blob finder to find blobs in the picture pic, using
        a luminance threshold tau.
        """

        # Initialize an empty list for the blobs in pic.
        self._blobs = []

        # Create a 2D list of booleans called marked, having the same
        # dimensions as pic.
        marked = Stdarray.create2D(pic.width(), pic.height(), False)

        # Enumerate the pixels of pic, and for each pixel (i, j):
        # 1. Create a Blob object called blob.
        # 2. Call _findBlob() with the right arguments.
        # 3. Add blob to _blobs if it has a non-zero mass.
        for i in range(pic.width()):
            for j in range(pic.height()):
                blob = Blob()
                self._findBlob(pic, tau, i, j, marked, blob)
                if blob.mass() > 0:
                    self._blobs += [blob]

    def _findBlob(self, pic, tau, i, j, marked, blob):
        """
        Identifies a blob using depth-first search. The parameters are
        the picture (pic), luminance threshold (tau), pixel column (i),
        pixel row (j), 2D boolean matrix (marked), and the blob being
        identified (blob).
        """

        # Base case: return if pixel (i, j) is out of bounds, or if it
        # is marked, or if its luminance is less than tau.
        if i >= pic.width() or j >= pic.height() or i < 0 or j < 0 \
           or marked[i][j] is True or Luminance.luminance(pic.get(i, j)) < tau:
            return

        # Mark the pixel.
        marked[i][j] = True

        # Add the pixel to blob.
        blob.add(i, j)

        # Recursively call _findBlob() on the N, E, W, S pixels.
        self._findBlob(pic, tau, i - 1, j, marked, blob)
        self._findBlob(pic, tau, i + 1, j, marked, blob)
        self._findBlob(pic, tau, i, j + 1, marked, blob)
        self._findBlob(pic, tau, i, j - 1, marked, blob)

    def getBeads(self, P):
        """
        Returns a list of all beads with >= P pixels.
        """

        Blob = []
        for i in self._blobs:
            if i.mass() >= P:
                Blob += [i]
        return Blob

def writeFile(sth, location):
    open(str(location), "w").write("\n".join(str(i) for i in sth))

def check_file_existence(path):
    if os.path.exists(path):
        os.remove("blob_finder_results.txt")


# Takes an integer P, a float tau, and the name of a JPEG file as
# command-line arguments; writes out all of the beads with at least P
# pixels; and then writes out all of the blobs (beads with at least 1 pixel).
def _main():
    P = int(sys.argv[1])
    tau = float(sys.argv[2])
    frames = int(sys.argv[3])
    check_file_existence("./blob_finder_results.txt")
    resfile = open("blob_finder_results.txt", "a+")
    for k in range(frames):
        if k < 10 :
            frame = "frame0000" + str(k) + ".jpg"
        elif 10 <= k < 100 :
            frame = "frame000"  + str(k) + ".jpg"
        elif 100 <= k <1000 :
            frame = "frame00"   + str(k) + "jpg"
        address = "../Datasets/Frames/" + frame
        pic = Picture(address)
        b = BlobFinder(pic, tau)
        blobs = b.getBeads(P)
        resfile.write(frame[:10] + '\n')
        for j in blobs:
            resfile.write(str(j) + '\n')
        
        

if __name__ == '__main__':
    _main()