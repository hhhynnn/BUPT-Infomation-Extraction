############################################################
# 功能: 读取数据库, ① 对文章进行分词 ②构造倒排索引文件
#      将二者的计算结果保存到 CACHE_PATH
# 参数: 无
# 返回值: 无
############################################################

import json
import jieba
import sqlite3
from collections import defaultdict
from debug_function import *
from config import CACHE_PATH

# 1. 读取数据库的所有文件
conn = sqlite3.connect('./res.db')
cursor = conn.cursor()

cursor.execute('select * from article')
articles = cursor.fetchall()

conn.commit()
cursor.close()
conn.close()

print(f"{timestamp()}# 数据库读取完成, 用时{runtime()}")

# 2. 构造倒排索引
iv_index = defaultdict(list)  # 倒排索引
seg_dict = defaultdict(list)  # 分词结果 [id->[word1, word2, ...]]
for article in articles:
    idx = article[0]
    # title = article[1]
    # abstract = article[5]
    content = article[7]
    # ss = f"{title} {abstract} {content}"
    # seg_list = jieba.lcut(ss, cut_all=False)
    seg_list = jieba.lcut(content, cut_all=False)
    seg_dict[idx] = seg_list
    for word in set(seg_list):
        # 添加索引项
        iv_index[word].append(idx)

print(f"{timestamp()}# 文件构造完成, 用时{runtime()}")

# 3. 保存为json
with open(CACHE_PATH, 'w', encoding='utf8') as f:
    d = {'index': iv_index, 'seg': seg_dict}
    f.write(json.dumps(d, ensure_ascii=False))

print(f"{timestamp()}# 文件写入完成, 用时{runtime()}")
