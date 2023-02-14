import numpy as np  

def save_np(filename, np_array):
    with open(filename, 'wb') as f:
        np.save(f, np_array)
        