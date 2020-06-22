# coding: utf-8

import libMod as mylib
import sqlite3


class User(object):

    def __init__(self, json):
        self.id            = json["id"]
        self.name          = json["login"]
        self.url           = json["url"]
        self.follower_url  = json["followers_url"]
        self.followers     = []
        self.following_url = json["following_url"]
        self.followings    = []
        self.repos_url     = json["repos_url"]
        self.repos         = []
        self.type          = json["type"]

    def get_followings(self):
        res = mylib.github_api_request(self.following_url.replace("{/other_user}", ""))
        self.followings = []
        for f_user in res.json():
            self.followings.append(User(f_user))
        return self.followings

    def get_followers(self):
        res = mylib.github_api_request(self.follower_url.replace("{/other_user}", ""))
        self.followers = []
        for f_user in res.json():
            self.followers.append(User(f_user))
        return self.followers
    
    def get_repos(self):
        pass

class DB(object):

    def __init__(self):
        self.db_name = "user.db"
        self.table   = "user"
        self.conn    = self._get_conn()
        self._create_table()

    def _get_conn(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        with self.conn as conn:
             c = conn.cursor()
             sql = """create table if not exists %s(
                      id integer primary key default null,
                      name varchar(255) default null,
                      url varchar(255) default null,
                      created_at TIMESTAMP DEFAULT (DATETIME('now','localtime')),
                      updated_at TIMESTAMP DEFAULT (DATETIME('now','localtime')));
                 """ % self.table
             c.execute(sql)
             sql = """CREATE TRIGGER if not exists  trigger_user_updated_at 
             AFTER UPDATE ON %s
                      BEGIN
                        UPDATE %s SET updated_at = DATETIME('now', 'localtime') WHERE rowid == NEW.rowid;
                      END;
                      """ % (self.table, self.table)
             c.execute(sql)
             conn.commit()

    def insert(self, user):
        if self._is_exist_user(user.id):
            return False
        with self.conn as conn:
            c = conn.cursor()
            sql = "insert into %s(id, name, url) values('%s', '%s', '%s');" % (
                self.table, user.id, user.name, user.url)
            c.execute(sql)
            conn.commit()
            return True
    
    def _is_exist_user(self, user_id):
        with self.conn as conn:
            c = conn.cursor()
            sql = "select id, name from %s where id = '%s';" % (self.table, user_id)
            if c.execute(sql).fetchone():
                return True
            return False

    def get_records(self):
        with self.conn as conn:
            c = self.conn.cursor()
            sql = "select id, name from %s;" % self.table
            return c.execute(sql).fetchall()
