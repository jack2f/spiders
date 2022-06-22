# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pandas as pd
import time
import sqlite3

class ProjxdwPipeline(object):



    def open_spider(self,spider):
        self.res=pd.DataFrame(columns=["title","time","content","tel"])

    def close_spider(self,spider):
        a=time.strftime("%m%d%H%M%S",time.localtime())
        #b=self.res
        #b['p_price']=b['money']/b['square']
        self.res.to_excel('xdw'+a+'.xlsx',encoding="utf_8_sig",sheet_name="234450",header=True,index=False)
        #print("close---------------->\n",self.res,a)
        #self.res.to_csv('xdw'+a+'.csv',encoding='utf_8_sig')
    def process_item(self, item, spider):
        # print(str(item))
        # print(type(item))
        # print(self.res,"--------------------->")

        res0=pd.DataFrame([item])
        # 给item（字典类型）套上列表后，就可以使用了data = [{'a': 1, 'b': 2},{'a': 5, 'b': 10, 'c': 20}]  df = pd.DataFrame(data)
        self.res=pd.concat([self.res,res0])
        #print(self.res)
        #print(json.dump(item))
        return item

class RentPipeline1(object):
    def __init__(self):
        print("---------use sqlite-----------")
    def open_spider(self,spider):
        self.db_conn=sqlite3.connect("rent_xdw.db")
        self.db_cur=self.db_conn.cursor()
        exe='''CREATE TABLE RentData(
        title TEXT,
        momey REAL, 
        square REAL,
        code TEXT PRIMARY,
        tel TEXT);
        '''
        self.db_cur.execute(exe)
        # self.db_cur.commit()

    def close_spider(self,spider):
        self.db_conn.close()
    def process_item(self, item, spider):
        self.insert_db(item)
        return item
    def insert_db(self,item):
        value=(item["title"],item["money"],item["square"],item["code"],item["tel"])
        sql='''INSERT INTO RentData(
        title,money,square,code,tel)
        VALUES(
        %s,%f,%f,%s,%s)
        '''
        self.db_cur.execute(sql%value)
        # self.db_cur.commit()


class Sqlite3Pipeline(object):
    def __init__(self, sqlite_file, sqlite_table):
        self.sqlite_file = sqlite_file
        self.sqlite_table = sqlite_table
        


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file = crawler.settings.get('SQLITE_FILE'), # 从 settings.py 提取
            sqlite_table = crawler.settings.get('SQLITE_TABLE', 'items')
        )
    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.sqlite_file)
        self.cur = self.conn.cursor()
        create_sql='''CREATE TABLE IF NOT EXISTS rent(
            time text not null,
            title text not null,
            content text not null,
            tel text primary key)'''
        self.cur.execute(create_sql)
        self.conn.commit()
    def close_spider(self, spider):
        self.conn.close()
    def process_item(self, item, spider):
        # print(item.keys())
        # print(', '.join(['?'] * len(item.keys())))
        '''
        insert_sql = "insert into {0}({1}) values ({2})".format(self.sqlite_table,
                                                                ', '.join(item.fields.keys()),
                                                                ', '.join(['?'] * len(item.fields.keys())))
                                                                '''
        insert_sql = "insert into {0}({1}) values ({2})".format(self.sqlite_table,
                                                                ', '.join(item.keys()),
                                                                ', '.join(['?'] * len(item.keys())))    
        # print(insert_sql)  
        # print(list(item.values()))                                                  
        self.cur.execute(insert_sql, list(item.values()))
        self.conn.commit()
        return item

