# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RecruitmentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source = scrapy.Field()
    utc_time = scrapy.Field()
    position = scrapy.Field()
    job_description = scrapy.Field()
    wage = scrapy.Field()
    company_introduction = scrapy.Field()
    company_name = scrapy.Field()
    legal_person = scrapy.Field()
    registered_capital = scrapy.Field()
    founding_time = scrapy.Field()
    company_type = scrapy.Field()
    operating_state = scrapy.Field()
    working_place = scrapy.Field()
    experience = scrapy.Field()
    education_background = scrapy.Field()
    type_of_work = scrapy.Field()
    a_few_months = scrapy.Field()
    a_few_days = scrapy.Field()
