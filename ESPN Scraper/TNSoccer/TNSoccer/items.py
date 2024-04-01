# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TnsoccerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #-------Main Team Stats-------#
    team       = scrapy.Field()
    conference = scrapy.Field()
    win_lose   = scrapy.Field()
    web_address = scrapy.Field()

    #-----Individual Top Player Stats of Top 50 Teams-----#
    
    leading_stat_cat = scrapy.Field()
    leading_athletes = scrapy.Field()
    leading_stat_num = scrapy.Field()

    sport_category   = scrapy.Field()
    pass
