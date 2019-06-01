
import json 
import re 
import nltk 
#nltk.download('punkt')
#nltk.download('stopwords')
from nltk.corpus import stopwords 



#import file that indicates how many times word 
with open('revfreq_dict.json') as f: 
    freq_dict = json.load(f)

def create_vocab(len_vocab): 
    words = list(freq_dict.items())
    stop_words = stopwords.words('english')
    top_words = sorted(words,key=lambda x:(-x[1],x[0]))
    vocab_list = [pair[0] for pair in top_words[:len_vocab]
                  if pair[0] not in stop_words]
    vocab_dict = {}
    for i in range(len(vocab_list)):
        vocab_dict[vocab_list[i]] = i
    return vocab_dict



#Should be used in minimum 250 reviews. There are over 6 million ones. 
#vocab_mini = create_vocab(250, freq_dict)




