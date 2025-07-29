import requests
import zipfile
import re
import os
import urllib
import collections
import random
import shutil
from bs4 import BeautifulSoup
def download():
    # 可以从百度云服务器下载一些开源数据集(dataset.bj.bcebos.com)
    corpus_url = 'https://dataset.bj.bcebos.com/word2vec/text8.txt'
    web_request = requests.get(corpus_url)
    corpus = web_request.content
    with open( "text8.txt", "wb") as f:
        f.write(corpus)
    f.close()
    
def datapreprocess(corpus):
    corpus = corpus.strip().lower()
    corpus = corpus.split(" ")
    return corpus

def build_dictionary(corpus):
    word_freq_dict = dict()
    for word in corpus:
        if word not in word_freq_dict:
            word_freq_dict[word] = 0
        word_freq_dict[word] += 1
    word_freq_dict = sorted(word_freq_dict.items(), key=lambda x: x[1], reverse=True)
    
    word2id_dict = dict()
    word2id_freq = dict()
    id2word_dict = dict()
    for word, freq in word_freq_dict:
        curr_id = len(word2id_dict)
        word2id_dict[word] = curr_id
        word2id_freq[word2id_dict[word]] = freq
        id2word_dict[curr_id] = word

    return word2id_dict, word2id_freq, id2word_dict
word2id_dict, word2id_freq, id2word_dict = build_dictionary(corpus)
vocab_size = len(word2id_dict)
