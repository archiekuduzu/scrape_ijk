#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./run.py - TableParser
# -----------------------------------------------
# This program will merge pickles into the argv[1] provided
import sys
import pickle
#import pprint

alen = len(sys.argv)

i = 0

if alen >= 3:
    newprodlist = []

    for arg in sys.argv[2:]:
        with open(arg, "rb") as fi:
            prodlist = pickle.load(fi)

            for prod in prodlist:
                print("Added: " + prod.brand + " to " + prod.categories)
                newprodlist.append(prod)
                i += 1

    with open('./' + sys.argv[1], "wb") as fi:
        pickle.dump(newprodlist, fi)
    print("Done. File ./pickle/" + sys.argv[1], 'Created from', sys.argv[2:])
    print("Added", i, "items")
else:
    print('Usage: ./merge_pickle <outputfile> <inputfile1> <inputfile2>...')
