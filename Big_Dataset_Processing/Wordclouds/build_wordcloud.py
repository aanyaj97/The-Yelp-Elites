'''
Generates wordcloud based on tf/idf vectors.
Must download wordcloud library first like so: 

git clone https://github.com/amueller/word_cloud.git 
cd word_cloud
pip install .
python setup.py build_ext -i

must also have a .png stored for wordcloud shape
(eg yelp_logo.png)

'''

import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import scipy.sparse as sp 


def find_top_k_words(tf_idf_npz, word_dict_file, k):
    '''
    tf_idf_npz: tfidf.npz
    word_dict_file: vocab_ind20.json
    k: # words you'd like in your wordcloud 
    '''
    sparse_tfidf = sp.load_npz(tf_idf_npz) 
    tf_idf = sparse_tfidf.toarray()

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
        index = index_array[-i]
        word = index_dict[index]
        freq = v_1[index]
        freq_dict[word] = freq

    return freq_dict


def run(tf_idf_npz, word_dict_file, k, png_file):
    '''
    png_file = image you'd like your wordcloud to be shaped
    '''

    cloud_mask = np.array(Image.open(png_file))

    freq_dict = find_top_k_words(tf_idf_npz, word_dict_file, k)
    
    wc = WordCloud(background_color="white", mask=cloud_mask)
    wordcloud = wc.generate_from_frequencies(freq_dict)
    
    plt.imshow(wordcloud, interpolation="bilinear", )
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    run('tfidf_npz/SC_tfidf.npz', 'Small_Dataset_Processing/vocab_ind20.json', 1000, 'yelp_logo.png')
