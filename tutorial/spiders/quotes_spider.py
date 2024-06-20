from bs4 import BeautifulSoup
import scrapy
from scrapy import signals
from scrapy import Request
from scrapy.exporters import CsvItemExporter
from scrapy.linkextractors import LinkExtractor
from scrapy.mail import MailSender
from itemadapter import ItemAdapter
import csv


#possible problems

#Possible anti scraping is begining implemented? It wouldn't let me go to the website after around 3 hours of usage
#but once I swapped vpn locations it was fine

#The fastgpt website doesn't recognize the websites ' and instead replaces it with "b " (looks more like a box
#on the website, don't know if it'll cause problems since ai might be smart enough to still glean enough but idk

#each index is a paragraph, neatness wise not the best but could be worse

#making it into an executable seems to be hard but doable https://stackoverflow.com/questions/55331478/how-can-i-create-a-single-executable-file-in-windows-10-with-scrapy-and-pyinstal

#scrapy crawl conditions
#scrapy shell 'https://quotes.toscrape.com/page/1/'

def authentication_failed(response):

    # or False if it succeeded.
    pass

    #https://stackoverflow.com/questions/20753358/how-can-i-use-the-fields-to-export-attribute-in-baseitemexporter-to-order-my-scr
# class CSVPipeline(object):
#
#   def __init__(self):
#     self.files = {}
#
#   def from_crawler(cls, crawler):
#     pipeline = cls()
#     crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
#     crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
#     return pipeline
#
#   def spider_opened(self, spider):
#     file = open('%conditions.csv' % spider.name, 'w+b')
#     self.files[spider] = file
#     self.exporter = CsvItemExporter(file)
#     self.exporter.fields_to_export = ["index", "conditions"]
#     self.exporter.start_exporting()
#
#   def spider_closed(self, spider):
#     self.exporter.finish_exporting()
#     file = self.files.pop(spider)
#     file.close()
#
#   def process_item(self, item, spider):
#     self.exporter.export_item(item)
#     return item

class QuotesSpider(scrapy.Spider):

    name = "conditions"
    start_urls = ["https://www.petmd.com/dog/conditions",]


    def secondFunc(self, response):

        thingy = response.css("p")

        #check right now only really works for none, the others are still basically getting printed
        check = [None, "Featured Image:", "WRITTEN BY", "Was this article helpful?"]

        for div in thingy:
            totalLine = ""
            text = div.css("p::text").get()
            # text2 = div.css("a::text").getall()
            # text3 = div.css("p::text").getall()

            test = div.getall()
            final = test[0].split('>')

            for value in final:

                for char in value:
                    if char == '<':
                        break
                    else:
                        totalLine += char
            totalLine += '\n'

            if totalLine not in check:
                yield {
                    "text": totalLine,
                }
                # print(totalLine)

            else:
                continue

        #file = CsvItemExporter("C:\Users\William\Documents",)
        # yield {
        #     "text": totalLine,
        # }

    def parse(self, response):

        correctLinks = False
        i = 0
        for div in response.css("a"):
            i += 1
            #print(i)

#current problem was that if a new link was added it doesn't get incorperated


            next_page_url = div.css("a::attr(href)").get()
            url = response.urljoin(next_page_url)

            if url == "https://www.facebook.com/petMD/":
                break

            if correctLinks:
                print(url)
                yield scrapy.Request(url, self.secondFunc)

            # if i == 100:
            #     break

            if url == "https://www.petmd.com/" and i > 90:
                correctLinks = True

#scrapy crawl conditions --loglevel=INFO -o links.csv
#746 total links we are currently scrapping from

