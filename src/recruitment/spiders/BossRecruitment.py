import scrapy


class BossrecruitmentSpider(scrapy.Spider):
    name = 'BossRecruitment'
    allowed_domains = ['www.zhipin.com']
    start_urls = ['http://www.zhipin.com/']

    def parse(self, response):
        pass
