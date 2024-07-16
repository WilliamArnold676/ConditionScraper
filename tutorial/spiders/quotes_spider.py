import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy import Request
import csv


#To Scrawl from the website type in scrapy crawl conditions into the terminal


class QuotesSpider(scrapy.Spider):

    #Name of the File
    name = "conditions"

    #Website to scrape from
    start_urls = ["https://www.petmd.com/dog/conditions",]

    def parse(self, response):

        # Scrapes provided link for more links

        correctLinks = False
        i = 0

        for div in response.css("a"):
            i += 1
            print(i)


            next_page_url = div.css("a::attr(href)").get()
            url = response.urljoin(next_page_url)

            if url == "https://www.facebook.com/petMD/":
                break

            if correctLinks:
                yield scrapy.Request(url, self.secondFunc)

            if url == "https://www.petmd.com/" and i > 90:
                correctLinks = True

            # if i == 106:
            #     break


    def secondFunc(self, response):

        # Scraping at article previous link lead to
        thingy = response.css("div.article_content_article_body__GQzms")

        # Additional needless words, when detected next article is checked
        check = ["Featured Image:", "WRITTEN BY", "Was this article helpful?",
                 "PetMD's medications content was written and reviewed", "\xa0"]

        # Title of the current article
        # texty = response.css("h1.article_title_article_title__98_zt")
        # title =  texty.css("h1.article_title_article_title__98_zt::text").getall()
        # title[1]

        breakBool = False

        totalLine = ""
        for div in thingy:

            pageList = div.css("::text").getall()

            if pageList == None:
                continue


            for value in pageList:
                if value is None:
                    continue

                if '\n' in value:
                    continue


                for word in check:
                    if word in value:
                        breakBool = True

                if breakBool:
                    break

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


        yield {
            "value ": totalLine+" ",
        }


# I used this to try and get an .exe version of the program working, did not work
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



