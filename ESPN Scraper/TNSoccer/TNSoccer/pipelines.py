# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class TnsoccerPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = 'Y5d7fp32!@',
            database = '21Nov2022'
        )
        self.cursor = self.conn.cursor()
      
    def create_table(self):
        #--------Main Team Table-----------#
        self.cursor.execute('DROP TABLE IF EXISTS ncaa')
        self.cursor.execute('''CREATE TABLE ncaa (team text, conference text, win_lose text, web_address text)''')

        
        #---------Top Stats on Each Team--------#
        self.cursor.execute('''DROP TABLE IF EXISTS top_stats''')
        self.cursor.execute('''CREATE TABLE top_stats (
                            leading_stat_cat text,
                            leading_athletes text,
                            leading_stat_num text
                            )''')

        self.conn.commit()


    def process_item(self, item, spider):
        self.update_table(item)
        return item

    def update_table(self, item):
        team_list = ['team', 'conference', 'win_lose', 'web_address']
        stats_list = ['leading_stat_cat', 'leading_athletes', 'leading_stat_num']

        if team_list[0] in item.keys(): # No Keys Are Shared Just Check if First Item Matches
            self.cursor.execute('INSERT INTO ncaa VALUES (%s,%s,%s,%s)', (item['team'], item['conference'], item['win_lose'], item['web_address']))
        elif stats_list[0] in item.keys(): # STAT CAT MESSED UP 26Nov2022
            self.cursor.execute('INSERT INTO top_stats VALUES (%s,%s,%s)', (item['leading_stat_cat'], item['leading_athletes'], item['leading_stat_num']))
        else:
            pass

        
        self.conn.commit()

