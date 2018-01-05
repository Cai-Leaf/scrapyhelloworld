# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb


class MoviePipeline(object):
    def process_item(self, item, spider):
        if item["item_class"] == 'movie':
            if self.check_not_in_db(item):
                self.put_in_db(item)
        if item["item_class"] == 'animation':
            if self.check_animation_not_in_db(item):
                self.put_animation_in_db(item)
        return item

    def check_not_in_db(self, item):
        sql = "select * from MOVIE where name = '%s'" % item['name'].replace("'", "\\'")
        update_sql = "UPDATE MOVIE SET score ='%s' WHERE name ='%s'" % (item['score'], item['name'].replace("'", "\\'"))
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            if len(results) < 1:
                return True
            elif (results[0][3] == '' and item['score'] != '') or item['score'] != results[0][3]:
                # 更新内容
                self.cursor.execute(update_sql)
                self.db.commit()
                self.update_score.append(item['name'])
        except MySQLdb.Error as e:
            # Rollback in case there is any error
            print("哎呀错了", e)
            print(sql)
            self.db.rollback()
            return False
        self.can_not_add.append(item['name'])
        return False

    def check_animation_not_in_db(self, item):
        sql = "select * from animation where douban_id = '%s'" % item['douban_id'].replace("'", "\\'")
        update_sql = "UPDATE animation SET score ='%s' WHERE douban_id ='%s'" % (item['score'], item['douban_id'].replace("'", "\\'"))
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            if len(results) < 1:
                return True
            elif (results[0][2] == '' and item['score'] != '') or item['score'] != results[0][2]:
                # 更新内容
                self.cursor.execute(update_sql)
                self.db.commit()
                self.update_animation_score.append(item['name'])
        except MySQLdb.Error as e:
            # Rollback in case there is any error
            print("哎呀错了", e)
            print(sql)
            self.db.rollback()
            return False
        self.can_not_animation_add.append(item['name'])
        return False

    def put_in_db(self, item):
        sql = "insert into MOVIE(imdb, name, date, score, director, summary, time, area) \
                           values ('%s', '%s', '%s', '%s', '%s','%s','%s','%s')" % \
              (item['imdb'], item['name'].replace("'", "\\'"), item['date'], item['score'],
               item['director'].replace("'", "\\'"), item['summary'].replace("'", "\\'"),
               item['time'].replace("'", "\\'"), item['area'])
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.new_add.append(item['name'])
        except MySQLdb.Error as e:
            # Rollback in case there is any error
            print("哎呀错了", e)
            print(sql)
            self.db.rollback()

    def put_animation_in_db(self, item):
        sql = "insert into animation(douban_id, name, date, score, summary, time, area) \
            values ('%s', '%s', '%s', '%s', '%s','%s','%s')" % \
           (item['douban_id'], item['name'].replace("'", "\\'"), item['date'], item['score'],
            item['summary'].replace("'", "\\'"), item['time'].replace("'", "\\'"), item['area'])
        try:
            self.cursor.execute(sql)
            self.db.commit()
            self.new_animation_add.append(item['name'])
        except MySQLdb.Error as e:
            # Rollback in case there is any error
            print("哎呀错了", e)
            print(sql)
            self.db.rollback()

    def open_spider(self, spider):
        # 打开数据库连接
        self.db = MySQLdb.connect("localhost", "root", "123456", "movie", charset="utf8")
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()
        self.new_add = []
        self.update_score = []
        self.can_not_add = []
        self.new_animation_add = []
        self.update_animation_score = []
        self.can_not_animation_add = []

    def close_spider(self, spider):
        # 关闭数据库连接
        self.db.close()
        print("新增的电影", self.new_add)
        print("更新评分的电影", self.update_score)
        print("已经存在的电影", self.can_not_add)
        print("新增的动画", self.new_animation_add)
        print("更新评分的动画", self.update_animation_score)
        print("已经存在的动画", self.can_not_animation_add)


