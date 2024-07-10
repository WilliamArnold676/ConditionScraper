import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy import Request
import csv


#possible problems

#Possible anti scraping is begining implemented? It wouldn't let me go to the website after around 3 hours of usage
#but once I swapped vpn locations it was fine

# for making file into executable
# https://stackoverflow.com/questions/55331478/how-can-i-create-a-single-executable-file-in-windows-10-with-scrapy-and-pyinstal
# https://stackoverflow.com/questions/49085970/no-such-file-or-directory-error-using-pyinstaller-and-scrapy

# csv file stuff
# https://stackoverflow.com/questions/29943075/scrapy-pipeline-to-export-csv-file-in-the-right-format
# https://stackoverflow.com/questions/20753358/how-can-i-use-the-fields-to-export-attribute-in-baseitemexporter-to-order-my-scr

def authentication_failed(response):

    # or False if it succeeded.
    pass

class QuotesSpider(scrapy.Spider):

    name = "conditions"
    start_urls = ["https://www.petmd.com/dog/conditions",]



    def secondFunc(self, response):


        thingy = response.css("div.article_content_article_body__GQzms")

        #check right now only really works for none, the others are still basically getting printed
        check = [None, "Featured Image:", "WRITTEN BY", "Was this article helpful?", "PetMD's medications content was written and reviewed"]

        # texty = response.css("h1.article_title_article_title__98_zt")
        # title =  texty.css("h1.article_title_article_title__98_zt::text").getall()

        totalLine = ""
        for div in thingy:


            pageList = div.css("::text").getall()

            if pageList == None:
                continue

            # print(pageList)
            # break

            for value in pageList:
                if '\n' in value:
                    continue
                if value in check:
                    continue

                for char in value:
                    if char == '<':
                        break
                    else:

                        if char == "’":
                            totalLine += "'"
                        elif char == "“":
                            totalLine += '"'
                        elif char == "”":
                            totalLine += '"'
                        else:
                            totalLine += char

        #title[1]

        yield {
            "conditions": totalLine,
        }




    def parse(self, response):

        correctLinks = False
        i = 0
        lastFunc = ""
        for div in response.css("a"):
            i += 1
            print(i)



            next_page_url = div.css("a::attr(href)").get()
            url = response.urljoin(next_page_url)

            if url == "https://www.facebook.com/petMD/":
                break
            if correctLinks:
                #print(url)
                yield scrapy.Request(url, self.secondFunc)


            if url == "https://www.petmd.com/" and i > 90:
                correctLinks = True

            if i == 106:
                break




# process = CrawlerProcess(
#     settings={
#         "FEEDS": {
#             "conditions.csv": {"format": "csv"},
#         },
#     }
# )
#
# process.crawl(QuotesSpider)
# process.start()
#scrapy crawl conditions --loglevel=INFO -o links.csv
#746 total links we are currently scrapping from

