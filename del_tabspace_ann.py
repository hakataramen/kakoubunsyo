#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

dirpath = sys.argv[1]
if dirpath[-1] != "/": dirpath += "/"


for filename in os.listdir(dirpath):
    f = open(dirpath+filename, "r")
    with open("tr_"+filename, "w") as tr_f:
        for line in f.readlines():
            b=line.replace("\t"," ")
            tr_f.write(b)
