import numpy as np
import matplotlib.pyplot as plt
def a_z(s_position, mic_positions, M, v, f0):

    result = []
    #print("start")
    for microphone in mic_positions:
        #print(f"mic_position inside a_z: {microphone}")
        #print(f"s_position inside a_z: {s_position}")
        rm = np.linalg.norm(s_position - microphone)
        tm = rm/v
        result.append( ((1/rm) * np.exp(-1j * 2*np.pi*f0 * tm) ) )
        #print(f"rm inside a_z: {rm}")
   
    result = np.array(result)
    
    return result
    


def music_z(Rx, Q, M, xyz_points, v, f0, mic_positions):
    
    eigenvals, eigenvecs = np.linalg.eigh(Rx)
    noises = M - Q
    Un = eigenvecs[:, :noises]

    result = np.zeros(shape = xyz_points.shape[:2])
    for i, row in enumerate(xyz_points):
        for j, cell in enumerate(row):

            a = a_z(cell, mic_positions, M, v, f0)

            to_append = np.matmul(a.conj().T, Un)
            to_append = np.matmul(to_append, Un.conj().T)
            to_append = np.matmul(to_append, a)
            result[i, j] = 20*np.log10(np.abs(1/to_append))


    return result


def mvdr_z(Rx, M, xyz_points, v, f0, mic_positions):
    
    result = np.zeros(shape = xyz_points.shape[:2])
    for i, row in enumerate(xyz_points):
        for j, cell in enumerate(row):

            a = a_z(cell, mic_positions, M, v, f0)

            to_append = np.matmul(a.conj().T, np.linalg.inv(Rx))
            to_append = np.matmul(to_append, a)
            result[i, j] = 20*np.log10(np.abs(1/to_append))

    return result

def generate_scan_points(xRange, yRange, zoff, resolution):
    
    result = [[(x, y ,zoff) for x in np.arange(min(xRange), max(xRange), resolution)] for y in np.arange(min(yRange), max(yRange), resolution)]

    return np.array(result)

def test_shit ():
    return 0

def generate_mic_positions(d = 0, M = 0):
    #mic_positions = np.array( [ [d * step , 0, 0] for step in range (M) ])
    #middle_point = mic_positions[len(mic_positions) - 1]/2
    #result = np.array([(mic_positions[i] - middle_point) for i in range (len(mic_positions))])
    #return result

    mic_locs_data = [
    [-0.025, 0.05, 0],  # 0
    [ 0.025, 0.05, 0],  # 1
    [-0.025, 0,    0],  # 2
    [ 0.025, 0,    0],  # 3
    [-0.025, -0.05, 0], # 4
    [ 0.025, -0.05, 0]  # 5
    ]

    # Convert to a NumPy array
    mic_array = np.array(mic_locs_data)
    return mic_array

if __name__ == "__main__":
    pass
