'''
Generates wordcloud based on tf/idf vectors.
Must download wordcloud library first like so: 

git clone https://github.com/amueller/word_cloud.git 
cd word_cloud
pip install .
python setup.py build_ext -i

must also have a .png stored for wordcloud shape
'''

import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import scipy.sparse as sp
import json

def find_top_k_words(tf_idf, word_dict_file, k):

    v = tf_idf.shape[1] # number of words in vocab 
    v_1 = np.sum(tf_idf, axis=0)
    index_array = np.argsort(v_1)
    
    with open(word_dict_file) as filename:
        word_dict = json.load(filename)
    
    index_dict = {}
    for word, index in word_dict.items():
        index_dict[index] = word
    
    freq_dict = {}
    for i in range(1, k+1):
        index = index_array[0, -i]
        word = index_dict[index]
        freq = v_1[0, index]
        freq_dict[word] = freq

    return freq_dict


def run(tfidf_file, word_dict_file, k, png_file=None):
    
    tf_idf = sp.load_npz(tfidf_file)
    tf_idf = tf_idf.toarray() 
    if png_file is not None: 
        cloud_mask = np.array(Image.open(png_file))

    freq_dict = find_top_k_words(tf_idf, word_dict_file, k)
    
    wc = WordCloud(background_color="white", mask=cloud_mask)
    wordcloud = wc.generate_from_frequencies(freq_dict)
    
    plt.imshow(wordcloud, interpolation="bilinear", )
    plt.axis("off")
    plt.show()

    