#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import pymorphy2
import YaMarket
import pickle
'''
product = YaMarket.InfoYaMarket('12259971')
advantages = product.get_advantages_list()
morph = pymorphy2.MorphAnalyzer()
p = morph.parse(u'стали')[0]
pp = product.get_specs_dict()
for i in pp.keys():
    print i

for j in pp['Экран']:
    print j

print pp['Экран']['Размер изображения']
'''
with open('12772728.pickle', 'rb') as fin:
    obj = pickle.load(fin)
print (type(obj))