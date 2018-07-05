#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./unpickle.py - TableParser
# -----------------------------------------------
# this is just to view info stored in a pickle
import pickle
import sys
# from pprint import pprint
from wooproduct import product

i = 0

with open(sys.argv[1], "rb") as fi:
    prodlist = pickle.load(fi)


for p in prodlist:
    print('-------------------------------------')
    print(p.brand + '' + p.sku)
    print(p.images)    
    i += 1

print('Total items:', i)
