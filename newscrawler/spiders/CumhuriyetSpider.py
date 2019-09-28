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
                item['author'] = response.xpath('//div[@class="publish-date"]/div[@class="left"]/span/a/text()').extract()[0]
                item['date'] = response.xpath('//div[@class="publish-date"]/div[@class="right"]/span/text()').extract()[0]
                item['title'] = ' '.join(response.xpath('//h1[@class="news-title"]/text()').extract())
                item['abstract'] = ' '.join(response.xpath('//div[@class="news-short"]/text()').extract())
                item['content'] = ' '.join(response.xpath('//div[@class="formatted news-content"]//p/text()').extract())
                # tags
            except Exception as e:
                logging.error(e)
        return item

