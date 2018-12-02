import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import re
from crawler.items import CrawlerItem,CommentItem

class MySpider(CrawlSpider):
    name = 'crawler'
    allowed_domains = ['reddit.com']
    start_urls = ['https://old.reddit.com/r/all/']

    rules = (
        Rule(LinkExtractor(allow=('https://old.reddit\.com/(r/.*/)?\?count=.*&after=.*',)), callback='parse_list', follow=True),
    )

    picture_type = re.compile(r'.*\.jpg$|.*\.png$|.*\.gifv$|.*\.jpeg$')

    def parse_start_url(self, response):
        return scrapy.Request(self.start_urls[0], callback=self.parse_list)

    def parse_list(self, response):
        self.log('Hi, this is an item page! %s' % response.url)
        lists = response.xpath('//div[re:match(@class," ?thing.*")] ')
        for list in lists:
            picture, err = self.analysis_list(list)
            if err is None:
                picture['href'] = "https://old.reddit.com" + picture['href']
                request = scrapy.Request(picture['href'], callback=self.parse_comment)
                request.meta['info'] = picture
                yield request
            else:
                print picture['href'], err
                continue

    def parse_comment(self, response):
        picture_href = response.xpath('//div[re:match(@class,"media-preview-content.*")]/a/@href').extract_first()
        if picture_href != None:
            response.meta['info']["url"] = picture_href
            response.meta['info']["type"] = picture_href.split(".")[-1]
            comments = response.xpath(
                '//div[@id="' + "siteTable_" + response.meta["info"]["id"] + '"]/div[re:match(@class," ?thing id-.*")]')
            if comments:
                parent = comments.xpath('@id').extract_first()
                parent_id = parent.split('_')[-1]
                get_comments = self.analysis_comment(response.meta["info"]['id'], response.meta["info"]['href'], parent_id, comments)
                i = 0
                while i < len(comments):
                    comment_item, num = get_comments.next()
                    i = i + 1
                    i = i - num
                    yield comment_item
            yield CrawlerItem(response.meta['info'])
        elif self.picture_type.match(response.meta['info']["url"]):
            response.meta['info']["type"] = response.meta['info']["url"].split(".")[-1]
            comments = response.xpath(
                '//div[@id="' + "siteTable_" + response.meta["info"]["id"] + '"]/div[re:match(@class," ?thing id-.*")]')
            if comments:
                parent = comments.xpath('@id').extract_first()
                parent_id = parent.split('_')[-1]
                get_comments = self.analysis_comment(response.meta["info"]['id'], response.meta["info"]['href'], parent_id, comments)
                i = 0
                while i < len(comments):
                    comment_item, num = get_comments.next()
                    i = i + 1
                    i = i - num
                    yield comment_item
            yield CrawlerItem(response.meta['info'])
        else:
            print response.url, " is not picture. data-url is ", response.meta['info']["url"]

    def analysis_list(self, list):
        err = None
        picture = dict()
        picture["title"] = list.xpath(
            'div[@class="entry unvoted"]/div[@class="top-matter"]/p[@class="title"]/a/text()').extract_first()
        picture["id"] = list.xpath('@data-fullname').extract_first()
        picture["author"] = list.xpath('@data-author').extract_first()
        picture["author_id"] = list.xpath('@data-author-fullname').extract_first()
        picture["subreddit"] = list.xpath('@data-subreddit').extract_first()
        picture["subreddit_id"] = list.xpath('@data-subreddit-fullname').extract_first()
        picture["subreddit_type"] = list.xpath('@data-subreddit-type').extract_first()
        picture["timestamp"] = list.xpath('@data-timestamp').extract_first()
        picture["url"] = list.xpath('@data-url').extract_first()
        picture["href"] = list.xpath('@data-permalink').extract_first()
        picture["domain"] = list.xpath('@data-domain').extract_first()
        picture["rank"] = list.xpath('@data-rank').extract_first()
        if picture["rank"] is None:
            picture["rank"] = 0
        else:
            picture["rank"] = int(picture["rank"])
        picture["comments_count"] = list.xpath('@data-comments-count').extract_first()
        if picture["comments_count"] is None:
            picture["comments_count"] = 0
        else:
            picture["comments_count"] = int(picture["comments_count"])
        picture["score"] = list.xpath('@data-score').extract_first()
        if picture["score"] is None:
            picture["score"] = 0
        else:
            picture["score"] = int(picture["score"])
        picture["likes"] = list.xpath(
            'div[@class="midcol unvoted"]/div[@class="score unvoted"]/@title').extract_first()
        if picture["likes"] is None:
            picture["likes"] = 0
        else:
            picture["likes"] = int(picture["likes"])
        return picture, err

    def analysis_comment(self, picture_id, href, parent_id, comments):
        for comment_info in comments:
            comment = dict()
            comment['id'] = picture_id
            comment['href'] = href
            comment['parent_id'] = parent_id
            comment['comment_id'] = comment_info.xpath('p[@class="parent"]/a/@name').extract_first()
            comment['author'] = comment_info.xpath('@data-author').extract_first()
            comment['author_id'] = comment_info.xpath('@data-author-fullname').extract_first()
            comment['timestamp'] = comment_info.xpath(
                'div[@class="entry unvoted"]/p[@class="tagline"]/time/@datetime').extract_first()
            comment['text'] = comment_info.xpath(
                'div[@class="entry unvoted"]/form[@class="usertext warn-on-unload"]/div/div[@class="md"]/p/text()').extract_first()
            comment['reply'] = comment_info.xpath('@data-replies').extract_first()
            if comment['reply'] is None:
                comment['reply'] = 0
            else:
                comment['reply'] = int(comment['reply'])
            comment['likes'] = comment_info.xpath(
                'div[@class="entry unvoted"]/p[@class="tagline"]/span[@class="score unvoted"]/@title').extract_first()
            if comment['likes'] is None:
                comment['likes'] = 0
            else:
                comment['likes'] = int(comment['likes'])
            comments_selector = comment_info.xpath(
                'div[@class="child"]/div[@id="' + "siteTable_" + parent_id + '"]/div[re:match(@class," ?thing id-.*")]')
            if comments_selector:
                parent = comments_selector.xpath('@id').extract_first()
                parent_id = parent.split('_')[-1]
                get_comments = self.parse_comments(picture_id, href, parent_id, comments_selector)
                i = 0
                while i < len(comments_selector):
                    comment_item, num = get_comments.next()
                    i = i + 1
                    i = i - num
                    yield comment_item, 1
            yield CommentItem(comment), 0


