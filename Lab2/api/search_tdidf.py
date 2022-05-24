############################################################
# 功能: 使用 TD-IDF 算法实现搜索
# 参数: 搜索关键字
# 返回值: list, 其中 list 的元素类型为 dict
#        dict 格式为 {'title':xx, # 文章标题
#                    'time' :xx, # 发布时间
#                    'url:  :xx, # 原文链接
#                    'relate':xx}# 相关位置
############################################################
import json
import math
import re
import sys
import sqlite3
from collections import defaultdict

import jieba
from debug_function import *
from config import CACHE_PATH

# 获取搜索关键词
keywords_ori = sys.argv[1]
keywords_ori = re.split(r'\s+', keywords_ori)
keywords = []
for keyword in keywords_ori:
    keywords.extend(jieba.lcut(keyword, cut_all=False))

# 读取倒排索引
with open(CACHE_PATH, 'r', encoding='utf8') as f:
    d = json.loads(f.read())
    index = d['index']
    seg_dict = d['seg']

# 计算文档范围
article_ids = set()
for keyword in keywords:
    if keyword not in index:
        continue
    article_ids.update(index[keyword])
else:
    article_ids = tuple(article_ids)

# 获取文档
conn = sqlite3.connect('./res.db')
cursor = conn.cursor()

cursor.execute(f'select * from article where id in {article_ids}')
article_list = cursor.fetchall()

conn.commit()
cursor.close()
conn.close()

article_dict = dict()
for article in article_list:
    article_dict[article[0]] = {
        'title': article[1],
        'time': article[2],
        'author': article[3],
        'source': article[4],
        'abstract': article[5],
        'url': article[6],
        'content': article[7]
    }

print(f"{timestamp()}# 预处理完成, 用时{runtime()}")
##################################################
# 向量空间检索算法实现
# 1. 利用 TF-IDF 计算词向量
# 2. 计算各文章与查询的向量内积
# 3. 按内积表现的相关度排序
# 4. 输出
##################################################

##############################
# 1. 计算词向量
##############################
tf_dict = defaultdict(dict)  # [文章id][词word] -> word 在 文章i 中的出现次数
idf_dict = dict()  # [词word] -> word 在各个文章中的出现次数

# 计算 tf
for k, article in article_dict.items():
    # 对 content 分词
    seg_list = seg_dict[f'{k}']
    word_set = set(seg_list)
    # 统计 tf 和 df
    for keyword in keywords:
        tf_dict[k][keyword] = seg_list.count(keyword)
# 计算 idf
article_set = set(article_ids)
doc_cnt = len(article_ids)  # 文章个数
for keyword in keywords:
    doc_set = set(index[keyword])
    idf_dict[keyword] = math.log10(doc_cnt / len(doc_set & article_set))

# 计算 tf-idf 向量
tfidf_vec_dict = defaultdict(list)
std_vec = [idf_dict[key] for key in keywords]
for i in article_ids:
    tfidf_vec_dict[i] = [tf_dict[i][key] * idf_dict[key] for key in keywords]
print(f"{timestamp()}# TF-IDF 计算完成, 用时{runtime()}")

##############################
# 2. 计算向量内积
##############################
sc_dict = dict()  # 相似度字典
vec_len = len(std_vec)  # 向量长度
for i in article_ids:
    sc_dict[i] = 0
    i_vec = tfidf_vec_dict[i]  # 向量 i
    for idx in range(vec_len):
        sc_dict[i] += std_vec[idx] * i_vec[idx]

print(f"{timestamp()}# 向量内积计算完成, 用时{runtime()}")

##############################
# 3. 结果排序并输出
##############################
seq = sorted(sc_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

result = []
for i, sc in seq:
    d = {'title': article_dict[i]['title'],
         'time': article_dict[i]['time'],
         'url': article_dict[i]['url']
         }
    for key in keywords:
        if key not in seg_dict[f'{i}']:
            continue
        content = article_dict[i]['content']
        pos = content.find(key)
        begin = max(0, pos - 20)
        end = min(len(content), pos + 30)
        relate = [f'...{content[begin:pos], content[pos:pos + len(key)]}', f'{content[pos + len(key):end]}...']
        relate = [each.replace('\n', ' ') for each in relate[:]]

        d['relate'] = relate
        break
    result.append(d)

print(f"{timestamp()}# 排序计算完成, 用时{runtime()}")

for each in result[:5]:
    print(each)
