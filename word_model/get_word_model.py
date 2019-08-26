import jieba
from gensim.models import word2vec
from time import time
import os
import logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',level=logging.INFO)

"""
该文件是为了获得词向量模型，也可以直接将模型训练好放入Data文件中
"""

def create_Model(file_path,file_name):
    sentences = word2vec.Text8Corpus(os.path.join(file_path,file_name))   #导入已经切分好的语料
    model = word2vec.Word2Vec(sentences,sg=0,min_count=50,size=300,seed=1,iter=8,workers=15)
    #min_count在较大的语料中，可以忽略出现次数较小的单词
    #size 用来设置神经网络的层数，word2vec中的默认值是设置为100层
    # workers参数用于设置并发训练时候的线程数
    model.save(file_path+"word2vec_wikicorpus.model")
    model.wv.save_word2vec_format(file_path+"word2vec_wikicorpus.model.bin",binary = True)

if __name__=="__main__":
    file_path = './Data/'
    file_name = 'zhwiki_jian_20190720_cutwords.txt'
    create_Model(file_path,file_name)