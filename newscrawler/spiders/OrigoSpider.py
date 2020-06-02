import scrapy, logging
from newscrawler.items import NewsItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class OrigoSpider(CrawlSpider):

    name = "origo"
    allowed_domains = ["origo.hu"]
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
        urls = ['https://www.origo.hu/index.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_item(self, response):
        item = NewsItem()
        if response.xpath('//div[@class="article-lead"]') not in ['',None,[]]:
            try:
                url = str(response.url)
                item['url'] = url
                item['topic'] = self.get_topic(response)
                item['source'] = self.get_source(response)
                item['author'] = self.get_author(response)
                item['date'] = self.get_date(response)
                item['title'] = self.get_title(response)
                item['abstract'] = self.get_abstract(response)
                item['content'] = self.get_content(response)
                item['tags'] = self.get_tags(response)
            except Exception as e:
                logging.error(e)
        return item


    def get_author(self, response):
        result = None
        try:
            result =  response.xpath('//span[@class="article-author"]/text()').extract()[0]
            return result
        except Exception as e:
            logging.error("Could not get author from URI: " + response.url)
        return result

    def get_tags(self, response):
        result = None
        try:
            result = response.xpath('//div[@class="article-tags"]/a/text()').extract()
            return result
        except Exception as e:
            logging.error("Could not get tags from URI: "+response.url)
        return result

    def get_content(self, response):
        result = None
        try:
            result = ' '.join(response.xpath('//div[@id="article-text"]/p//text()').extract())
            return result
        except Exception as e:
            logging.error("Could not get content from URI: "+response.url)
        return result

    def get_abstract(self, response):
        result = None
        try:
            result = ' '.join(response.xpath('//div[@class="article-lead"]//text()').extract() )
            return result
        except Exception as e:
            logging.error("Could not get abstract from URI: "+response.url)
        return result

    def get_title(self, response):
        result = None
        try:
            result = response.xpath('//header[@id="article-head"]/h1/text()').extract()[0]
            return result
        except Exception as e:
            logging.error("Could not get title from URI: "+response.url)
        return result

    def get_date(self, response):
        result = None
        try:
            result = response.xpath('//span[@id="article-date"]/text()').extract()[0]
            return result
        except Exception as e:
            logging.error("Could not get date from URI: "+response.url)
        return result

    def get_source(self, response):
        result = None
        try:
            url = str(response.url)
            return url.split("/")[2]
        except Exception as e:
            logging.error("Could not get source from URI: "+response.url)
        return result

    def get_topic(self, response):
        result = None
        try:
            url = str(response.url)
            return url.split("/")[3]
        except Exception as e:
            logging.error("Could not get topic from URI: "+response.url)
        return result
