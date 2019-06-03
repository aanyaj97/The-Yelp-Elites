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
    start_time = time.time() 
    comm = MPI.COMM_WORLD
    rank, size = comm.Get_rank(), comm.Get_size() 
    if rank == 0: 
        csvfile = open(review_csv)
        readCSV = csv.reader(csvfile, delimiter=',')
        review_data = np.array(list(readCSV))
        chunks = np.array_split(review_data, size) 
    else: 
        chunks = None 
    chunk = comm.scatter(chunks, root=0)
    chunk = embedding(chunk, vocab_json)
    gathered_chunks = comm.gather(chunk, root=0)
    elapsed_time = time.time() - start_time
    print('gathered chunks done', elapsed_time)
    print(gathered_chunks)
    M = sum(gathered_chunks)
    elapsed_time = time.time() - start_time
    print('created m', elapsed_time)
    print('running svd')
    U, s, Vt = lin.svds(M, k=50)
    elapsed_time = time.time() - start_time
    print('ran svd', elapsed_time)
    print('creating mat')
    sig = fractional_matrix_power(np.diag(s), 0.5)
    W = np.matmul(U, sig)
    np.savez('matrix_W.npz', W)
    elapsed_time = time.time() - start_time
    print('completed', elapsed_time)


def embedding(chunk, vocab_json): 
    with open(vocab_json,  errors='ignore') as vj: 
        vocab = json.load(vj, strict=False)
        v = len(vocab)
        M = np.zeros((v, v))
        window = 5 #intend to keep this constant 
    for review in chunk: 
        for index in range(len(review)):
            if review[index] not in vocab: 
                continue
            pairs = back(vocab, review, index, window)
            pairs += front(vocab, review, index, window)
            for pair in pairs:
                index0 = vocab[pair[0]]
                index1 = vocab[pair[1]]
                M[index0, index1] += 1
    s = M.sum()
    Nw = M.sum(axis=1)
    Nc = M.sum(axis=0)
    M = M + np.ones((v, v))
    M = M * M.sum()
    for i in range(v):
        M[i] = M[i] / (Nw[i] + 1)
        M[:, i] = M[:, i] / (Nc[i] + 1) 
    M = np.log(M)
    M = M[:10000, :10000]
    return M 


def front(vocab, words, index, window):
    front_pairs = []
    word = words[index]
    num_context = 0
    length = len(words)
    counter = 1 
    index += 1
    while (counter < window and index < length):
        context = words[index]
        if context in vocab:
            front_pairs.append((word, context))
            num_context += 1
        counter += 1
        index += 1 
    return front_pairs
    
def back(vocab, words, index, window):
    back_pairs = []
    word = words[index]
    num_context = 0
    length = len(words)
    counter = 1 
    index -= 1
    while (counter < window and index >= 0):
        context = words[index]
        if context in vocab:
            back_pairs.append((word, context))
            num_context += 1
        counter += 1
        index -= 1
    return back_pairs


if __name__ == "__main__": 
    create_embmat('review_text_list.csv', 'vocab_ind20.json')

