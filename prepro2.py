#!/bin/python3
# -*- coding:utf-8 -*-

import tr_all3
import numpy as np
from collections import OrderedDict


def get_index_dic(sents_list):
    idx_dic = OrderedDict()

    i = len(idx_dic)+1
    for line in sents_list:#一文
        for word in line:
            if not word in idx_dic:
                idx_dic[word] = i
                i += 1
    return idx_dic

def replace_sents_to_idx_and_get_maxlen(dic, sents_list):
    id_sent =[]
    max_len = 0
    for line in sents_list:
        l_len = len(line)
        if l_len >= max_len:
            max_len = l_len
        one_sent =[]
        for word in line:
            if word in dic:
                    one_sent.append(dic[word])
        id_sent.append(one_sent)        

    return(id_sent, max_len)

def Padding(id_sent, max_len):
    for line in id_sent:
        if max_len < len(line):
            print("Padding Error train max length < test max length ")
        for i in range(max_len-len(line)):#max_lenとの差分出して0埋める回数を出す
                line.append(0)
    return id_sent
            
def make_one_hot_from_labels(label_list):
    labels = []
    for i in label_list:
        one_hot = np.zeros(4)
        one_hot[i-1] = 1
        labels.append(one_hot)
    return labels



    
#tr_sp_doc = tr_all3.tr_sp_doc
label_list = tr_all3.label_list
sents_list = tr_all3.sents_list

idx_dic = get_index_dic(sents_list)
id_sent, max_len = replace_sents_to_idx_and_get_maxlen(idx_dic, sents_list)

id_sent = Padding(id_sent, max_len)
one_hot_labels = make_one_hot_from_labels(label_list)

data_x = np.array(id_sent)
data_y = np.array(one_hot_labels)
#print(idx_dic)
#print(sent_idx)
