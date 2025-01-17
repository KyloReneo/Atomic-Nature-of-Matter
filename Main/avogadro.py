import math
from bead_tracker import bead_tracker as bt
from bead_tracker import create_frame_address as cfa

# Default values of inputs :
# Number of Pixels: 25
# Tau: 180.0
# Delta: 25.0
# Starting frame: frame00000
# Number next frames: 100

def main():
    
    print("Default value : 25")
    P                     = int(input("Number of Pixels: \n").strip() or "25")
    print("Default value : 180.0")
    tau                   = float(input("Tau: \n").strip() or "180.0")
    print("Default value : 25.0")
    delta                 = float(input("Delta: \n").strip() or "25.0")
    print("Default value : 0")
    frame_name            = int(input("Starting frame: \n").strip() or "0")
    first_frame = cfa(frame_name)
    print("Default value : 100")
    number_of_next_frames = int(input("Number next frames: \n").strip() or "100")
    
    try:
        res = bt(P, tau, delta, first_frame, number_of_next_frames)
        print("Bead Tracker's job is done.")
    except:
        print("Tracking beads went wrong!")
        
    n = 0
    D = 0.00
    for r in res :
        temp = r * (0.175 * (10 ** -6)) #For converting pixel to meter
        D += temp * temp
        n += 1
        print(temp)

    D = D / (2 * n)
    eta = 9.135 * (10 ** -4)
    rho = 0.5 * (10 ** -6)
    T = 297.0
    R = 8.31457
    k = 6 * math.pi * D * eta * rho / T
    N_A = R / k
    print('Boltzman Constant = {} \nAvogadro Number = {} \n'.format(k, N_A))

if __name__ == '__main__':
    main()
