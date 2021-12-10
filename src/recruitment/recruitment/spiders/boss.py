import scrapy
import datetime
from recruitment import items


# TODO 获取python相关职位 职位 工资 经验 学历 工作地点 职位描述 公司(成立时间,法人,类型,注册资金)
class BossSpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['https://www.zhipin.com']
    start_urls = ['https://www.zhipin.com/']
    url = 'https://www.zhipin.com'
    page = 'https://www.zhipin.com/c100010000/?query=python&page={}'
    idx_bool = True

    def extract(self, response):
        item = items.RecruitmentItem()
        # 数据来源
        item['source'] = 'Boss'
        # 抓取时间
        item['utc_tim'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 职位
        item['position'] = response.xpath(
            '//*[@id="main"]/div[1]/div/div/div[2]/div[2]/h1/text()'
        ).extract_first()
        # 职位描述
        item['job_description'] = response.xpath(
            '//*[@id="main"]/div[1]/div/div/div[2]/div[2]/h1/text()'
        ).extract_first()
        # 工资
        item['wage'] = response.xpath(
            '//*[@id="main"]/div[1]/div/div/div[2]/div[2]/span/text()'
        ).extract_first()
        # 公司介绍
        item['company_introduction'] = response.xpath(
            '//*[@id="main"]/div[3]/div/div[2]/div[2]/div[2]/div/text()'
        ).extract_first()
        # 公司名
        item['cmpany_name'] = response.xpath(
            '//*[@id="main"]/div[3]/div/div[2]/div[2]/div[5]/div[1]/text()'
        ).extract_first()
        # 法人
        item['legl_person'] = response.xpath(
            '//*[@id="main"]/div[3]/div/div[2]/div[2]/div[5]/div[2]/li[1]/text()'
        ).extract_first()
        # 注册资金
        item['registered_capital'] = response.xpath(
            '//*[@id="main"]/div[3]/div/div[2]/div[2]/div[5]/div[2]/li[2]/text()'
        ).extract_first()
        # 成立时间
        item['founding_time'] = response.xpath(
            ' //*[@id="main"]/div[3]/div/div[2]/div[2]/div[5]/div[2]/li[3]/text()'
        ).extract_first()
        # 公司类型
        item['company_type'] = response.xpath(
            ' //*[@id="main"]/div[3]/div/div[2]/div[2]/div[5]/div[2]/li[4]/text()'
        ).extract_first()
        # 经营状态
        item['operating_state'] = response.xpath(
            '//*[@id="main"]/div[3]/div/div[2]/div[2]/div[5]/div[2]/li[5]/text()'
        ).extract_first()
        # 工作地点
        item['working_place'] = response.xpath(
            '//*[@id="main"]/div[3]/div/div[2]/div[2]/div[6]/div/div[1]/text()'
        ).extract_first()
        # 要求: 全职 1经验 2学历| 实习 1每周工作天数 2工作月数 3学历
        requirements = response.xpath(
            '//*[@id="main"]/div[1]/div/div/div[2]/p/text()').extract()
        if len(requirements) == 2:
            item['experience'] = requirements[0]
            item['eduction_background'] = requirements[1]
            item['type_of_work'] = '全职'
        else:
            item['a_few_months'] = requirements[0]
            item['a_few_days'] = requirements[1]
            item['education_background'] = requirements[2]
            item['type_of_work'] = '实习'
        yield item


# 全国数据 https://www.zhipin.com/c100010000/?query=python&page=1
# query 搜素关键字 page 页码

    def parse(self, response):
        page_idx = 1
        # 详情页
        # "/job_detail/369e23e877c41e311nF93dS0FVVR.html"
        a_list = response.xpath(
            '//*[@id="main"]//div[2]//li//div[1]/div[1]/div/div[1]/span[1]/a/@href'
        ).extract()
        print(
            response.xpath(
                '//*[@id="main"]/div/div[3]/div[3]/a[2]/@class').extract())
        state = response.xpath('//*[@id="main"]/div/div[2]/div[2]/a[2]/@class'
                               ).extract()[0] == 'cur'
        # 判断是否翻到底
        if a_list and state:
            self.idx_bool = False
        if self.idx_bool:
            for each in a_list:
                # 拼接详情页url
                details_page = self.url + each
                yield scrapy.Request(url=details_page, callback=self.extract)
            next_page = self.page.format(page_idx)
            # 翻页
            yield scrapy.Request(url=next_page, callback=self.parse)
