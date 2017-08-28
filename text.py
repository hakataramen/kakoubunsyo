#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import MeCab
from collections import Counter

#tagger = MeCab.tagger('mecabric')
#_ = tagger.parseToNode('空撃ち')

f = sys.argv[1]
g = sys.argv[2]


#tr_info = []
#with open(g, "r") as ann:
#    for line in ann.readlines():
#        if line.startswith("T"):
#            idx, tag, start, end, word = line.split()
#            tr_info.append((idx, start, end, word))

            
tr_info = []
with open(g, "r") as ann:
    for line in ann.readlines():
        if line.startswith("T"):
            idx, tag, start, end, s_word = line.split()
            tr_info.append((idx, start, end, s_word))
            tr_info = list(sorted(tr_info, key=lambda x :int(x[1])))
                           
with open(f, "r") as txt:
    a=txt.read()
    ls = []
    ls.extend(a)
    

    
    ls2=[]
    for idx, start, end, s_word in tr_info:
        counter_word = -1
        counter_space = 0
        for word in ls:
            if word == " ":
                counter_space += 1
            elif word != " ":
                counter_word += 1
                #print(counter_word, start)
                if int(counter_word) == int(start):
                    #print("こっち入った")
                    new_start = int(start)+int(counter_space)
                    if " " in ls[int(new_start):int(end)+int(counter_space)]:
                        counter = Counter(ls[int(new_start):int(end)+int(counter_space)])
                        counter_add = counter[" "]
                        #print("counter", counter[" "])
                        #print("end",end)
                        #print("置き換えするよ")
                        #print("www", ls[int(new_start):int(end)+int(counter_space)+counter_add])
                        ls[int(new_start):int(end)+int(counter_space)+counter_add] = "$"+idx+"$"
                        #ls[int(new_start):int(end+counter_space+counter_add)] = "$"+s_word+"$"
                    else:
                        ls[int(new_start):int(end)+int(counter_space)] = "$"+idx+"$"
                
    print("".join(ls))
#        if i == 50:
#            break
#        if word ==" ":
#            i = i
#            print(i,word)
#        else:
#            i += 1
#            print(i,word)
#        if " " in a[3:7]:
#            print("空白あり")
#        else:
#            print("空白なし")

    #list_a = list(a)
    #print(list_a)

#    for line in tr_info[::-1]:
#        if " " in list_a[int(line[1]):int(line[2])]:
#            counter = Counter(list_a[int(line[1]):int(line[2])])
#            count_add = counter[" "]
#            print("count_add=",count_add)
#            print("list_a[int(line[1]):int(line[2])+count_add]=",list_a[int(line[1]):int(line[2])+count_add])
#            list_a[int(line[1]):int(line[2])+count_add]=list("$"+line[0]+"$")
#        else:
#            list_a[int(line[1]):int(line[2])]=list("$"+line[0]+"$")
#    print(list_a)
