#In[]:
import scrapy
from scrapy.crawler import CrawlerProcess
import time
#In[]
def timer(func):
    def inner_wrapper(*args, **kwargs):
        """
        Decorator to return time taken to run function
        """
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print('-' * 20)
        print(f"Finished {func.__name__!r} in {run_time:.8f} secs")
        return value
    return inner_wrapper

#In[]
"""Saves dictionary to outputresponse variable"""
outputresponse = {}

class WaterSpider(scrapy.Spider):
    name = 'water'
    
    def start_requests(self):
        """
        Returns requests from page 1 of openbeautyfacts for products containing water"""
        yield scrapy.Request("https://world.openbeautyfacts.org/ingredient/water")
        ## yield acts as return in scrapy spider

    def parse(self,response):
        """
        On each page runs through list of html elements/classes under the <ul> tag with class = 'products
        and retrieves barcode and title for products. Returns dictionary of  with key: value pair, barcode: name.
        """
        products = response.css('ul.products a')  
        ## list of items with <a> tag under the <ul> tag class ='products'
        ## list containes 20 items representing 20 <a> tags for each product on the page
        # 
        global outputresponse  ## creates global variable of empty dictionary in class
        for item in products:   ## creating dictionary of each key value pair on the page
            outputresponse_dict = {
                item.css('a::attr(href)').get().replace('/product/','').split('/')[0]: item.css('a::attr(title)').get()
            }
            outputresponse.update(outputresponse_dict)  ## updating to the global variable
            yield outputresponse_dict  ## return each dict
            

        for x in range(2,100):  ## runs through 100 pages on the website 
            yield(scrapy.Request(f"https://world.openbeautyfacts.org/ingredient/water/{x}", callback = self.parse))
@timer  ##timer decorator
def run_spider():
    """
    Calling the spider crawlerprocess
     """
    process = CrawlerProcess()

    process.crawl(WaterSpider)
    process.start()

run_spider()
#In[]:
print(outputresponse)
print(len(outputresponse))
#In[]
"""Saves dictionary to csv file """
class WaterSpider2(scrapy.Spider):
    name = 'water'
    
    def start_requests(self):
        yield scrapy.Request("https://world.openbeautyfacts.org/ingredient/water")

    def parse(self,response):
        products = response.css('ul.products a')
        for item in products:

            yield {
                'name': item.css('a::attr(title)').get(),
                'barcode': item.css('a::attr(href)').get().replace('/product/','').split('/')[0] 
            }
            

        for x in range(2,100):
            yield(scrapy.Request(f"https://world.openbeautyfacts.org/ingredient/water/{x}", callback = self.parse))


@timer
def run_spider2():
"""
Changes crawlerprocess settings so tha dictionary is saved to csv"""
    process = CrawlerProcess(settings = {
    'FEED_URI': 'water2.csv',
    'FEED_FORMAT': 'csv'
})
    #process = CrawlerProcess()

    process.crawl(WaterSpider2)
    process.start()

run_spider2()
# job = Job(WaterSpider)
# processor = Processor()
# data = processor.run(job)


#In[]:
print(outputresponse)
print(len(outputresponse)) #1802
# items scraped 1980
#In[]:
import pandas as pd
df = pd.read_csv('water2.csv')

df.head(20)
print(df.loc[df['barcode'] == '8711600285309'])
