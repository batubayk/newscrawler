import scrapy, logging
from newscrawler.items import NewsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class NTVSpider(CrawlSpider):

    name = "ntv"
    allowed_domains = ["ntv.com.tr"]
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
        urls = ['http://ntv.com.tr']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_item(self, response):
        item = NewsItem()
        if response.xpath('//article') not in ['',None,[]]:
            try:
                url = str(response.url)
                item['url'] = url
                item['topic'] = self.get_topic(response)
                item['source'] = self.get_source(response)
                # item['author'] = response.xpath('//div[@class="publish-date"]/div[@class="left"]/span/a/text()').extract()[0]#
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
            result = response.xpath('//article/section[@class="tags"]/ul/li/a/text()').getall()
            return result
        except Exception as e:
            logging.error("Could not get tags from URI: "+response.url)
        return result

    def get_content(self, response):
        result = None
        try:
            result = ' '.join(response.xpath('//article/div[@class="content article-body"]//p/text()').extract())
            return result
        except Exception as e:
            logging.error("Could not get content from URI: "+response.url)
        return result

    def get_abstract(self, response):
        result = None
        try:
            result = ' '.join(response.xpath('//article/h2/text()').extract())
            return result
        except Exception as e:
            logging.error("Could not get abstract from URI: "+response.url)
        return result

    def get_title(self, response):
        result = None
        try:
            result = ' '.join(response.xpath('//article/header/div/h1/text()').extract())
            return result
        except Exception as e:
            logging.error("Could not get title from URI: "+response.url)
        return result

    def get_date(self, response):
        result = None
        try:
            result = response.xpath('//article/header/time/span[@class="first-publish"]/span[@class="desktop-only"]/text()').extract()[0]
            return result
        except Exception as e:
            logging.error("Could not get date from URI: "+response.url)
        return result

    def get_source(self, response):
        result = None
        try:
            result = response.xpath('//article/header/p[@class="source"]/span/text()').extract()[0]
            return result
        except Exception as e:
            logging.error("Could not get source from URI: "+response.url)
        return result

    def get_topic(self, response):
        result = None
        try:
            result = response.xpath('//article/header/a/text()').extract()[1].replace("\r", "")
            return result
        except Exception as e:
            logging.error("Could not get topic from URI: "+response.url)
        return result
