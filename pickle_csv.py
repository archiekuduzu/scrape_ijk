#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./run.py - TableParser
# -----------------------------------------------
import csv
import sys
import pickle
from wooproduct import product

for arg in sys.argv[1:]:
    with open(arg, "rb") as fi:
        prodlist = pickle.load(fi)

    outfile = arg.split('.', 1)[0]
    outfile = outfile + '.csv'

    print('Writing ' + outfile + '...')

    # write the csv - filename is argv[2]
    with open(outfile, 'w', newline='') as csvfile:
        fieldnames = [
            'post_title',
            'post_name',
            'ID',
            'post_excerpt',
            'post_content',
            'post_status',
            'menu_order',
            'post_date',
            'post_author',
            'comment_status',
            'sku',
            'stock',
            'regular_price',
            'sale_price',
            'weight',
            'length',
            'width',
            'height',
            'tax_class',
            'visibility',
            'stock_status',
            'backorders',
            'manage_stock',
            'tax_status',
            'upsell_ids',
            'crosssell_ids',
            'featured',
            'sale_price_dates_from',
            'sale_price_dates_to',
            'product_url',
            'button_text',
            'images',
            'tax:product_type',
            'tax:product_visibility',
            'tax:product_cat',
            'tax:product_tag',
            'tax:product_shipping_class',
            'attribute:ijk',
            'attribute_data:ijk',
            'attribute_default:ijk',
            'attribute:my thoughts',
            'attribute_data:my thoughts',
            'attribute_default:my thoughts'
                      ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for p in prodlist:
            writer.writerow({
                'post_title': p.brand + ', ' + p.title,
                'post_name': p.name,
                'ID': p.pid,
                'post_excerpt': p.post_date,
                'post_content': p.post_content,
                'post_status': 'publish',
                'menu_order': '0',
                'post_date': p.post_date,
                'post_author': 1,
                'comment_status': 'open',
                'sku': p.sku,
                'stock': '',
                'regular_price': p.regular_price,
                'sale_price': p.sale_price,
                'weight': p.weight,
                'length': p.length,
                'width': p.width,
                'height': p.height,
                'tax_class': '',
                'visibility': 'visible',
                'stock_status': 'instock',
                'backorders': 'no',
                'manage_stock': 'no',
                'tax_status': 'taxable',
                'upsell_ids': p.upsell_ids,
                'crosssell_ids': p.crosssell_ids,
                'featured': 'no',
                'sale_price_dates_from': '',
                'sale_price_dates_to': '',
                'product_url': '',
                'button_text': '',
                'images': p.images,
                'tax:product_type': 'simple',
                'tax:product_visibility': '',
                'tax:product_cat': p.categories,
                'tax:product_tag': '',
                'tax:product_shipping_class': '',
                'attribute:ijk': p.attribute_ijk,
                'attribute_data:ijk': '0|0|0',
                'attribute_default:ijk': '',
                'attribute:my thoughts': '',
                'attribute_data:my thoughts': '',
                'attribute_default:my thoughts': ''
            })
