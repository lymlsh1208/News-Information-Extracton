import os
import re
import jieba
from pyltp import SentenceSplitter   #分割句子
from pyltp import Postagger   #词性标注
from pyltp import NamedEntityRecognizer   #命名实体识别
from pyltp import Parser   #依存句法分析
import pandas as pd

"""
该文件将句子分割进行命名实体识别、依存分析，找到所有符合主谓关系并且谓语和“说”意思相近的句子，将主语和宾语写入到一个字典中
"""


def split_sentences(string):   #分割句子
    sents = SentenceSplitter.split(string)
    sentences = [s for s in sents if len(s)!= 0]
    return sentences

def deal(string):    #处理句子，返回数字和文字 切割后的结果
    string = re.findall('[\d|\w|\u3002 |\uff1f |\uff01 |\uff0c |\u3001 |\uff1b |\uff1a |\u201c |\u201d |\u2018 |\u2019 |\uff08 |\uff09 |\u300a |\u300b |\u3008 |\u3009 |\u3010 |\u3011 |\u300e |\u300f |\u300c |\u300d |\ufe43 |\ufe44 |\u3014 |\u3015 |\u2026 |\u2014 |\uff5e |\ufe4f |\uffe5]+',string)
    return ' '.join(jieba.cut(string))
def split_words(sentences):
    sents = [deal(s) for s in sentences]
    return sents
def get_word_pos(ltp_model_path,sents):   #词性标注
    model_path = ltp_model_path
    pos_model_path = os.path.join(model_path,'pos.model')
    postagger = Postagger()
    postagger.load(pos_model_path)   #导入词性标注模型
    postags = [postagger.postag(words.split()) for words in sents]
    postags = [list(w) for w in postags]
    postagger.release()
    return postags

def dependency_parsing(ltp_model_path,sents,postags,said):
    LTP_DATA_DIR = ltp_model_path   #ltp模型目录路径
    par_model_path = os.path.join(LTP_DATA_DIR,'parser.model')
    ner_model_path = os.path.join(LTP_DATA_DIR,'ner.model')

    recognizer = NamedEntityRecognizer()   #初始化实例，命名实体识别
    recognizer.load(ner_model_path)

    parser = Parser()   #初始化实例，依存句法分析
    parser.load(par_model_path)

    contents = []
    for i in range(len(sents)):
        words = sents[i].split()   #每句话的单词
        pos = postags[i]    #该句子的词性标注
        nertags = recognizer.recognize(words,pos)    #命名实体识别标注结果
        #print(list(nertags))
        if ('S-Ns' not in nertags) and ('S-Ni' not in nertags) and ('S-Nh' not in nertags):
            continue
        arcs = parser.parse(words,pos)   #依存句法分析结果,标注该句子是主谓关系还是动宾关系等等
        arcs = [(arc.head,arc.relation) for arc in arcs]
        arcs = [(i,arc) for i,arc in enumerate(arcs) if arc[1] == 'SBV']  #找出所有主谓关系的句子，如“我说"
        for arc in arcs:
            verb = arc[1][0]
            subject = arc[0]
            if words[verb - 1] not in said:   #如果不是和“说”意思相近的词则跳过
                continue
            contents.append((words[subject],''.join(words[verb:])))   #形成一个列表，每个元素都是代表一个言论，某某，说，什么
    parser.release()
    recognizer.release()
    return contents

def del_sentences(string):
    file_path = './Data/similar_word.txt'   #导入相似词
    with open(file_path,'r') as f:
        s = f.readlines()
        said= s[0].split(' ')
    ltp_model_path = "./Data/model/"
    sentences = split_sentences(string)
    sents = split_words(sentences)
    postags = get_word_pos(ltp_model_path,sents)
    contents = dependency_parsing(ltp_model_path,sents,postags,said)
    contents_dict = {}
    for index,content in enumerate(contents):
        contents_dict[str(index)] = [content(0),content(1)]
    return contents_dict

if __name__ == "__main__":
    file_path = "./Data/news_chinese.csv"
    news = pd.read_csv(file_path)
    news_content = news['content']
    result = []
    for i in range(len(news_content)):
        opinion = del_sentences(news_content[i])
        result.append([news_content[0],opinion])   #形成一个列表，每个元素包含新闻标题、新闻观点
    print(result)









