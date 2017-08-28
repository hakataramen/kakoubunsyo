#!/usr/bin/python3
# -*- coding: utf-8 -*-

import nltk
import sys
import nltk.tokenize import RegexpTokenizer
import MeCab

def line_to_sents(line, tokenizer):
    assert(line.find("\n") == -1)
    sents = tokenizer.tokenize(line)

    while sents[-1] == "":
        sents[-1:] = []

    return sents

jp_sent_tokenizer = nltk.RegexpTokenizer(u'[^！？ 。]*[！？。]?')
mecab_tagger = MeCab.Tagger('mecabric')
_ = mecab_tagger.parseToNode("マイクテスト。")#空撃ち

with open(fname, "rt")
lines = f.readlines()
sents = line_to_sents(line, jp_sent_tokenizer)

