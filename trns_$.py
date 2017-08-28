#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import MeCab


if len(sys.argv) < 3:
        exit()

#txtname = sys.argv[1]
#annname = sys.argv[2]

dirpath =sys.argv[1]
if dirpath[-1] != "/": dirpath += "/"
        
#元のテキストを一文字ずつ区切ってリストへ追加
txt_split=[]
with open(txtname, "r") as txts:
    for line in txts.read():
        txt_split += line
                
#アノテーションファイルの並び順を加工用語の開始位置順でソート
tr_info = []
with open(annname, "r") as anns:
    for line in anns.readlines():
        if line.startswith("T"):
                idx, tag, start, end, word = line.split()
                tr_info.append((idx, start, end, word))
    tr_info = list(sorted(tr_info, key=lambda x:int(x[1])))
#print(tr_info)
                        
#アノテーションファイルを逆順に取り出し加工用語をインデックスに置換
for line in tr_info[::-1]:
        txt_split[int(line[1]):int(line[2])]=list("$"+line[0]+"$")
print("".join(txt_split))
