import os
from blob_finder import BlobFinder
from Libs.Picture import Picture

def check_file_existence(path):
    if os.path.exists(path):
        os.remove("./bead_tracker_results.txt")
        
def where_to_start(path):
    s = path.split("/")[3]
    frame_name = s.split(".")[0]
    start_frame = int(frame_name[5:])
    return start_frame

def create_frame_address(n):
    if n < 10 :
        frame = "frame0000" + str(n) + ".jpg"
    elif 10 <= n < 100 :
        frame = "frame000"  + str(n) + ".jpg"
    elif 100 <= n <1000 :
        frame = "frame00"   + str(n) + "jpg"
    address = "../Datasets/Frames/"  + frame
    return address
        
def bead_tracker(P, tau, delta, first_frame, N):

    results = []
    start_frame = where_to_start(first_frame)
    bf = BlobFinder(Picture(first_frame), tau)
    prevBeads = bf.getBeads(P)
    check_file_existence("./bead_tracker_results.txt")
    resfile = open("./bead_tracker_results.txt", "a+")
    frames = int(N)
    
    for i in range(1, frames):
        next_frame_address = create_frame_address(i + start_frame)
        bf = BlobFinder(Picture(next_frame_address), tau)
        currBeads = bf.getBeads(P)
        for currBead in currBeads:
            min_dist = float('inf')
            for prevBead in prevBeads:
                d = currBead.distanceTo(prevBead)
                if d <= delta and d < min_dist:
                    min_dist = d
            if min_dist != float('inf'):
                resfile.write(str(min_dist) + '\n') 
                results.append(min_dist)
        resfile.write('\n')
        prevBeads = currBeads
    return results
