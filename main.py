#coding: utf-8

import datetime
import sys
import config
import searchRecord
import userInfo
import libMod as mylib


class githubStarResearcher():

    def __init__(self):
        self.searched_users = []
        self.access_limit   = 0
        self.access_count   = 0

    def main(self):
        search = mylib.Search()
        search_record = searchRecord.SearchRecord()
        rec = search_record.get_latest_record()
        if rec:
            print("latest record:%s" % rec)
            res = mylib.github_api_request(str(rec)).json()
            print(res)
            user = userInfo.User(res)
            for f in user.get_followings():
                self._search(f, search_record)
        else:
            search = mylib.Search()
            json = search.search()
            users = []
            for item in json["items"]:
                user = userInfo.User(item)
                self._search(user, search_record)
                users.append(user)

    def _search(self, user, search_record):
        print("user:%s" % user.name)
        if self.access_count >= self.access_limit:
            return
        self.access_count = self.access_count + 1

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
            if repo.star >= config.MANY_STAR:
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


if __name__ == "__main__":
    if mylib.is_exceed_rate_limit():
        pass
    researcher = githubStarResearcher()
    researcher.access_limit = config.GITHUB_API_ACCESS_LIMIT
    researcher.main()
    print("api access: %s" % researcher.access_count)
