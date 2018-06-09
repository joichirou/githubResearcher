#coding: utf-8

import datetime
import requests
import sys
import sqlite3
import urllib
import config

MANY_STAR         = 1000
GITHUB_API_ACCESS = 0

def is_exceed_rate_limit(url=None):
    u"""APIのレート制限を越えていないか"""
    if not url:
        s = Search()
        result = s.search()
        user = User(result["items"][0])
        url = user.repos_url
    res = requests.get(url)
    json = res.json()
    if "message" in json:
        print("over api rate limit.\n[api message]%s" % json["message"])
        return True
    return False


def github_api_request(url, params={}):
    if params:
        url_encode = url + "?" + urllib.parse.urlencode(params)
        res = requests.get(add_oauth_param(url_encode))
    else:
        res = requests.get(add_oauth_param(url))
    global GITHUB_API_ACCESS
    GITHUB_API_ACCESS += 1
    return res


def add_oauth_param(url):
    u"""認証用パラメータを付加する"""
    oauth_params = {"access_token": config.GITHUB_API_TOKEN}
    if url.find("?") > -1:
        linking = "&"
    else:
        linking = "?"
    encode_url = url + linking + urllib.parse.urlencode(oauth_params)
    return encode_url


class Search(object):

    def __init__(self, user="payzaburou"):
        self.search_url = "https://api.github.com/search/users"
        self.user       = user

    def search(self):
        response = github_api_request(self.search_url, params={"q": self.user})
        return response.json()


class User(object):

    def __init__(self, json):
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
        res = github_api_request(self.following_url.replace("{/other_user}", ""))
        self.followings = []
        for f_user in res.json():
            self.followings.append(User(f_user))
        return self.followings

    def get_repos(self):
        res = github_api_request(self.repos_url)
        self.repos = []
        for repo in res.json():
            r = Repository(repo)
            self.repos.append(r)
        return self.repos


class Repository(object):

    def __init__(self, json):
        self.name       = json["name"]
        self.star       = json["stargazers_count"]
        self.language   = json["language"]
        self.owner      = User(json["owner"])
        self.clone_url  = json["clone_url"]
        self.created_at = json["created_at"]
        self.updated_at = json["updated_at"]


class GitHubStarResearcher():

    def __init__(self):
        self.searched_users = []

    def main(self):
        search = Search()
        search_record = SearchRecord()
        rec = search_record.get_latest_record()
        if rec:
            print("latest record:%s" % rec)
            res = github_api_request(str(rec)).json()
            print(res)
            user = User(res)
            for f in user.get_followings():
                self._search(f, search_record)
        else:
            search = Search()
            json = search.search()
            users = []
            for item in json["items"]:
                user = User(item)
                self._search(user, search_record)
                users.append(user)

    def _search(self, user, search_record):
        print("user:%s" % user.name)

        self.searched_users.append(user.name)
        if self._search_many_stars_repo(user.get_repos()):
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            search_record.record(user.url, now)
            sys.exit()

        followings = user.get_followings()
        for f in followings:
            if self._is_not_searched(f.name):
                print("user:%s" % f.name)
                if self._search_many_stars_repo(f.get_repos()):
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    search_record.record(f.url, now)
                    sys.exit()

        for f in followings:
            if self._is_not_searched(f.name):
                self._search(f, search_record)
                self.searched_users.append(f.name)

    def _search_many_stars_repo(self, repos):
        star_repos = []
        for repo in repos:
            print("repo:%s" % repo.name)
            if repo.language != "Python":
                continue
            if repo.star >= MANY_STAR:
                star_repos.append(repo)
        if star_repos:
            print("=====star repos====")
            for repo in star_repos:
                print("owner:%s" % repo.owner.name)
                print("repo:%s" % repo.name)
                print("star:%s" % repo.star)
                print("updated at:%s" % repo.updated_at)
            print("===================")
            print("searched users: %s" % self.searched_users)
            return True
        return False

    def _is_not_searched(self, user_name):
        u"""まだ探索していないユーザーの判定"""
        if user_name not in self.searched_users:
            return True
        self.searched_users.append(user_name)
        return False


class SearchRecord(object):

    def __init__(self):
        self.db_name = "search.db"
        self.table   = "search_history"
        self.conn    = self._get_conn()
        self._create_table()

    def _get_conn(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        with self.conn as conn:
             c = conn.cursor()
             sql = """create table if not exists %s(
                      id integer primary key autoincrement,
                      owner_url varchar(255) default null,
                      search_date datetime default '0000-00-00');
                 """ % self.table
             c.execute(sql)
             conn.commit()

    def record(self, url, search_date):
        with self.conn as conn:
            c = conn.cursor()
            sql = "insert into %s(owner_url, search_date) values('%s', '%s');" % (self.table, url, search_date)
            print(sql)
            c.execute(sql)
            conn.commit()

    def get_latest_record(self):
        with self.conn as conn:
            c = self.conn.cursor()
            sql = "select owner_url from %s order by search_date desc;" % self.table
            print(sql)
            c.execute(sql)
            return c.fetchone()[0]


if __name__ == "__main__":
    global GITHUB_API_ACCESS
    if is_exceed_rate_limit():
        pass
        #sys.exit()
    researcher = GitHubStarResearcher()
    researcher.main()
    print("api access: %s" % GITHUB_API_ACCESS)
