import requests
import lxml
from lxml import html
from lxml.html import parse
#from lxml import etree
import re
import pickle

class InfoYaMarket:
    
    def __init__(self, number):
        self.product_number = number

        
    main_url = 'https://market.yandex.ru'
    product = '/product'
    reviews = '/reviews'
    spec = '/spec'
    product_name = ''
    
    advantages_list = []
    disadvantages_list = []
    specs_dict = dict()


    
    #from http://foxtools.ru/Proxy; if proxies not works, need to update
    proxies = {
        "HTTP": "HTTP://146.185.252.133:8888",
        "HTTP": "HTTP://77.241.17.112:3128",
        "HTTPS": "HTTPS://103.247.12.70:80",
        "HTTP": "HTTP://201.242.252.99:8080",
        "HTTPS": "HTTPS://103.247.12.70:80",
        "HTTP": "HTTP://189.36.20.37:80",
        "HTTPS": "HTTPS://84.42.3.3:3128",
        "HTTP": "HTTP://109.230.252.44:80",
        "HTTP": "HTTP://109.172.51.147:80",
        "HTTPS": "HTTPS://159.255.163.228:80",
    } 
    def get_product_name(self):
        return self.product_name

    def get_advantages_list(self):
        return self.advantages_list

    def get_disadvantages_list(self):
        return self.disadvantages_list

    def get_specs_dict(self):
        return self.specs_dict
    #------------------------------------------------------------------------------------------------
    def parse_product_name(self):
        page_url = self.main_url+self.product+'/'+self.product_number
        #regex pattern
        page_url_pattern = re.compile("http.:\/\/market\.yandex\.ru\/product\/\d+.*")

        if page_url_pattern.match(page_url):
            #print 'Url:',  page_url
            #Getting page
            response = requests.get(page_url, proxies = self.proxies)
            page = html.fromstring(response.text)
            #Take out the product name
            self.product_name = page.cssselect('div.headline__header h1')[0].get('title').rstrip().lstrip()
            #print 'Product name:',  self.product_name
        else:
            print 'Url ',  page_url,' is not correct.'
        #return self.product_name
    #------------------------------------------------------------------------------------------------
    def parse_advantages_list(self):
        page_url = self.main_url+self.product+'/'+self.product_number+self.reviews
        
        #regex pattern
        page_url_pattern = re.compile("http.:\/\/market\.yandex\.ru\/product\/\d+\/reviews.*")

        if page_url_pattern.match(page_url):
            #print 'Url:',  page_url

            #Getting page
            response = requests.get(page_url, proxies = self.proxies)
            page = html.fromstring(response.text)

            product_facts_categories = page.cssselect('div.product-facts h2.product-facts__title')
            product_facts_block_list = page.cssselect('div.product-facts ul.product-facts__block')
            facts = product_facts_block_list[0].cssselect('li.product-facts__item')
            for fact in facts:
                #print fact.text
                if not fact.text in self.advantages_list:
                    self.advantages_list.append(fact.text)

        else:
            print 'Url ',  page_url,' is not correct.'

        #return self.advantages_list
    #------------------------------------------------------------------------------------------------
    def parse_disadvantages_list(self):
        page_url = self.main_url+self.product+'/'+self.product_number+self.reviews
        
        #regex pattern
        page_url_pattern = re.compile("http.:\/\/market\.yandex\.ru\/product\/\d+\/reviews.*")

        if page_url_pattern.match(page_url):
            #print 'Url:',  page_url

            #Getting page
            response = requests.get(page_url, proxies = self.proxies)
            page = html.fromstring(response.text)

            product_facts_categories = page.cssselect('div.product-facts h2.product-facts__title')
            product_facts_block_list = page.cssselect('div.product-facts ul.product-facts__block')
            facts = product_facts_block_list[1].cssselect('li.product-facts__item')
            for fact in facts:
                #print fact.text
                if not fact.text in self.disadvantages_list:
                    self.disadvantages_list.append(fact.text)

        else:
            print 'Url ',  page_url,' is not correct.'
        #return self.disadvantages_list
    #------------------------------------------------------------------------------------------------
    def parse_specs_dict(self):
        page_url = self.main_url+self.product+'/'+self.product_number+self.spec

        #regex pattern
        page_url_pattern = re.compile("http.:\/\/market\.yandex\.ru\/product\/\d+\/spec.*") 

        if page_url_pattern.match(page_url):
            #print 'Url:',  page_url
            #specs_dict['page_url_spec'] = page_url

            #Getting page
            response = requests.get(page_url, proxies = self.proxies)
            page = html.fromstring(response.text)

            #take out the list of categories.
            product_facts_categories = page.cssselect('div.product-spec-wrap__body h2')
            #take out the blocks with a list of characteristics
            product_facts_block_list = page.cssselect('div.product-spec-wrap__body')

            if (len(product_facts_categories) <= len(product_facts_block_list)):
                #In cycle parse every fact in relation to the category
                i = 0
                for category in product_facts_categories:
                    #print category.text

                    #specs_dict[category.text]

                    spec_names = product_facts_block_list[i].cssselect('dl.product-spec span.product-spec__name-inner')
                    spec_values = product_facts_block_list[i].cssselect('dl.product-spec span.product-spec__value-inner')

                    if (len(spec_names) == len(spec_values)):
                        tmp_dict = dict()
                        j = 0
                        for name in spec_names:
                            #print '  ', j, ' ', name.text, '--\t--\t-->', spec_values[j].text
                            tmp_dict[name.text] = spec_values[j].text
                            j = j + 1

                        self.specs_dict[category.text] = tmp_dict

                    else:
                        print 'Error 505.', ' ', 'len(spec_names) =, ', len(spec_names), '; len(spec_values) = ', len(spec_values)
                    i = i + 1
            else:
                print 'Error 121', ' ', 'len(product_facts_categories) =, ', len(product_facts_categories), '; len(product_facts_block_list) = ', len(product_facts_block_list)

        else:
            print 'Url ',  page_url,' is not correct.'
        #return self.specs_dict
    #------------------------------------------------------------------------------------------------
    def parse_all_info(self):
        page_url = self.main_url+self.product+'/'+self.product_number+self.reviews
        
        #regex pattern
        page_url_pattern = re.compile("http.:\/\/market\.yandex\.ru\/product\/\d+\/reviews.*")

        if page_url_pattern.match(page_url):
            #print 'Url:',  page_url

            #Getting page
            response = requests.get(page_url, proxies = self.proxies)
            page = html.fromstring(response.text)
            
            #Take out the product name
            self.product_name = page.cssselect('div.headline__header h1')[0].get('title').rstrip().lstrip()
            #print 'Product name:',  self.product_name
            
            product_facts_categories = page.cssselect('div.product-facts h2.product-facts__title')
            product_facts_block_list = page.cssselect('div.product-facts ul.product-facts__block')
            
            #take out the advantages
            #print 'advantages'
            facts = product_facts_block_list[0].cssselect('li.product-facts__item')
            for fact in facts:
                #print '\t', fact.text
                if not fact.text in self.disadvantages_list:
                    self.disadvantages_list.append(fact.text)
            
            #take out the disadvantages
            #print 'disadvantages'
            facts = product_facts_block_list[1].cssselect('li.product-facts__item')
            for fact in facts:
                #print '\t', fact.text
                if not fact.text in self.disadvantages_list:
                    self.disadvantages_list.append(fact.text)
        else:
            print 'Url ',  page_url,' is not correct.'
        
        #Next, we take out the characteristics, by calling the function
        #return self.specs_dict
    #------------------------------------------------------------------------------------------------
#end of class InfoYaMarket
'''
number = '11028554'
tmp = InfoYaMarket(number) # , 1632006,6219323, 10624078, 9281443, 10495456, 10707535, 12259333, 12772728, 11028554, 12466715, 12260784
tmp.parse_advantages_list()
tmp.parse_disadvantages_list()
tmp.parse_specs_dict()
tmp.parse_product_name()
#tmp.get_all_info()

with open(number+'.pickle', 'wb') as fout:
    pickle.dump(tmp,fout, pickle.HIGHEST_PROTOCOL)
'''