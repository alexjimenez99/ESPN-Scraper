import scrapy
from ..items import TnsoccerItem

#------First Steps------
# GOAL: Crawl The Top 50 College Teams for Leading Offensive and Defensive Stats
# Databases
# 1. Main Database with Team and Rank
# 2. Database Where Each Team Has It's top Offensive and Defensive Team (consider Primary Key Denoatation MySQL)
# ---- Next Steps ------
# 1. Store Values in Database
# 2. Fiind more ways to crawl around the website, with checks to make sure it's looking at college basketball teams
# 3. Crawl Each Sports Category and Get Top Teams As well As Relevant Headling Stats

class TnsoccerSpider(scrapy.Spider):
    name = 'schools'
    start_urls = ['https://www.espn.com/mens-college-basketball/bpi']
    web_addresses = []
    counter = 0

    def __init__(self):
        self.web_addresses = []
        self.counter       = 0
#--------------------------------------
# Crawler Has Crawl Sports Working... See how we can generalize crawling on the sports webistes we pulled 28Nov2022
    def parse(self, response):
        item       = TnsoccerItem()

        team       = response.css('.team-names').css('::text')
        conference = response.css('.align-left+ td.align-left').css('::text')
        win_lose   = response.css('.align-left~ .align-left+ td').css('::text')
        sports     = response.css('#global-nav .sports .link-text')
        
        #-------------Pulling Web Address of Team Hyperlink-----#
        def get_link(self, links):
            for i in links:
                if 'id' in i.get() and 'story' not in i.get() and 'javascript' not in i.get():
                    TnsoccerSpider.web_addresses.append(i.get())

            return TnsoccerSpider.web_addresses

        web_address = get_link(self, response.css('a::attr(href)'))
        web_address = list(web_address[:-1])
        
        try: 
            for i in range(len(conference)):
                item['team']        = team[i].get()
                item['conference']  = conference[i].get()
                item['win_lose']    = win_lose[i].get()
                item['web_address'] = web_address[i]
                
                yield item
        except IndexError:
            print('Index Error Raised')
        for i in web_address:
            yield response.follow(i, callback = self.crawl_teams)

        sports = response.css('.espn-en li a::attr(href)')
        for i in sports:
            yield response.follow(i.get(), callback = self.crawl_sports)

# #----------------------------
        
    def crawl_teams(self, response):
        item = TnsoccerItem()
        leading_stat_cat      = response.css('.mb2::text')
        leading_stat_num      = response.css('.hs2::text')
        leading_athletes      = response.css('.Athlete__PlayerName::text')
        try:
            for i in range(len(leading_stat_cat)):
                item['leading_stat_cat']    = leading_stat_cat[i].get()
                item['leading_athletes']    = leading_athletes[i].get()
                item['leading_stat_num']    = leading_stat_num[i].get()

                yield item
        except IndexError:
            print(self.counter, 'what happened')
            self.counter += 1
      
    # LEFT OFF 30 Nov 2022 Trying To Crawl Xpath More efficiently at the bottom of the conditional statments
    def crawl_sports(self, response): 
        item = TnsoccerItem()
        # item['sport_category'] = response.css('li a::attr(href)').extract_first() 
        crawl_website = response.css('div a')
        keywords = ['snowboard', 'skateboard', 'surf', 'football']
        counter_iter = 0
        for i in crawl_website:
            crawl_individual = i.get()
            for sport in keywords:
                if sport in crawl_individual: # keep crawling and look for item 
                    try:
                        html_tags = ['p', 'div', 'a']
                        # more_crawling = i.css('*')
                        for element in html_tags:
                            more_crawling = i.css(element)
                            print(more_crawling)
                            more_crawling = more_crawling.xpath('//*')
                            counter_iter += 1
                            if sport in more_crawling: # This loop isn't working
                                item['sport_category'] = element.get()
                                yield item
                            else:
                                pass
                    except Error as err:
                        print(err)
                    yield item
        print(counter_iter)
            # item['sport_category'] = i.get()
        # yield item

            
    
