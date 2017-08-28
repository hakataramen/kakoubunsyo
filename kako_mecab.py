#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pdb
import sys
import os
import MeCab

tagger = MeCab.Tagger('mecabric')
_ = tagger.parseToNode("マイクテスト")

def sent_to_feature(sents, tagger):
    for sent in sents:
        node = tagger.parseToNode(sent)
        node = node.next
        surface_list = []
        while node.next:
            if node.surface == '$':
                b =[] #join用
                b.append(node.surface)#$の追加
                node = node.next #$の次のノード
                pdb.set_trace()
                while 1:
                    if node.surface == '$':
                        break
                    b.append(node.surface)#次の$が出るまでbに追加($の次のノード)
                    node = node.next #$の次の次
                b.append(node.surface) #2回目の$をbへ追加
                surface_list.extend("".join(b))#b内をくっつけたものを元リストへ追加
                node = node.next
                
            surface_list.append(node.surface)
            node = node.next
        print(surface_list)
    return surface_list



dirpath_txt = sys.argv[1]

if dirpath_txt[-1] != "/": dirpath_txt += "/"

for txtfilename in os.listdir(dirpath_txt):
    txt_split = []
    with open(dirpath_txt+txtfilename, "r") as txt:
        for line in txt.readlines():
            txt_split.append(line.strip("\n"))
            for surface in sent_to_feature(txt_split,tagger):
                print(surface)
