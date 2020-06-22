# coding: utf-8

import datetime
import urllib
import requests
import config
import userInfo
import sqlite3
import pagenation
import libMod


class Repository(object):
    def __init__(self, json=None):
        if json:
            self.set_json_data(json)
            return
        self.id         = None
        self.name       = None
        self.star       = None
        self.language   = None
        self.owner_id   = None
        self.owner      = None
        self.url        = None

    def set_json_data(self, json):
        self.id         = json["id"]
        self.name       = json["name"]
        self.star       = json["stargazers_count"]
        self.language   = json["language"]
        self.owner_id   = json["owner"]["id"]
        self.owner      = userInfo.User(json["owner"])
        self.url        = json["html_url"]


class GithubApi(object):
    def __init__(self):
        self.page_num = 0

    def get_repositories(self):
        search_url = "https://api.github.com/search/repositories"
        response = self._github_api_request(search_url, params={"q": " "})
        return response.json()

    def _github_api_request(self, url, params={}):
        if params:
            # get page number
            page_db = pagenation.DB()
            repo_db = DB()
            page = page_db.get_page_number(repo_db.table)
            if page:
                self.page_num = int(page[0])
            else:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                page_db.insert(repo_db.table)
                print(" * Insert a new pagenation record.")
                self.page_num = 0
            url_encode = url + "?" + urllib.parse.urlencode(params) + "+language:python" + "&page=" + str(self.page_num) + "&per_page=100"
            print(libMod.add_oauth_param(url_encode))
            res = requests.get(libMod.add_oauth_param(url_encode))
        else:
            res = requests.get(libMod.add_oauth_param(url))
            print(libMod.add_oauth_param(url))
        return res


class DB(object):

    def __init__(self):
        self.db_name = "github.db"
        self.table   = "repository"
        self.conn    = self._get_conn()
        self._create_table()

    def _get_conn(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        with self.conn as conn:
             c = conn.cursor()
             sql = """create table if not exists %s(
                      id integer primary key autoincrement,
                      repository_id integer default null,
                      name varchar(255) default null,
                      star integer default 0,
                      language varchar(255) default null,
                      owner_id integer default null,
                      url varchar(255) default null,
                      created_at TIMESTAMP DEFAULT (DATETIME('now','localtime')),
                      updated_at TIMESTAMP DEFAULT (DATETIME('now','localtime')));
                 """ % (self.table)
             c.execute(sql)
             sql = """CREATE TRIGGER if not exists  trigger_repository_updated_at 
             AFTER UPDATE ON %s
                      BEGIN
                        UPDATE %s SET updated_at = DATETIME('now', 'localtime') WHERE rowid == NEW.rowid;
                      END;
                      """ % (self.table, self.table)
             c.execute(sql)
             conn.commit()

    def insert(self, repo):
        if self._is_exist_repo(repo.id):
            return False
        with self.conn as conn:
            c = conn.cursor()
            sql = "insert into %s(repository_id, name, star, language, owner_id, url) values('%s', '%s', '%s', '%s', '%s', '%s');" % (
                self.table, repo.id, repo.name, repo.star, repo.language, repo.owner.id, repo.url)
            c.execute(sql)
            conn.commit()
            return True

    def _is_exist_repo(self, repo_id):
        with self.conn as conn:
            c = conn.cursor()
            sql = "select repository_id, name from %s where repository_id = '%s';" % (self.table, repo_id)
            if c.execute(sql).fetchone():
                return True
            return False

    def get_records(self):
        with self.conn as conn:
            c = self.conn.cursor()
            sql = "select name from %s;" % self.table
            return c.execute(sql).fetchall()


    def get_famous_repo_list(self):
        repo_list = []
        with self.conn as conn:
            c = self.conn.cursor()
            sql = "select r.repository_id, r.name, r.star, r.language, r.owner_id, r.url, u.name, u.avatar_url, u.url from repository as r join user as u on r.owner_id = u.id where r.star >= 1000 order by r.star desc limit 10;"
            for rec in c.execute(sql).fetchall():
                repo = Repository()
                repo.id         = rec[0]
                repo.name       = rec[1]
                repo.star       = rec[2]
                repo.language   = rec[3]
                repo.owner_id   = rec[4]
                repo.url        = rec[5]
                user            = userInfo.User()
                user.id         = repo.owner_id
                user.name       = rec[6]
                user.avatar_url = rec[7]
                user.url        = "https:github.com/" + user.name
                repo.owner      = user
                repo_list.append(repo)
        return repo_list