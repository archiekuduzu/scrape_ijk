#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./product.py - TableParser


class product(object):
    # I changed this so the object will only spawn with the default
    # values we will manually assign the data to the object using
    # methods rather than trying to do it in the init.
    # We may add some stuff like name and maybe
    # other stuff if it seems like a good idea
    def __init__(self):
        self.title = ''
        self.name = ''
        self.brand = "brand"
        self.pid = "0000"
        self.post_date = "01/01/2018 8:00"
        self.post_content = ''
        self.sku = ''
        self.regular_price = 0
        self.sale_price = ''
        self.featured = "no"
        self.sale_date_from = ''
        self.sale_date_to = ''
        self.weight = 1
        self.length = 30
        self.width = 30
        self.height = 30
        self.upsell_ids = ''
        self.crosssell_ids = ''
        self.images = ''
        self.categories = "Uncategorized"
        self.attribute_ijk = "http://projectbkl.com/"
        self.ijk_html = "<html></html>"
        self.menu_order = 0
        self.post_author = 1
        self.comment_status = ''
        self.post_status = "publish"
        self.tax_class = ''
        self.visibility = "visible"
        self.stock_status = "instock"
        self.backorders = "no"
        self.manage_stock = "no"
        self.tax_status = "taxable"
        self.downloadable_files = ""
        self.tax_product_type = "simple"
        self.tax_product_visibility = ''
        self.tax_product_tags = ''
        self.attribute_data = "0|0|0"
