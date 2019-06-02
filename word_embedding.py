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


    


