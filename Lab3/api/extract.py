import json
import sys
import sqlite3
from sys import path

path.append(sys.path[0] + '\\NER')

import jieba
import jieba.analyse
from config import CACHE_PATH

from NER import main

sys.stdout.reconfigure(encoding='utf-8')
# 获取搜索关键词
article_id = int(sys.argv[1])

# 读取数据库文件
conn = sqlite3.connect('./res.db')
c = conn.cursor()

c.execute(f"""
    select * from article
    where id = {article_id}
""")

article = c.fetchall()[0]

conn.commit()
conn.close()

org, name, address, urls = main.extract(article[7])

print(json.dumps({
    "org": org,
    "name": name,
    "address": address,
    "urls": urls
},ensure_ascii=False))
