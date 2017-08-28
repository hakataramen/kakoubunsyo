#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

if len(sys.argv) < 3:
    exit()


#txtname = sys.argv[1]
#annname = sys.argv[2]

dirpath_txt = sys.argv[1]
dirpath_ann = sys.argv[2]
if dirpath_txt[-1] != "/": dirpath_txt += "/"
if dirpath_ann[-1] != "/": dirpath_ann += "/"

    
#kakou_txtフォルダから元のテキストを一文字ずつ区切ってリストへ追加

for txtfilename, annfilename in zip(os.listdir(dirpath_txt), os.listdir(dirpath_ann)):
    txt_split=[]
    with open(dirpath_txt+txtfilename, "r") as txt:
       
        #with open(tr_filename, "w") as tr_txt:
            for line in txt.read():
                txt_split += line
    #アノテーションファイルの並び順を加工用語の開始位置順でソート
    tr_info = []
    with open(dirpath_ann+annfilename, "r") as ann:
        for line in ann.readlines():
            if line.startswith("T"):
                idx, tag, start, end, word = line.split()
                tr_info.append((idx, start, end, word))
                tr_info = list(sorted(tr_info, key=lambda x:int(x[1])))
                #print(tr_info)
                            
    #アノテーションファイルを逆順に取り出し加工用語をインデックスに置換
    for line in tr_info[::-1]:
        txt_split[int(line[1]):int(line[2])]=list(" $"+line[0]+"$ ")
    with open("tr_"+txtfilename, "w") as tr_txt:
        tr_txt.write("".join(txt_split))

            
