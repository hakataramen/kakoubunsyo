#!/bin/python3
#-*- coding: utf-8 -*-

import sys

tr_path = sys.argv[1]
doc_path = sys.argv[2]

tr_info = []
with open(tr_path,'r') as f:
    for line in f.readlines():
        if line[0] == 'T':
            sp = line.split(' ')
            tr_info.append([sp[0],sp[2],sp[3],sp[4].strip()])
        else:
            break


    with open(doc_path, 'r') as f:
        doc = f.read()
        len_doc = len(doc)
        sp_doc = doc.split(' ')
        print(sp_doc)
        for tr_word, start, end, word in sorted(tr_info, key=lambda x:int(x[1]))[::-1]:
            #print("tr_word, start, end, word",'{} {} {} {}'.format(tr_word, start, end, word))
            total_len = 0
            for i, words in enumerate(sp_doc):
                #print("i, words",'{} {}'.format(i, words))
                if total_len == int(start if not words.startswith('\n') else int(start)  -1):
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
                    print('{} {}'.format(sp_doc[tr_start:tr_end], word))
                    sp_doc[tr_start:tr_end] = [tr_word]
                    break
                total_len += len(words)
                #print("total_len",total_len)

        print(sp_doc)
        tr_sp_doc =[]
        for i in sp_doc:
            tr_sp_doc.append(i.strip())
        tr_sp_doc[-1:] =[]
        print(tr_sp_doc)
