import scrapy


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['https://www.lagou.com']
    start_urls = [
        'https://www.lagou.com/wn/jobs?px=new&pn=1&kd=Python&city=%E5%85%A8%E5%9B%BD'
    ]
    kd = 'Python'
    city = '%E5%85%A8%E5%9B%BD'
    url = 'https://www.lagou.com/wn/jobs??px=new&pn={pn}kd={kd}&city={city}'.format(
        pn=1, kd=kd, city=city)

    def parse(self, response):
        response.follow()
