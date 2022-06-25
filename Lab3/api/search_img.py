############################################################
# 功能: 检索图片
# 参数: 关键字
# 返回值: list, 其中 list 的元素类型为 dict
#        dict 格式为 {'des':xx, # 图片描述
#                    'img':xx, # 图片url
#                     'href':xx # 图片源文链接}
# 算法: 关键字匹配......
############################################################


import json
import math
import re
import sys
import sqlite3
from collections import defaultdict

import jieba
import jieba.analyse
from config import CACHE_PATH

sys.stdout.reconfigure(encoding='utf-8')

# 获取搜索关键词
keywords_ori = sys.argv[1]
keywords_ori = re.split(r'\s+', keywords_ori)
keywords = []
for keyword in keywords_ori:
    keywords.extend(jieba.analyse.extract_tags(keyword))
with open(CACHE_PATH, 'r', encoding='utf8') as f:
    d = json.loads(f.read())
    index = d['img_index']
    seg_dict = d['img_seg']

# 计算匹配范围
img_ids = set()
for keyword in keywords:
    if keyword not in index:
        continue
    img_ids.update(index[keyword])
else:
    img_ids = tuple(img_ids)

# 获取图片

conn = sqlite3.connect('./res.db')
cursor = conn.cursor()

cursor.execute(f'select * from img where id in {img_ids}')
img_list = cursor.fetchall()

conn.commit()
cursor.close()
conn.close()

result = []
for img in img_list:
    d = {'des': img[1], 'href': img[2], 'img': img[3]}
    result.append(d)
print(json.dumps(result,ensure_ascii=False))
