Overview:

This program is a python webscrapper designed specifically to scrap from pages full of links from Petmd. Specific examples of what pages
this works on includes dog diseases A-Z and pet medications. I created this program during my internship at the chinese medicine company 
111. While this program can certainly be retrofitted to work on other websites and can serve as an example, it will not function on its own
without adjustments. If you wish to learn more about scrapy I highly recommend reading their tutorial to begin with: 
https://docs.scrapy.org/en/latest/intro/tutorial.html

How to Use:

  1. Open the program in an IDE of your choosing
  2. Pull up the terminal
  3. In the terminal type in scrapy crawl conditions
In the folder directory a conditions.csv file will be generated with the result.

If you wish to put the result in a different file type that can also be done by instead typing 
scrapy crawl conditions --loglevel=INFO -o conditions.json if you wish to put it into a json. This will generate a conditions.json file in 
addition to the previous .csv fille. Scrapy only supports a set number of output formats 
(json, jsonlines, jsonl, jl, csv, xml, 'marshal', 'pickle') and to use those you must replace the .json in the command line with your 
respective type.

Unfinished tasks:

During my time working on this, I tried a number of smaller tasks, including implementing openai's assistent chat bot and making the 
program into a .exe executable. I did not have enough time to finish both, but you can find the remenants of both. The ai items can be
ai.py file and .exe items can be found at the bottom of the quotes_spider.py file. I'd also recommend you consult these links for
dependencies and such:
https://stackoverflow.com/questions/55331478/how-can-i-create-a-single-executable-file-in-windows-10-with-scrapy-and-pyinstal
https://stackoverflow.com/questions/49085970/no-such-file-or-directory-error-using-pyinstaller-and-scrapy
