# -*- coding: utf-8 -*-
from unicodedata import name
from data import build_corpus
from utils import extend_maps, prepocess_data_for_lstmcrf, load_model
from evaluate import hmm_train_eval, crf_train_eval, \
    bilstm_train_and_eval, ensemble_evaluate

import pdb
import re
from zhon.hanzi import punctuation

def Find_url(string): 
    url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', string)
    return url 

def extract(model_input):
    urls = Find_url(model_input)
    model_input = re.sub(r'http\S+', '', model_input)
    test_word_lists = re.split('[，。；]', model_input)
    test_word_lists = [list(i) for i in test_word_lists]
    # 训练评估CRF模型
    # print("CRF模型")
    CRF_MODEL_PATH = 'Lab3/api/NER/ckpts/crf.pkl'
    crf_model = load_model(CRF_MODEL_PATH)
    crf_pred = crf_model.test(test_word_lists)

    organizations = []
    names = []
    address = []
    for i in range(len(crf_pred)):
        org = ''
        name = ''
        addr = ''
        for j in range(len(crf_pred[i])):
            if crf_pred[i][j] in ['B-organization','I-organization','E-organization','B-company', 'I-company','E-company']:
                org  += test_word_lists[i][j]
            if crf_pred[i][j] in ['I-name', 'B-name', 'E-name']:
                name += test_word_lists[i][j]
            if crf_pred[i][j] in ['I-address', 'B-address', 'E-address']:
                addr += test_word_lists[i][j]
        for i in punctuation:
            name = name.replace(i, '')
            org = org.replace(i, '')
            addr = addr.replace(i, '')
        if(org != '' and org not in organizations):
            organizations.append(org)
        if(name != '' and name not in names):
            names.append(name.strip())
        if(addr != '' and addr not in address):
            address.append(addr)
    return organizations, names, address, urls
if __name__ == "__main__":
    model_input = '''2019年是锂离子电池事业的“高光”时刻，当年的诺贝尔化学奖授予了三位对锂离子电池的发明和发展具有杰出贡献的科学家和工程师，他们分别是斯坦利·惠廷厄姆（M. Stanley Whittingham）、约翰·古迪纳夫（John B. Goodenough）和吉野彰（Akira Yoshino）。

 

其中，古迪纳夫教授的贡献在于，他在1980年左右提出了一种锂离子电池阴极材料——层状六方化合物钴酸锂。直到现在，我们兜里的手机都配有由这种材料演变而出的一些阴极材料，例如，用镍、锰等元素替换钴元素，或者将镍、锰、铁、镁、铝等掺杂在钴酸锂中。不过，它们的结构都是层状结构，且具有一个共同特征：具备储存和释放锂离子的能力，从而让锂离子在阴极的层与层之间进行可逆地嵌入和脱嵌，并且理想情况下不会破坏阴极材料的基本结构。



同样的，电池阳极也应该具备同等的能力：1983年，Richard Yazami博士证实，层状结构的石墨能够可逆地嵌入、脱嵌锂离子，而成为了极好的阳极候选者。但是要想进一步提升锂离子电池的性能，科学家仍在继续寻找和尝试新的阳极材料，如硅阳极和锂金属阳极。

 

尽管阴极材料的研究已经相对成熟，但阳极材料的优化，以及用固体电解质代替危险的液体电解质的相关研究却陷入了困境。因此，可以说，目前锂离子电池的发展进入了瓶颈期。

 

不过，还有一些科学家顺势思考了另外一个问题：是否能够在现有材料的基础上多“挤”出一些电能？

 

最近，美国SLAC国家加速器实验室、普渡大学、弗吉尼亚理工大学和欧洲同步辐射实验室（ESRF）的研究者共同在《科学》杂志上发表了一项研究，在如何开发长寿命锂离子电池的关键问题上，这些科学家反而要从“电池为何会失活”当中寻找答案。

 



把一块电极“减”到颗粒



需要说明的一点是，在锂离子电池充电时，阴极材料会把它事先储存的锂离子，经过电解质、隔膜，传送到阳极，并储存在阳极的层间。在放电时，锂离子的传递过程会反过来，即从阳极到阴极。在锂离子不断进出电极的过程中，理想情况下是不会破坏电极结构的，但事实并非如此，这也是电池逐渐失活的关键诱因。

 

说到电极，你的脑海里会浮现出什么？一块电极板？毕竟在我们的教材里，电极就是插进电解液中的一块“板”。但事实上，电极是由数百万个电极颗粒层层堆叠而成的。这样也许就很好理解，当锂离子进来或出去时，会不可避免地与电极颗粒发生碰撞或其他相互作用，从而使电极颗粒出现裂纹。经过反复充放电后，电极颗粒也会因此失去电化学活性。



不过，此前大部分研究都主要关注于单个颗粒的特征，例如颗粒的大小和形貌，却鲜有研究关注颗粒的群体行为。但是，没有一个颗粒是一座孤岛，颗粒网络会如何随充放电发生变化也非常重要。

 



颗粒的群体行为

 

事实上，这支由多家单位组成的研究团队在2019年就发表了2项研究，他们通过同步辐射X射线，以及计算模拟和机器学习，“看”到了锂离子电池发生损伤的数千个电极颗粒。重要的是，他们发现，电极颗粒并不是同时失效的，有一些位置的颗粒会更快地失活。例如，相比于距离电极更近的颗粒，距离电池隔膜更近的颗粒会被过度“使用”，而更快地丧失电化学活性。而且，这种“非均匀失活”现象在更厚的电极和快充条件下更加严重。

 

看到这里，我们也许还不太清楚这种非均匀性为何会引起他们的注意。不过，在2021年，这支团队在《自然·材料学》杂志上发表文章称，不同电极颗粒在充放电中表现得不同其实非常重要。此前，科学家一直认为锂离子会同时且以几乎相同的速度，从所有电极颗粒中流出或流进。但这支团队发现，在充电时，有一些颗粒能立即释放出锂离子，但同时，有一些颗粒则几乎不怎么“干活”。研究人员表示，这种“非均匀”行为会给电极的一些“员工”施加太大的压力，从而降低它们的寿命。而且，在多次循环中，这些勤奋的颗粒“员工”一直都是工作的主干，而一开始不好好干活的颗粒也并没有什么进步。



在最近发表于《科学》的这项新研究中，这支团队再次发现了“均一性”的重要性。这一次，他们把目光专门放在了锂离子电池的阴极材料上，且选用的是一种富镍的复合阴极——由多层锂镍锰钴氧化物（NMC）颗粒，以及导电碳和黏合剂结合而成，其中活性颗粒被包裹在导电碳中。他们通过同步辐射X射线断层扫描成像、计算模拟，以及计算机视觉技术，研究经历多次快充条件下（5C）的充放电循环（10次和50次）后，电池阴极的微观结构——阴极颗粒的特征所发生的变化。



按照普渡大学赵克杰教授（这项研究的通讯作者之一）所说，这些阴极颗粒就像人一样，一开始每个人都各走各的路，然后遇到了同伴，于是就走在了一起。因此，“我们不仅需要研究单个颗粒的电化学行为，还需要了解这些颗粒在群体中的表现。”

 

最终，研究人员通过计算机视觉识别出2000多种阴极颗粒，随后经计算模拟，得到了各个颗粒的大小、形貌和表面粗糙度等个体特征，并获得了更多的群体特征，例如这些颗粒之间是如何相互接触的，以及它们的形貌差异。

 

通过分析这些特征，他们发现了一个非常特别的变化趋势：在10次充放电循环后，决定颗粒是否发生损伤及失效的最关键因素是颗粒的个体特征，如颗粒的比表面积、是否是球形。然而，在经历50次充放电循环后，最关键的因素反而是这些颗粒是否具有类似的颗粒大小、颗粒的排列以及形貌等是否均一这样的“均一性”群体特征。



我们可以看到，随着充放电循环的进行，或者说，手机使用了更长时间（如1年）后，决定锂离子电池寿命的是电极颗粒之间的相互作用。这对于科学家和工程师而言非常重要，因为他们可以开发相关技术，通过设计和制造电池电极来控制颗粒的群体行为，从而多“挤”一些电能出来。

 

美国SLAC国家加速器实验室的刘宜晋（这项研究的通讯作者之一）提出：“可以利用磁场或电场来控制颗粒之间的排列。”弗吉尼亚理工大学的林锋教授（这项研究的通讯作者之一）表示，他们实验室目前正在重新设计电池电极，目的是制造支持快充且长寿命的电极结构。

 


参考链接：

https://www.science.org/doi/10.1126/science.abm8962

https://vtx.vt.edu/articles/2022/04/science-feng_lin_battery_recharge_lifespan_testing.html

https://onlinelibrary.wiley.com/doi/10.1002/aenm.201900674

https://www.sciencedirect.com/science/article/abs/pii/S0022509619303126?via%3Dihub

https://www.nature.com/articles/s41563-021-00936-1

https://www.cnet.com/tech/mobile/does-fast-charging-affect-battery-life-6-phone-battery-questions-answered/

https://batteryuniversity.com/article/bu-409-charging-lithium-ion'''
    org, name, address, urls  = extract(model_input)
