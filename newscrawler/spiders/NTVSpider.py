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
                item['topic'] = response.xpath('//article/header/a/text()').extract()[1].replace("\r", "")
                item['source'] = response.xpath('//article/header/p[@class="source"]/span/text()').extract()[0]
                # item['author'] = response.xpath('//div[@class="publish-date"]/div[@class="left"]/span/a/text()').extract()[0]#
                item['date'] = response.xpath('//article/header/time/span[@class="first-publish"]/span[@class="desktop-only"]/text()').extract()[0]
                item['title'] = ' '.join(response.xpath('//article/header/div/h1/text()').extract())
                item['abstract'] = ' '.join(response.xpath('//article/h2/text()').extract())
                item['content'] = ' '.join(response.xpath('//article/div[@class="content article-body"]//p/text()').extract())
                item['tags'] = response.xpath('//article/section[@class="tags"]/ul/li/a/text()').getall()
            except Exception as e:
                logging.error(e)
        return item

