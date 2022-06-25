############################################################
# 功能: 检索
# 参数1: 搜索算法 (可选: tfidf, bm25)
# 参数2: 搜索关键字
# 返回值: list, 其中 list 的元素类型为 dict
#        dict 格式为 {'title':xx, # 文章标题
#                    'time' :xx, # 发布时间
#                    'url:  :xx, # 原文链接
#                    'relate':xx, # 相关内容
#                    'org':xx,   # 机构名称
#                    'name':xx,  # 人名
#                    'address':xx, # 地址
#                    'urls':xx   # 链接
#        relate 为列表, 分3段, 其中第二段为关键字 (第二段可以高亮显示)
# 举例: 搜索 传递参数 tfidf "可持续发展" 返回 json 如下
#
# {
#     "title": "3D打印产业峰会聚焦前沿技术，3D打印数字维创中心正式启幕！",
#     "time": "2018年01月02日",
#     "url": "https://huanqiukexue.com/a/qianyan/cailiao__huaxue/2018/0102/27705.html",
#     "relate": [
#         "...数字创意，打印未来”——3D打印产业创新",
#         "发展",
#         "高峰论坛隆重开启，此次论坛由中关村科技园区丰台园管理委员..."
#     ],
#     "org": [
#         "北京丰台科技园建设发展有限公司丰科博创北京科技服务有限公司",
#         "管委会",
#         "中关村科技园区丰台园管委会工委委员北京丰台科技园建设发展有限公司",
#         "上海交通大学医学3D打印创新研究中心",
#         "乔治华盛顿大学",
#     ],
#     "name": [
#         "孙睿",
#         "石岩刘亚凡",
#         "陈玉涛陈玉涛",
#         "何镜堂",
#     ],
#     "address": [
#         "中关村科技园区丰台园3D打印数字维创中心",
#         "中关村科技园区丰台园3D打印数字维创中心姚京",
#         "高新科技园区",
#         "中关村丰台区",
#     ],
#     "urls": [],
# },
############################################################
import json
import math
import re
import sys
import sqlite3
from collections import defaultdict

import jieba.analyse
from config import CACHE_PATH
from sys import path

# 信息抽取库
path.append(sys.path[0] + '\\NER')
from NER import main

# >>> 获取搜索关键词
sys.stdout.reconfigure(encoding='utf-8')
mode = sys.argv[1]
keywords_ori = sys.argv[2]
# 获取搜索关键词 <<<

keywords_ori = re.split(r'\s+', keywords_ori)
keywords = []
for keyword in keywords_ori:
    # keywords.extend(jieba.lcut(keyword, cut_all=False)) # 简单拆解
    # keywords.extend(jieba.lcut_for_search(keyword))  # 搜索化拆解
    keywords.extend(jieba.analyse.extract_tags(keyword))  # 搜索化拆解

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


##################################################
# mode = tfidf
# 向量空间检索算法实现
# 1. 利用 TF-IDF 计算词向量
# 2. 计算各文章与查询的向量内积
# 3. 按内积表现的相关度排序
# 4. 输出
##################################################
def search_by_tfidf():
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
        for word in keywords:
            tf_dict[k][word] = seg_list.count(word)
    # 计算 idf
    article_set = set(article_ids)
    doc_cnt = len(article_ids)  # 文章个数
    for word in keywords:
        try:
            doc_set = set(index[word])
        except KeyError:
            doc_set = set()
        try:
            idf_dict[word] = math.log10(doc_cnt / (1 + len(doc_set & article_set)))
        except ValueError:
            idf_dict[word] = 0

    # 计算 tf-idf 向量
    tfidf_vec_dict = defaultdict(list)
    std_vec = [idf_dict[key] for key in keywords]
    for i in article_ids:
        tfidf_vec_dict[i] = [tf_dict[i][key] * idf_dict[key] for key in keywords]

    ##############################
    # 2. 计算向量内积
    ##############################
    sc_dict = dict()  # 相似度字典
    vec_len = len(std_vec)  # 向量长度
    std_vec_len = math.sqrt(sum([v * v for v in std_vec]))  # 标准向量模长
    for i in article_ids:
        sc_dict[i] = 0
        i_vec = tfidf_vec_dict[i]  # 向量 i
        for idx in range(vec_len):
            sc_dict[i] += std_vec[idx] * i_vec[idx]
        sc_dict[i] /= std_vec_len

    ##############################
    # 3. 结果排序并输出
    ##############################
    sc_dict_filtered = dict(filter(lambda kv: kv[1] > 1, sc_dict.items()))
    sc_dict_filtered = sorted(sc_dict_filtered.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    sc_dict_unfiltered = sorted(sc_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    seq = sc_dict_filtered if len(sc_dict_filtered) > 5 else sc_dict_unfiltered[:5]
    return seq


##################################################
# mode = bm25
# bm25 检索算法实现
# 1. 构造字典
# 2. 构造bm25Model
# 3. 搜索
##################################################
import codecs
from gensim import corpora
from gensim.summarization import bm25


def search_by_bm25():
    ##############################
    # 1. 构造字典
    ##############################
    corpus = []
    for aid in article_ids:
        corpus.append(seg_dict[f'{aid}'])
    dictionary = corpora.Dictionary(corpus)

    ##############################
    # 2. 构造 bm25Model
    ##############################
    bm25Model = bm25.BM25(corpus)

    ##############################
    # 3. 搜索
    ##############################
    avg_idf = sum(bm25Model.idf.values()) / len(bm25Model.idf.values())
    scores = bm25Model.get_scores(keywords, avg_idf)
    sc_dict = dict(zip(article_ids, scores))
    sc_dict_filtered = dict(filter(lambda kv: kv[1] > 4, sc_dict.items()))
    sc_dict_filtered = sorted(sc_dict_filtered.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    sc_dict_unfiltered = sorted(sc_dict.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    seq = sc_dict_filtered if len(sc_dict_filtered) > 5 else sc_dict_unfiltered[:5]
    return seq


if mode == 'tfidf':
    result_id_list = search_by_tfidf()
else:
    result_id_list = search_by_bm25()

##################################################
# 根据排序返回要显示的内容
##################################################
result = []
for i, sc in result_id_list:
    d = {
        'title': article_dict[i]['title'],
        'time': article_dict[i]['time'],
        'url': article_dict[i]['url']
    }
    for key in keywords:
        if key not in seg_dict[f'{i}']:
            continue
        content = article_dict[i]['content']
        d['org'], d['name'], d['address'], d['urls'] = main.extract(content)
        pos = content.find(key)
        begin = max(0, pos - 20)
        end = min(len(content), pos + 30)
        relate = [f'...{content[begin:pos]}', content[pos:pos + len(key)], f'{content[pos + len(key):end]}...']
        relate = [each.replace('\n', ' ') for each in relate[:]]
        d['relate'] = relate
        # 格式化信息抽取情况
        for key in ['org', 'name', 'address', 'urls']:
            for idx, ss in enumerate(d[key]):
                d[key][idx] = ss.replace('\n',' ')
        break
    result.append(d)
print(json.dumps(result, ensure_ascii=False, indent=4, separators=(',', ':')))
