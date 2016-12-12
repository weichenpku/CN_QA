#-*-coding:utf-8-*-

import json
import os, re
import jieba
import jieba.posseg as pseg
import numpy as np
import pandas as pd
import pickle

from util import Loader

raw_qas_path = "../../data/question.txt"

qa_class = set(['n','i','nr','m','t','nt','ns'])
qas_class = {}

def read_raw_data():
    with open(raw_qas_path, 'r', encoding="UTF-8") as f:
        lines = f.readlines()
    qass = {}
    tags = {}
    pattern = re.compile(r"^[0-9]")
    count = 0
    for line in lines:
        qas, ans = "", ""
        line = line.strip()
        if not line:
            continue
        if not pattern.search(line):
            continue
        context = line[line.find('.')+1:]
        if '？' in context:
            qas = context.split('？')[0].strip()
            ans = context.split('？')[1].strip()
        elif ':' in context:
            qas = context.split(':')[0].strip()
            ans = context.split(':')[1].strip()
        qas = ''.join(qas.split()).replace("“","").replace("”","").replace("《","").replace("》","")
        ans = ans.replace("答案","").replace("：","")
        ans = ''.join(ans.split())
        if "下一句" in qas or "www" in ans or "下半句" in qas or "上半句" in qas or "上一句" in qas:
            continue
        if qas == "" or ans == "":
            continue
        
        qas = pseg.lcut(qas)
        ans = pseg.lcut(ans)
        if len(ans) > 1: continue
        q, a = '', ''
        for w, t in qas:
            q += '|' + w + ' ' + t
        for w, t in ans:
            if t not in qa_class: break
            # if t == 'n':
            #     print (w)
            a += '|' + w + ' ' + t
        if a == "": continue
        count += 1
        qass[q[1:]] = a[1:]
        qas_class.setdefault(a[1:].split()[1], [])
        qas_class[a[1:].split()[1]].append(q[1:])

    json.dump(qass, open('../../data/qas_yzdd.json','w', encoding="UTF-8"), ensure_ascii=False)
    json.dump(qas_class, open('../../data/qas_class.json','w', encoding="UTF-8"), ensure_ascii=False)
    print (count)


if __name__ == "__main__":
    read_raw_data()            

    