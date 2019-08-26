import pymysql
import os
import jieba
from collections import defaultdict
import pandas as pd
import socket
socket.setdefaulttimeout(10)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""
该文件从云数据库中读取news_chinese表格，并将title\content两列内容写入到news_chinese.csv文件中
"""

def get_news_from_sql(host,user,password,database,port,file_path):
    connect = pymysql.Connect(host=host,port = port,user = user, passwd= password,db = database)
    cursor = connect.cursor()
    data_news = defaultdict(list)   #形成一个标题+文章的字典
    sql = "select content,title from stu_db.news_chinese"
    cursor.execute(sql)
    data = cursor.fetchall()
    for i in range(len(data)):
        content = data[i][0]
        #content = ' '.join(jieba.cut(content))
        title = data[i][1]
        data_news[title] = content
    df = pd.DataFrame(data = data_news)
    df = df[['title','content']]
    df.to_csv(file_path+"news_chinese.csv",encoding="utf-8")
    print('把数据库中的文章提取到csv文件中')

if __name__ == "__main__":
    host = 'rm-8vbwj6507z6465505ro.mysql.zhangbei.rds.aliyuncs.com'
    user = 'root'
    password = 'AI@2019@ai'
    database = 'stu_db'
    table = 'news_chinese'
    port = 22
    file_path = './Data/'
    get_news_from_sql(host,user,password,database,port,file_path)

