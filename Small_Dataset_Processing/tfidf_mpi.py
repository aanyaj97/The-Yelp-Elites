import csv 
from mpi4py import MPI
import numpy as np 
from scipy.sparse import csr_matrix, vstack
import time 
import csv 
import json 
from scipy.linalg import fractional_matrix_power
import scipy.sparse.linalg as lin

def create_embmat(review_csv, vocab_json): 
    print('yo')
    start_time = time.time() 
    comm = MPI.COMM_WORLD
    rank, size = comm.Get_rank(), comm.Get_size() 
    print(rank, size)
    if rank == 0: 
        csvfile = open(review_csv)
        readCSV = csv.reader(csvfile, delimiter=',')
        review_data = np.array(list(readCSV))
        tot = len(review_data) 
        comm.bcast(tot, root=0) 
        chunks = np.array_split(review_data, size)
    else: 
        chunks = None 
        tot = comm.recv(source=0, tag=7)
    print(tot)
        #tot = comm.recv(source=0, tag=7)    


