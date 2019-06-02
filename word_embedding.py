import numpy as np 
from scipy import spatial

with np.load('matrix_W.npz') as data:
    W = data['arr_0']

# Saved vocabulary as json file
import json
vocab_file = open('Small_Dataset_Processing/vocab_ind20.json')
vocab_str = vocab_file.read()
vocab = json.loads(vocab_str)

index_to_word = {}
for word in vocab.keys():
    index = vocab[word]
    index_to_word[index] = word

def close_words(word, num_words):
    if (word not in vocab or vocab[word] > 9999): 
        print('word not in vocabulary')
        return None 
    d = np.shape(W)[0]
    W_hat = W - W[vocab[word]]
    norms = np.sum(W_hat**2, axis=1)
    indices = norms.argsort()[:num_words + 1]
    word_list = [index_to_word[i] for i in indices]
    for w in word_list: 
        if w == word: 
            continue 
        print(w)

def print_words(word_list, num_words): 
    for word in word_list: 
        print("These are closest words to: " + word)
        close_words(word, num_words)
        print("\n") 


def analogy_words(word_tup, k): 
    for word in word_tup:
        if (word not in vocab or vocab[word] > 9999): 
            print(word + ' not in vocabulary')
            return None 
    with np.load('matrix_W.npz') as data:
        W = data['arr_0']
    index_to_word = {}
    for w in vocab.keys(): 
        index = vocab[w]
        index_to_word[index] = w
    d = np.shape(W)[0]
    vec = W[vocab[word_tup[1]]] - W[vocab[word_tup[0]]] + W[vocab[word_tup[2]]]
    W_hat = W - vec
    norms = np.sum(W_hat**2, axis=1)
    indices = norms.argsort()[:k + 3]
    word_list = [index_to_word[i] for i in indices]
    w_index = 0 
    print("If " + word_tup[0] + ":" + word_tup[1] + " then " + word_tup[2] + ":" )
    for w in word_list: 
        if w in word_tup: 
            continue
        elif w_index < k: 
            print(w)
        w_index += 1 

# def print_analogies(analogy_list, vocab, k): 
#     for word_tup in analogy_list:
#         print("If " + word_tup[0] + ":" + word_tup[1] + " then " + word_tup[2] + ":" )
#         analogy_words(word_tup, vocab, k)
#         print("\n")


    


