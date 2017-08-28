#!/bin/python3
#-*- coding: utf-8 -*-

import sys
import os

dir_path_txt= sys.argv[1]
dir_path_ann = sys.argv[2]

if dir_path_txt[-1] != "/": dir_path_txt += "/"
if dir_path_ann[-1] != "/": dir_path_ann += "/"

#tr_path = sys.argv[1]
#doc_path = sys.argv[2]

#t_ls=[] 
#a_ls=[]

t_ls=(sorted(os.listdir(dir_path_txt)))
a_ls=(sorted(os.listdir(dir_path_ann)))

#print(t_ls,a_ls)
    
#専門用語置換、および関係性のリスト作成
def replace_word_for_idx(dir_path_txt, dir_path_ann):

    
    all_relation_info=[]
    all_tr_info=[]
    tr_sp_doc =[]
    
    for txtfilename, annfilename in zip(t_ls, a_ls):
        #print(txtfilename, annfilename)
        #print()
        
        relation_info = []
        tr_info = []
        with open(dir_path_ann+annfilename,'r') as f:
            for line in f.readlines():
                if line[0] == 'T':
                    sp = line.split(' ')
                    tr_info.append([sp[0],sp[2],sp[3],sp[4].strip()])
                else:
                    rel = line.split(' ')
                    #[0]:R_idx,[1]:relation_type,[2]:arg1,[3],arg2
                    relation_info.append([rel[0],rel[1],rel[2],rel[3].strip()])
                    
        all_tr_info.append(tr_info)
        all_relation_info.append(relation_info)


        
        with open(dir_path_txt+txtfilename, 'r') as f:
            #print("-------------------"+txtfilename+"----------------------------")
            doc = f.read()
            len_doc = len(doc)
            sp_doc = doc.split(' ')
            #print(sp_doc)
            for tr_word, start, end, word in sorted(tr_info, key=lambda x:int(x[1]))[::-1]:
                #print("tr_word, start, end, word",'{} {} {} {}'.format(tr_word, start, end, word))
                total_len = 0
                for i, words in enumerate(sp_doc):
                    #print("i, words",'{} {}'.format(i, words))
                    if total_len == int(start if not words.startswith('\n') else int(start) -1):
                        #print("total_len,start",'{} {}'.format(total_len,start))
                        tr_start = i
                        end_pos = total_len
                        #print('total_len',total_len)
                        #print('end_pos',end_pos)
                        for j, w in enumerate(sp_doc[i:]):
                            #print("j, w",'{} {}'.format(j, w))
                            end_pos += len(w)
                            #print("end_pos",end_pos)
                            if end_pos >= int(end):
                                tr_end = tr_start + j + 1
                                #print("tr_end",tr_end)
                                break
                        #print('{} {}'.format(sp_doc[tr_start:tr_end], word))
                        sp_doc[tr_start:tr_end] = [tr_word]
                        break
                    total_len += len(words)
                    #print("total_len",total_len)

            #print(sp_doc)
            #print(txtfilename, annfilename)     
            one_doc=[]
            sent=[]
            for i in sp_doc:
                if i.startswith("\n"):
                    one_doc.append(sent)
                    #print(sent)
                    sent=[]
                    sent.extend(i.split())
                else:
                    sent.append(i)
            tr_sp_doc.append(one_doc)        

            #tr_sp_doc[-1:] = []
            #print(tr_sp_doc)

            #with open("tr_wakati_"+txtfilename, "w") as tr_txt:
                #tr_txt.write(" ".join(tr_sp_doc))
    return (doc, sp_doc,tr_sp_doc, all_tr_info, all_relation_info)

def get_labels(tr_sp_doc, all_relation_info):
    new_l =[]
    for one_doc in all_relation_info:
        for tag, relation, arg1, arg2 in one_doc:


            for lines in tr_sp_doc:
                for line in lines:
                    ls = []
                    if arg1.strip("Arg1:") and arg2.strip("Arg2:") in line:
                        if relation == "Relation":
                            relation = 1
                        elif relation == "Positive":
                            relation = 2
                        elif relation == "Negative":
                            relation = 3
                        elif relation == "Sub":
                            relation = 4

                        ls.append(relation)
                        ls.extend(line)
                        new_l.append(ls)
                        #print(ls)

                            

    return(new_l)

    
if __name__ == '__main__':
    doc, sp_doc, tr_sp_doc, all_tr_info, all_relation_info=replace_word_for_idx(dir_path_txt, dir_path_ann)
    new_l = get_labels(tr_sp_doc, all_relation_info)   
    print(new_l)
