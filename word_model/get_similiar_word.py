from gensim.models import Word2Vec
from collections import defaultdict
import os

"""
该文件是为了得到所有和“说”意思相近的词，采用了广度优先搜索的办法，最后将所有相似的单词写入./Data/similar_word.txt
"""

def get_related_words(initial_words,model_path):
    model = Word2Vec.load(model_path)
    visited = initial_words
    seen = set()
    max_size = 100
    while(visited and len(visited)<max_size):
        froninter = visited.pop()
        if froninter in seen:
            continue
        similiar_words = [k for k,s in model.similar_by_word(froninter,topn=20)]
        for word in similiar_words:
            if word in seen:
                continue
            visited = [word] + visited
        seen.add(froninter)
    return seen
def save_similar_word(file_path,model_path,initial_words):
    similar_word = get_related_words(initial_words,model_path)
    string = ' '.join(similar_word)
    with open(file_path,'w') as f:
        f.write(string)
    return True

if __name__ == "__main__":
    model_path = "../Data/word2vec_wikicorpus.model"
    file_path = './Data/similar_word.txt'
    initial_words = ['说','称','表示']
    result = save_similar_word(file_path,model_path,initial_words)
    if result:
        with open(file_path,'r') as f:
            string = f.readlines()
            print(string)