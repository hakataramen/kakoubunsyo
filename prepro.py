#!/usr/bin/python3
# -*- coding;utf-8- -*-

#all_relation_info, all_tr_info, tr_sp_doc, t_ls, a_ls
import tr_all
import shelve
import MeCab


def lists_to_sents(lists):
    for line in lists:
        line = line
    return line

def line_to_ngrams(line):
    ngram_list =[]
    if len(line) >= n:
        #文字列の長さ-n+1までの要素を持つリストを用意[0,1,2...(len-n+1)-1]
        for i in range(len(line)-n+1):
            ngram_list.append(tuple(line[i:i+n]))# iからi+nの1つ前の幅で区切りリストへ入れる
    return(ngram_list)
    
def convert_to_idx(ngram, dictionary):
    #ngramのペアを受け取り、対応するインデックス番号に変換
    #dは辞書と同じように扱えるオブジェクト
    if ngram not in dictionary:
        new_idx = len(dictionary) + 1 #0番目からはじまるので+1
        dictionary[ngram] = new_idx
        return new_idx
    else:
        return dictionary[ngram] #id

def instance_vec_to_string(instance_vec):
    #受け取ったinstance_vecを文字列に変換(確認用)
    out = ""
    for key, value in sorted(instance_vec.items(), key=lambda x:x[0]):
        out += "%d:%d" %(key, value)
    out = out[:-1]
    return(out)


    
#mecab_tagger = MeCab.Tagger('mecabric')
#_ = mecab_tagger.parseToNode("マイクテスト")#空撃ち

n=2
if n==1:
    db = shelve.open("unigram_shelve.db")
if n==2:
    db = shelve.open("bigram_shelve.db")
if n==3:
    db = shelve.open("trigram_shelve.db")

if "dic" not in db:
    db["dic"]= {}

d = db["dic"]

for lists in tr_all.tr_sp_doc:
    line = lists_to_sents(lists)#['','',''....,''],一文

    instance_vec = {}#ngramをBOW表現するため
                          
    for ngram in line_to_ngrams(line):#ngram:1ペア分
        idx = convert_to_idx(ngram, d)

        if idx not in instance_vec: #インデックス番号が辞書の中にあるか確認
            instance_vec[idx] = 0
        instance_vec[idx] += 1
    
    print(instance_vec)
