import scrapy, logging
from newscrawler.items import NewsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy.crawler

class CumhuriyetSpider(CrawlSpider):
    name = "cumhuriyet"
    allowed_domains = ["cumhuriyet.com.tr"]
    rules = [
        Rule(
            LinkExtractor(
                canonicalize = True,
                unique = True
            ),
            follow = True,
            callback = "parse_item"
        )
    ]

    def start_requests(self):
        urls = ['http://cumhuriyet.com.tr']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_item(self, response):
        item = NewsItem()
        if response.xpath('//h1[@class="news-title"]/text()').extract() not in ['',None,[]]:
            try:
                url = str(response.url)
                topic = url[url.index('/haber')+7:]
                topic = topic[:topic.index('/')]
                item['url'] = url
                item['topic'] = topic
                item['source'] = url[url.index('www.')+4:url.index('.com')]
                item['author'] = self.get_author(response)
                item['date'] = self.get_date(response)
                item['title'] = self.get_title(response)
                item['abstract'] = self.get_abstract(response)
                item['content'] = self.get_content(response)
                # tags
            except Exception as e:
                logging.error(e)
        return item

    def get_author(self, response):
        result = None
        try:
            result = response.xpath('//div[@class="publish-date"]/div[@class="left"]/span/a/text()').extract()[0]
            return result
        except Exception as e:
            logging.error("Could not get author from URI: "+response.url)
        return result

    def get_content(self, response):
        result = None
        try:
            result = ' '.join(response.xpath('//div[@class="formatted news-content"]//p/text()').extract())
            return result
        except Exception as e:
            logging.error("Could not get content from URI: "+response.url)
        return result

    def get_abstract(self, response):
        result = None
        try:
            result = ' '.join(response.xpath('//div[@class="news-short"]/text()').extract())
            return result
        except Exception as e:
            logging.error("Could not get abstract from URI: "+response.url)
        return result

    def get_title(self, response):
        result = None
        try:
            result = ' '.join(response.xpath('//h1[@class="news-title"]/text()').extract())
            return result
        except Exception as e:
            logging.error("Could not get title from URI: "+response.url)
        return result

    def get_date(self, response):
        result = None
        try:
            result = response.xpath('//div[@class="publish-date"]/div[@class="right"]/span/text()').extract()[0]
            return result
        except Exception as e:
            logging.error("Could not get date from URI: "+response.url)
        return result
