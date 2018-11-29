import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import re
from crawler.items import CrawlerItem

class MySpider(CrawlSpider):
    name = 'crawler'
    allowed_domains = ['reddit.com']
    start_urls = ['https://old.reddit.com/r/all/']

    rules = (
        Rule(LinkExtractor(allow=('https://old.reddit\.com/(r/.*/)?\?count=.*&after=.*',)), callback='parse_list', follow=True),
    )

    def parse_start_url(self, response):
        return scrapy.Request(self.start_urls[0], callback=self.parse_list)

    def analysis(self, list):
        picture = dict()
        picture["rank"] = list.xpath('span[@class="rank"]/text()').extract_first()
        picture["likes"] = list.xpath(
            'div[@class="midcol unvoted"]/div[@class="score likes"]/text()').extract_first()
        picture["dislikes"] = list.xpath(
            'div[@class="midcol unvoted"]/div[@class="score dislikes"]/text()').extract_first()
        picture["unvoted"] = list.xpath(
            'div[@class="midcol unvoted"]/div[@class="score unvoted"]/text()').extract_first()

        info = list.xpath('div[@class="entry unvoted"]/div[@class="top-matter"]')
        picture["title"] = info.xpath('p[@class="title"]/a/text()').extract_first()
        picture["timestamp"] = info.xpath('p[@class="tagline "]/time/@datetime').extract_first()
        picture["author"] = info.xpath('p[@class="tagline "]/a[1]/text()').extract_first()
        picture["category"] = info.xpath('p[@class="tagline "]/a[2]/text()').extract_first()
        picture["comments"] = info.xpath(
            'ul[@class="flat-list buttons"]/li[@class="first"]/a/text()').extract_first()
        href = info.xpath('p[@class="title"]/a/@href').extract_first()
        return picture, href

    def parse_list(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        inside_website = re.compile(r'/r/.*')
        jpg_picture = re.compile(r'.*\.jpg$')
        gifv_picture = re.compile(r'.*\.gifv')
        lists = response.xpath('//div[re:match(@class," thing.*")] ')
        for list in lists:
            picture, href = self.analysis(list)
            if inside_website.match(href):
                href = "https://old.reddit.com" + href
                # self.get_info(href)
                request = scrapy.Request(href, callback=self.download)
                request.meta['info'] = picture
                yield request
            elif jpg_picture.match(href):
                picture["type"] = "jpg"
                picture["url"] = href
                yield CrawlerItem(picture)
            elif gifv_picture.match(href):
                picture["type"] = "gifv"
                picture["url"] = href
                yield CrawlerItem(picture)
            else:
                print href, " is External website"
                continue

    def download(self, response):
        picture_href = response.xpath('//div[re:match(@class,"media-preview-content.*")]/a/@href').extract_first()
        if picture_href != None:
            response.meta['info']["url"] = picture_href
            response.meta['info']["type"] = "jpg"
            yield CrawlerItem(response.meta['info'])
        else:
            print response.url," is not picture"