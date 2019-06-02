import numpy as np
import random
from scipy.sparse import csr_matrix, vstack 

def make_dummy_array():
    r1 = np.random.randint(10, 100)
    mat_list = []
    vec0 = np.zeros(1000)
    vec0[25] = 12.2
    vec0 = csr_matrix(vec0)
    for i in range(500):
        vec = np.zeros(1000)
        for j in range(r1):
            r_index = np.random.randint(0, 999)
            r_val = random.uniform(0.0, 20.0)
            vec[r_index] = r_val
            mat_list.append(vec)
    mat = np.array(mat_list)
    return mat 
