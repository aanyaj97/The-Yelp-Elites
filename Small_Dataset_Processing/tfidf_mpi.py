import csv 
from mpi4py import MPI
import numpy as np 
from scipy.sparse import csr_matrix, vstack, save_npz 
import time 
import csv 
import json 
from scipy.linalg import fractional_matrix_power
import scipy.sparse.linalg as lin
import math 

def create_embmat(review_csv, vocab_json, freq_json): 
    start_time = time.time() 
    comm = MPI.COMM_WORLD
    rank, size = comm.Get_rank(), comm.Get_size() 
    if rank == 0: 
        csvfile = open(review_csv)
        readCSV = csv.reader(csvfile, delimiter=',')
        review_data = np.array(list(readCSV))
        tot = len(review_data) 
        comm.send(tot, dest=1, tag=7) 
        chunks = np.array_split(review_data, size)
    else: 
        chunks = None 
        tot = comm.recv(source=0, tag=7)
    chunk = comm.scatter(chunks, root=0)
    chunk = tfidf(chunk, vocab_json, freq_json, tot) 
    gathered_chunks = comm.gather(chunk, root=0)
    elapsed_time = time.time() - start_time
    print('gathered chunks done', elapsed_time)
    tfidf_mat = vstack(gathered_chunks)
    save_npz('tfidf.npz', tfidf_mat) 
    elapsed_time = time.time() - start_time
    print('completed', elapsed_time)


def tfidf(chunk, vocab_json, freq_json, tot):
    with open(vocab_json,  errors='ignore') as vj: 
        vocab = json.load(vj, strict=False)
    with open(freq_json,  errors='ignore') as fj: 
        freq = json.load(fj, strict=False) 
    v = len(vocab)
    vec_list = []
    for review in chunk: 
        vec = np.zeros(v)
        for word in review: 
            if word in vocab: 
                idf = math.log(tot / freq[word])
                tf = review.count(word) / len(review)
                vec[vocab[word]] = tf * idf
        vec = csr_matrix(vec)
        vec_list.append(vec)
    mat = vstack(vec_list )
    return mat 



if __name__ == "__main__": 
    create_embmat('review_text_list.csv', 'vocab_ind20.json', 'vocab_freq20.json') 
