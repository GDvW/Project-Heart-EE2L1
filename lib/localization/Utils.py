import numpy as np
from scipy.ndimage import maximum_filter
import scipy.ndimage as ndimage

def scale(im):
    im1 = im - np.min(im)
    if np.max(im1) > 0:
        im1 = im1/np.max(im1)
    return im1

def top_n_coords(matrix, N, neighborhood=3):
    # Apply max filter
    max_filt = maximum_filter(
        matrix,
        size=neighborhood,
        mode='nearest'
    )

    # Strict local maxima (avoids plateaus)
    mask = (matrix == max_filt)

    # Suppress non-max neighbors inside plateaus
    labeled, num = ndimage.label(mask)
    coords = []

    for label in range(1, num + 1):
        indices = np.argwhere(labeled == label)
        # pick the strongest point in the plateau
        values = matrix[indices[:, 0], indices[:, 1]]
        coords.append(indices[np.argmax(values)])

    coords = np.array(coords)

    # Sort by peak value
    values = matrix[coords[:, 0], coords[:, 1]]
    idx = np.argsort(values)[::-1][:N]

    return coords[idx]

def convert_coords_to_m(matrix, coords, xrange, yrange):
    row, col = coords
    return [
        convert_index_to_m(col, xrange, matrix.shape[1]), 
        convert_index_to_m(row, yrange, matrix.shape[0]) 
    ]
    
def convert_index_to_m(x, ax_range, n):
    return min(ax_range) + x * ((max(ax_range) - min(ax_range)) / n)