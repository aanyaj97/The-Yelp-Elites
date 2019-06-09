import numpy as np 
from scipy import spatial


# This is the saved word_embedding matrix computed from embeddings.py 
with np.load('matrix_W.npz') as data:
    W = data['arr_0']

# Saved vocabulary as json file. Vocab has only 20K words. 
import json
vocab_file = open('Small_Dataset_Processing/vocab_ind20.json')
vocab_str = vocab_file.read()
vocab = json.loads(vocab_str)

index_to_word = {}
for word in vocab.keys():
    index = vocab[word]
    index_to_word[index] = word


def close_words(word, num_words):
    '''
    Function that prints words that are similar to each other. Note it only 
    takes the first 10000 words to limit the size of matrix. Can be 
    done with larger vocab sizes. 

    Inputs: 
      word: (string) the word you want to compare in question
      num_words: (int) the number of comparison words you want 

    
    ''' 

    if (word not in vocab or vocab[word] > 9999): #modify condition with larger vocab size
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
    '''
    Calls function repeatedly for a list of words to be compared. 
    ''' 
    for word in word_list: 
        print("These are closest words to: " + word)
        close_words(word, num_words)
        print("\n") 


def analogy_words(word_tup, k): 
    '''
    Finds relevant analogies of words in the vocabulary. Excellent for 
    testing words of sentiment. 

    Input: word_tup tuple of strings in form (word0, word1, word2) 
     
    Note word0 and word1 are related and the function tries to find 
    related words for word2 by computing the nearest embedding 
    vectors for v = v_word1 - v_word0 + v_word2. 

    Sample input (awesome, phenomenal, bad)
    Output: 
        horrible 
        terrible 
        disappointing 
        poor 
        awful 
    ''' 
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



    


