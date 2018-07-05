#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./ijk_product_grab.py - TableParser
# -----------------------------------------------
import urllib.request
import urllib.error
import urllib.parse
import os
from bs4 import BeautifulSoup
import re
import sys
from pprint import pprint
from wooproduct import product
import pickle
from decimal import Decimal
# -----------------------------------------------;


def ijk_get_desc(html_string):
    # get ijk desctription
    # url = prod.attribute_ijk
    # page = urllib.request.urlopen(url)

    # html_string = page.read().decode('utf-8', 'ignore')

    html_string = re.sub(r'[^\x00-\x7f]+', '*', html_string)

    # this bit will cull most of the html code that is useless to us
    # split the string at the body text comment and go with the latter half
    html_string = html_string.split('<!-- body_text //-->', 1)[1]
    # split the text and go with the former half
    html_string = html_string.split('<!-- body_eof //-->', 1)[0]

    # split at <table width="100%"> and keep the latter half
    html_string = html_string.split('<table width="100%">', 1)[1]

    # split at <table border="0" cellspacing="0" cellpadding="2" align="right">
    # and keep the former half
    html_string = html_string.split(
        '<table border="0" cellspacing="0" cellpadding="2" align="right">',
        1)[0]

    # remove all line endings so we dont get extra white space
    html_string = re.sub('\n', '', html_string)
    # html_string = re.sub('<br>', '', html_string)

    return html_string
    # print(html_string)

    # file = open("output.html", "w")
    # file.write(html_string)
    # file.close()

    # print("Wrote to output.html")


def ijk_get_categories(html_string):
    # ijk_get_categories
    # should make this use html string
    # currently it downloads the page multiple times when it doesnt need to
    # this could slow down the site

    # page = urllib.request.urlopen(url)

    # html_string = page.read().decode('utf-8', 'ignore')

    soup = BeautifulSoup(html_string, 'lxml')

    cat = soup.find('td', {'class': 'headerNavigation'})
    cat = re.sub(r'[^\x00-\x7f]+', '>', cat.get_text())
    # cat = re.sub(r' ', '', cat)
    cat = cat[6:]
    cat = cat.rsplit('>', 1)[0]
    return cat


def ijk_get_image(prod):
    # ijk_get_image_file
    # take ijk url, download file with pid as name
    # -------------------------------------------------
    fn = "ijk_get_image(prod):"
    print(fn, prod)
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
        filetype = src.rsplit('.', 1)[1]
        filename = './img/' + pcat + '-' + pid + '.' + filetype
        # print(fn, "img:", img)
        print(fn, "pid:", pid)
        print(fn, "filetype:", filetype)
        prod.images = 'http://projectbkl.com/wp-content/uploads/' + pcat + '-' + pid + '.' + filetype
        '''
        req = urllib.request.Request(
            src,
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0'
                }
        )

        # pprint(vars(req))

        img = urllib.request.urlopen(req)

        # check if the os path exists (may not work on non unix os)
        if not os.path.exists('./img/'):
            # make the dir if it doesnt exist
            os.makedirs('./img/')

        localfile = open(filename, 'wb')
        localfile.write(img.read())
        localfile.close()

    else:
        print(fn, "ERROR: ijk image url was null")
        '''


def ijk_get_image_url(prod):
    # i declare this to make the output easier to read
    fn = "ijk_get_image_url(prod):"
    print(fn, prod)
    print(fn, prod.attribute_ijk)

    # get the first 29 characters and the last 6
    # this can definitely be improved but if it aint broke dont fix it
    start = prod.attribute_ijk[0:29]
    print(fn, 'start: ' + start)
    pid = prod.attribute_ijk[-6:]
    print(fn, 'pid: ' + pid)

    # combine the start popup image script and the pid to get the image url
    # its very likely that this can be improved somehow
    print(fn, "url", start + "popup_image.php?pID=" + pid)
    url = start + "popup_image.php?pID=" + pid

    # return the url
    return url


def ijk_parse_table(table):
    # ijk_parse_table - create a file with the name passed to output a csv
    # the table on ijk
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # this is the method that actually grabs the products from the site
    # declare this to make output easier to read
    fn = "ijk_parse_table(table):"

    prodlist = []

    # we get the table and then skip the first row (the headings)
    table_i = iter(table.find_all('tr'))
    next(table_i)

    # loop through all the rows in the table using the html tags
    for row in table_i:
        columns = row.find_all('td')
        # rows = []

        prod = product()
        print(fn, "---------- new product ------------")

        # get_text() from each column in the product table
        prod.attribute_ijk = columns[0].find_all('a')[0].get('href')

        page = urllib.request.urlopen(prod.attribute_ijk)

        prod.ijk_html = page.read().decode('utf-8', 'ignore')
        prod.ijk_html = re.sub(r'[^\x00-\x7f]+', ' ', prod.ijk_html)

        prod.title = columns[0].get_text()
        # use regex to remove badchars
        prod.title = re.sub(r'[^\x00-\x7f]+', ' ', prod.title)

        prod.brand = columns[1].get_text()
        prod.brand = re.sub(r'[^\x00-\x7f]+', ' ', prod.brand)

        prod.sku = columns[2].get_text()
        prod.sku = re.sub(r'[^\x00-\x7f]+', ' ', prod.sku)

        prod.stock = columns[5].get_text()
        prod.stock = re.sub(r'[^\x00-\x7f]+', ' ', prod.stock)

        price = columns[6].get_text()
        price = re.sub(r'[^\x00-\x7f]+', ' ', price)
        prod.regular_price = Decimal(re.sub(r'[^\d.]', '', price))

        prod.post_content = ijk_get_desc(prod.ijk_html)
        prod.post_content = re.sub(r'[^\x00-\x7f]+', ' ', prod.post_content)

        ijk_get_image(prod)
        prod.categories = ijk_get_categories(prod.ijk_html)

        # skip all zero priced items (usually special offers or other)
        if prod.regular_price > 0:
            prodlist.append(prod)
            pprint(vars(prod))
        else:
            print('Prod had no price, skipping...')

    # return the prodlist to the caller
    return prodlist


def get_table(url, val):
    # grab a table from the url with the provided criteria
    # - --- - - - - - -  - - -- - - - -- - - - - -- - - -
    fn = "get_table(url, val)"
    # print the url to confirm what was entered.
    print(fn, "Getting ", url)

    # use first arg to pull html and pass it to html_string
    page = urllib.request.urlopen(url)
    html_string = page.read().decode('utf-8', 'ignore')

    # html becomes a beautifulsoup lxml, super tasty
    soup = BeautifulSoup(html_string, 'lxml')
    print(soup.find('title'))

    # find the product listing table
    table = soup.find('table', {'class': val})
    return table


def ijk_process_table(url):
    # product grab
    # processes an ijk table into a list of products
    # -- - - - -- -- -- -- - -- - - -- - - - -- - -
    fn = "ijk_process_table(url)"
    # made a get_table function to make grabbing different tables easier
    print(fn)
    table = get_table(url, 'productListing')

    # we made this a function so its way cleaner. clean soup is good soup
    prodlist = ijk_parse_table(table)

    return prodlist


# main function
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # store the number of args
    alen = len(sys.argv)
    if alen == 2:
        # get the list of products
        prodlist = ijk_process_table(sys.argv[1])
        # get the pcat from the url
        pcat = sys.argv[1].split('=', 1)[1]
        pcat = pcat.split('&', 1)[0]
        # store the list as pcat.pkl
        with open('./pickle/' + pcat + ".pkl", "wb") as fi:
            pickle.dump(prodlist, fi)
    else:
        # show help if wrong args used
        print("Usage: ./run.py <url>")
# EOF
