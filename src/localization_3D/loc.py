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

    result = []
    for candidate_source_location in xyz_points:
        
        a = a_z(candidate_source_location, mic_positions, M, v, f0)

        to_append = np.matmul(a.conj().T, Un)
        to_append = np.matmul(to_append, Un.conj().T)
        to_append = np.matmul(to_append, a)
        result.append(1/to_append)

    result = np.array(result)

    return result


def mvdr_z(Rx, M, xyz_points, v, f0, mic_positions):
    
    
    result = []
    for candidate_source_location in xyz_points:
        a = a_z(candidate_source_location, mic_positions, M, v, f0).reshape(M,1)

        to_append = np.matmul(a.conj().T, np.linalg.inv(Rx))
        to_append = np.matmul(to_append, a)
        result.append(1/to_append)
    result = np.array(result)

    return result

def generate_scan_points(radius, zoff):
    
    result = np.array([
    [radius * np.sin(np.deg2rad(angle)),
     radius * np.cos(np.deg2rad(angle)),
     zoff]
    for angle in range(-90,90)
    ])

    return result

def test_shit ():
    return 0

def generate_mic_positions(d, M):
    mic_positions = np.array( [ [d * step , 0, 0] for step in range (M) ])
    middle_point = mic_positions[len(mic_positions) - 1]/2
    result = np.array([(mic_positions[i] - middle_point) for i in range (len(mic_positions))])
    return result

if __name__ == "__main__":
    pass
