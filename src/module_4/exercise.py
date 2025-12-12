import numpy as np
import matplotlib.pyplot as plt

def a_lin(theta, M, d, v, f0):
    """Returns the *array response* or *steering vector* for a Uniform Linear Microphone Array

    Args:
        theta (float): angle of arrival
        M (int): number of microphones
        d (float): distance between microphones (m)
        v (float): speed of sound (m/s)
        f0 (float): frequency of wave (Hz)

    Returns:
        np.ndarray: The array response
    """  
    """okay"""
    result = np.array([ np.exp(
        (0 -1*mic*(d/v)*np.sin(theta*np.pi/180)*2*np.pi*f0 *1j)
        ) 
                       for mic in range (M)])

    return result

def generate_source(N):
    
    s_real = np.random.randn(N)
    s_imag = np.random.randn(N)
    
    s = s_real + 1j * s_imag
    
    # Power is defined as E[|s|^2], estimated by mean(|s|^2)
    current_power = np.mean(np.abs(s)**2)
    s_normalized = s / np.sqrt(current_power)
    
    return s_normalized

def datamodel (M, N, theta_range, d, v, f0):
    
    
    #create the A matrix (M x Q) of the steering vectors a(θ)
    A = np.array([a_lin(theta_range[i], M, d, v, f0)     for i in range (len(theta_range))] )
    A = np.transpose(A)

    #create the S matrix (Q x N) of the incoming signals of all sources
    S = np.array([generate_source(N) for i in range (len(theta_range))])

    #print(A.shape)
    #print(S.shape)

    #X = AS
    X = np.matmul(A,S)
    return X

def test_SVD():
    #define parameters
    M = 13   
    theta_range = [10, 90, 60]
    Q = len(theta_range)
    N = 10
    d = 0.1  
    v = 343  
    f0 = 250

    #construct a random X which doesnt have noise
    X = datamodel(M, N, theta_range, d, v, f0)

    #the rank gives the number of sources which is the length of theta_range
    rankx = np.linalg.matrix_rank(X)

    #the number of not zero (really small in reallity) eigenvalues
    #gives the number of sources too
    U, S, Vh = np.linalg.svd(X)
    V = Vh.conj().T
    print(rankx)
    print(S)

    x = np.array([i + 1 for i in range(len(S))])

    
    plt.figure(figsize=(8, 5))

    markerline, stemlines, baseline = plt.stem(x, S )

    
    plt.setp(markerline, marker='o', markersize=6)
    plt.setp(stemlines, linewidth=1.5)
    plt.setp(baseline, linewidth=1)

    plt.xlabel("Singular value index", fontsize=12)
    plt.ylabel(r"Singular value $\sigma_i$", fontsize=12)

    angles_str = ", ".join(str(a) for a in theta_range)
    plt.title(
        fr"Singular values of $X$  (angles: [{angles_str}], rank = {rankx})",
        fontsize=13
    )

    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    test_SVD()