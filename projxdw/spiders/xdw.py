# -*- coding: utf-8 -*-
# 1.item返回字典类型即可，不用字典中用list的数据
# 2.使用sqlite3时数据应该是list格式，如：self.cur.execute(insert_sql, list(item.values())),插入的数据应该是list格式。
# 3.使用pipeline为继承自Sqlite3Pipeline(object)
# 4.settings.py中加入两个变量SQLITE_FILE='xdw.db'，SQLITE_TABLE='rent'，而且表需要提前创建好。


import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class XdwSpider(CrawlSpider):
    name = 'xdw'
    allowed_domains = ['www.zgshxd.com']
    start_urls = ['http://www.zgshxd.com/city/yongjing/info.php?catid=154']
    link=LinkExtractor(allow='page=\d+')
    rules = (
        Rule(link, callback='parse_item', follow=True),
    )


    def parse_item(self, response):
        
        print(response)
        item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        lists = response.css('div.list_module')#.extract()
        for lis in lists:
            #print(lis)
            time=lis.css('span b.time::text').extract()[0]
            #print(time)
            title=lis.css('span.title a::text').extract()[0]
            content=lis.css('div.info::text').extract()[0].strip()
            try:
                tel=re.search(r'1\d{10}',content,re.M).group()
            except AttributeError as e:
                print(e)
                tel=''

                continue
            item={'time':time,'title':title,'content':content,'tel':tel}
            # item={'time':[time],'title':[title],'content':[content],'tel':[tel]}
            # 去掉list[]符号，也是可以运行的
            #print(str(item))
            #print(str(lists))

            yield item
