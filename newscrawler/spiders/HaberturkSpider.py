import scrapy, logging
from newscrawler.items import NewsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy.crawler


class HaberturkSpider(CrawlSpider):
    name = "haberturk"
    allowed_domains = ["haberturk.com"]
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
        urls = ['http://www.haberturk.com/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_item(self, response):
        item = NewsItem()
        if response.xpath('//h2[@class="spot-title"]/text()').extract() not in ['',None,[]]:
            try:
                url = str(response.url)
                item['url'] = str(response.url)
                item['topic'] = self.get_topic(response)
                item['source'] = url[url.index("www.")+4:url.index(".com")]
                item['author'] = self.get_author(response)
                item['date'] = self.get_date(response)
                item['title'] = self.get_title(response)
                item['abstract'] = self.get_abstract(response)
                item['content'] = self.get_content(response)
                item['tags'] = self.get_tags(response)
            except Exception as e:
                logging.error(e)
        return item


    def get_tags(self, response):
        result = None
        try:
            result = response.xpath('//div[@class="content-related"]/div[@class="widget widget-tag type1 mb-20"]/ul/li/a/text()').getall()
            return result
        except Exception as e:
            logging.error("Could not get tags from URI: " + response.url)
        return result


    def get_topic(self, response):
        result = None
        try:
            result = response.xpath('//div[@class="breadcrumb"]/span[2]/a/text()').extract()[0]
            return result
        except Exception as e:
            logging.error("Could not get topic from URI: " + response.url)
        return result

    def get_author(self, response):
        result = None
        try:
            result = response.xpath('//div[@class="source"]/span/text()').extract()[0]
            return result
        except Exception as e:
            logging.error("Could not get author from URI: "+response.url)
        return result

    def get_content(self, response):
        result = None
        try:
            result = ' '.join(response.xpath('//article[@class="content type1"]//p/text()').extract())
            return result
        except Exception as e:
            logging.error("Could not get content from URI: "+response.url)
        return result

    def get_abstract(self, response):
        result = None
        try:
            result = ''.join(response.xpath('//h2[@class="spot-title"]/text()').extract())
            return result
        except Exception as e:
            logging.error("Could not get abstract from URI: "+response.url)
        return result

    def get_title(self, response):
        result = None
        try:
            result = ' '.join(response.xpath('//h1[@class="title"]/text()').extract())
            return result
        except Exception as e:
            logging.error("Could not get title from URI: "+response.url)
        return result

    def get_date(self, response):
        result = None
        try:
            result = response.xpath('//span[@class="date"]/time/text()').extract()[0]
            return result
        except Exception as e:
            logging.error("Could not get date from URI: "+response.url)
        return result
