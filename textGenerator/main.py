#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



__author__ = 'parkinmsu'

import pymorphy2
import YaMarket
import random

class TextGenerator:
    def __init__(self, morphy, advantages_list, disadvantages_list, features):
        self.morphy = morphy
        self.advantages_list = advantages_list
        self.disadvantages_list = disadvantages_list
        self.features_dict = features
        self.update = False
        self.not_ubdate_flag = False

    def phrase_ubdate(self, phrase):
        first_letter = phrase[0]
        if phrase.find('*') >= 0:
            not_ubdate_flag = True
            phrase = phrase[1:]

        if self.update and not not_ubdate_flag:
            phrase = ', '  + phrase
            if self.update:
                phrase = phrase + '. '
            self.update = False
        else:
            phrase = phrase.capitalize() + '. '
        return phrase

    def get_introductory_text(self):
        introductory_phrase_list = []
        with open('introductory.txt', 'r') as fin:
            for line in fin:
                introductory_phrase_list.append(line)
        phrase = introductory_phrase_list[random.randint(0, len(introductory_phrase_list) - 1)]
        if (phrase.find('%product_name%')):
            phrase = phrase.replace('%product_name%', product.get_product_name())
        if (phrase.find('%day%')):
            day_morphy = morphy.parse('день')[0]
            day = random.randint(3, 25)
            replace_str = str(day)+' '+day_morphy.make_agree_with_number(day).word
            phrase = phrase.replace('%day%', replace_str)
        phrase = phrase + ' '
        return phrase

    def get_advantage_text(self, advantage):
        phrase_list = []
        phrase = ''
        if advantage == 'Камера':
            with open('pos/Camera_pos.txt', 'r') as fin:
                for line in fin:
                    phrase_list.append(line)
            phrase = phrase_list[random.randint(0, len(phrase_list) - 1)]
            if (phrase.find('%camera_pixels%')):
                camera_pixels_str = features['Мультимедийные возможности']['Фотокамера']
                camera_pixels = int(camera_pixels_str[:camera_pixels_str.find(' ')])
                camera_pixels_morphy = morphy.parse('мегапиксель')[0]
                phrase = phrase.replace('%camera_pixels%', str(camera_pixels) + ' ' + camera_pixels_morphy.make_agree_with_number(camera_pixels).word)
            phrase = self.phrase_ubdate(phrase)
        if advantage == 'Дизайн':
            with open('pos/Design_pos.txt', 'r') as fin:
                for line in fin:
                    phrase_list.append(line)
            phrase = phrase_list[random.randint(0, len(phrase_list) - 1)]
            if (phrase.find('%from_to%')):
                for_arr = ['сын', 'жена', 'дочь', 'любимая', 'девушка', 'ребёнок']
                to_morph = morphy.parse(for_arr[random.randint(0, len(for_arr) - 1)])[0]
                phrase = phrase.replace('%from_to%', to_morph.inflect({'gent'}).word)
            phrase = self.phrase_ubdate(phrase)
        if advantage == 'Экран':
            with open('pos/Screen_pos.txt', 'r') as fin:
                for line in fin:
                    phrase_list.append(line)
            phrase = phrase_list[random.randint(0, len(phrase_list) - 1)]
            if (phrase.find('%screen_resolution%')):
                phrase = phrase.replace('%screen_resolution%', features['Экран']['Размер изображения'])
            phrase = self.phrase_ubdate(phrase)
        if advantage == 'Скорость':
            with open('pos/Speed_pos.txt', 'r') as fin:
                for line in fin:
                    phrase_list.append(line)
            phrase = phrase_list[random.randint(0, len(phrase_list) - 1)]
            if (phrase.find('%OS%')):
                phrase = phrase.replace('%OS%', features['Общие характеристики']['Операционная система'])

            if (phrase.find('%RAM%')):
                phrase = phrase.replace('%RAM%', features['Память и процессор']['Объем оперативной памяти'])
            phrase = self.phrase_ubdate(phrase)
        if advantage == 'Аккумуятор':
            with open('pos/Battery_pos.txt', 'r') as fin:
                for line in fin:
                    phrase_list.append(line)
            phrase = phrase_list[random.randint(0, len(phrase_list) - 1)]
            if (phrase.find('%battery_time%')):
                hour_morphy = morphy.parse('час')[0]
                hour = random.randint(12, 48)
                phrase = phrase.replace('%battery_time%', str(hour) + ' ' + hour_morphy.make_agree_with_number(hour).word)
            phrase = self.phrase_ubdate(phrase)
        return phrase

    def get_disadvantage_text(self, disadvantage):
        phrase_list = []
        phrase = ''
        if disadvantage == 'Аккумулятор':
            with open('neg/Battery_neg.txt', 'r') as fin:
                for line in fin:
                    phrase_list.append(line)
            phrase = phrase_list[random.randint(0, len(phrase_list) - 1)]
            if (phrase.find('%battery_time%')):
                hour_morphy = morphy.parse('час')[0]
                hour = random.randint(6, 16)
                phrase = phrase.replace('%battery_time%', str(hour) + ' ' + hour_morphy.make_agree_with_number(hour).word)
            phrase = self.phrase_ubdate(phrase)
        if disadvantage == 'Цена':
            with open('neg/Price_neg.txt', 'r') as fin:
                for line in fin:
                    phrase_list.append(line)
            phrase = phrase_list[random.randint(0, len(phrase_list) - 1)]
            phrase = self.phrase_ubdate(phrase)
        return phrase

    def get_concluding_text(self):
        phrase_list = []
        phrase = ''
        with open('concluding.txt', 'r') as fin:
            for line in fin:
                phrase_list.append(line)

        phrase = phrase_list[random.randint(0, len(phrase_list) - 1)]
        if (phrase.find('%disadvantage_count%')):
            disadvantages_count = len(self.disadvantages_list)
            disadvantages_count_morphy = morphy.parse('недостаток')[0]
            phrase = phrase.replace('%disadvantage_count%', str(disadvantages_count) + ' ' + disadvantages_count_morphy.make_agree_with_number(disadvantages_count).word)
        return '\n' + phrase




product = YaMarket.InfoYaMarket('12259971')
product.advantages_list = ['Экран', 'Камера','Дизайн', 'Скорость']
product.disadvantages_list = ['Конструкция', 'Аккумулятор', 'Цена', 'Надежность']
product.product_name = 'Samsung Galaxy S6 32GB'
product.specs_dict = {'Общие характеристики':{'Операционная система':'Android 5.0'}, 'Экран':{'Диагональ':'5.1 дюйм.','Размер изображения':'2560x1440'}, 'Питание':{'Емкость аккумулятора':'2600мА*ч'}, 'Мультимедийные возможности':{'Фотокамера':'16 млн пикс.,светодиодная вспышка'}, 'Память и процессор':{'Объем оперативной памяти':'3 Гб'}}

'''
product = YaMarket.InfoYaMarket('9281443') # , 1632006,6219323, 10624078, 9281443, 10495456, 10707535, 12259333, 12772728, 11028554, 12466715, 12260784
product.parse_advantages_list()
product.parse_disadvantages_list()
product.parse_specs_dict()
product.parse_product_name()
'''
morphy = pymorphy2.MorphAnalyzer()

advantages = product.get_advantages_list()
disadvantages = product.get_disadvantages_list()
features = product.get_specs_dict()

generator = TextGenerator(morphy,advantages, disadvantages, features)

text = ''
text += generator.get_introductory_text()
for item in advantages:
    text += generator.get_advantage_text(item)
for item in disadvantages:
    text += generator.get_disadvantage_text(item)

text += generator.get_concluding_text()

with open('result.txt', 'w') as fout:
    fout.write(text)

'''
print 'Positive'
for i in advantages:
    print i
print 'Negative'
for i in disadvantages:
    print i
'''