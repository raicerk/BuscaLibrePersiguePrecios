# -*- coding: utf-8 -*-

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import logging


class scraping():
    
    price = 0
    name = ""
    author=""
    url = ""

    def __init__(self):
        logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO,datefmt="%d-%m-%Y %H:%M:%S")

    def simple_get(self):
        try:
            with closing(get(self.url, stream=True)) as resp:
                if self.is_good_response(resp):
                    return resp.content
                else:
                    return None
        except (Exception, RequestException) as e:
            logging.info('Error during requests to {0} : {1}'.format(url, str(e)))
            return None

    def is_good_response(self, resp):
        try:
            content_type = resp.headers['Content-Type'].lower()
            return (resp.status_code == 200 
                    and content_type is not None 
                    and content_type.find('html') > -1)
        except Exception as error:
            logging.info(error)

    def scrap(self):
        try:
            raw_html = self.simple_get()
            html = BeautifulSoup(raw_html, 'html.parser')
            divData = html.findAll("div", {"class" : "datos"})
            aData = ""
            for tag in divData:
                aData = tag.findAll("a", {"class": "font-color-bl link-underline"})
            resultAuthor = aData
            resultPrice = html.findAll("span", {"itemprop" : "price"})
            resultName = html.findAll("h1", {"itemprop" : "name"})
            self.price = int(resultPrice[0].text.replace("$ ", "").replace(".",""))
            self.name = resultName[0].text
            self.author = resultAuthor[0].text
            return ({
                "precio": self.price,
                "nombre": self.name,
                "autor": self.author
            })
        except Exception as error:
            logging.info(error)