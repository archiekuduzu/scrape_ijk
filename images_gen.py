#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./images_gen.py - TableParser

# add images to the products that have not got them.
import urllib.request
import urllib.error
import urllib.parse
import sys
from bs4 import BeautifulSoup
from wooproduct import product
from ijk_product_grab import ijk_get_image_url

import pickle

fn = 'images_gen.py'

with open(sys.argv[1], "rb") as fi:
    prodlist = pickle.load(fi)

    for prod in prodlist:
        url = ijk_get_image_url(prod)
        page = urllib.request.urlopen(url)
        print(fn, "page = urllib.request.urlopen(url):", url)
        html_string = page.read().decode('utf-8', 'ignore')
        soup = BeautifulSoup(html_string, 'lxml')
        src = ""
        for link in soup.find_all('img'):
            src = link.get('src')
        if src != '':
            src = src.replace(" ", "%20")
            print(fn, "ijk image url", src)
        # img = urllib.request.urlopen(src)
        pid = prod.attribute_ijk.rsplit('=', 1)[1]
        pcat = prod.attribute_ijk.split('=', 1)[1]
        pcat = pcat.split('&', 1)[0]

        # split at '.' then
        # use the part that comes after (the file ext)
        print('src', src)
        filetype = src.rsplit('.', 1)[1]
        filename = './' + pcat + '/' + pcat + '-' + pid + '.' + filetype
        # print(fn, "img:", img)
        print(fn, "pid:", pid)
        print(fn, "filetype:", filetype)
        prod.images = 'http://projectbkl.com/wp-content/uploads/' + pcat + '-' + pid + filetype
        print(prod.images)
