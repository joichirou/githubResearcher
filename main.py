#coding: utf-8

import datetime
import sys
import config
import userInfo
import libMod as mylib
import repository
import pagenation


class RepositoryCollector():

    def __init__(self):
        self.access_limit       = config.GITHUB_API_ACCESS_LIMIT
        self.access_count       = 0
        self.added_repositories = []
        self.added_users        = []
        self.exec_start_time    = None
        self.exec_end_time      = None

    def main(self):
        """
        collect github repositories using github api.
        """
        self.exec_start_time = datetime.datetime.now()
        print(" * Exec start time: %s" % self._print_dt_fmt(self.exec_start_time))

        repo_github_api = repository.GithubApi()
        json = repo_github_api.get_repositories()
        #print(json)

        repo_db = repository.DB()
        user_db = userInfo.DB()

        print(" * Searching famous repositories.")
        for i, item in enumerate(json["items"]):
            repo = repository.Repository(item)
            print(" L %s. Repo:%s / Lang:%s / ⭐️:%s / User:%s / UserID:%s" % 
            (i+1, repo.name, repo.language, repo.star, repo.owner.name, repo.owner.id))
            if repo.star >= config.MANY_STAR:
                print(" +++ This is famous repository!!! +++")
                if user_db.insert(repo.owner):
                    print("     * added new user:%s" % repo.owner.name)
                    self.added_users.append(repo.owner)
                else:
                    print("     * already exist user.")
            if repo_db.insert(repo):
                print("     * added new repository:%s" % repo.name)
                self.added_repositories.append(repo)
        print("(%s / %s) : (Searched / All)" % (len(json["items"]), json["total_count"]))

        print(" * Get inserted records.")
        searched_records = repo_db.get_records()
        for i, rec in enumerate(searched_records):
            print(" L %s. %s" % (i+1, rec))
        
        print(" * Get inserted users.")
        user_list = user_db.get_records()
        for i, rec in enumerate(user_list):
            print(" L %s. %s" % (i+1, rec))
        
        print(" * Added repositories: %s" % len(self.added_repositories))
        print(" * Added users: %s" % len(self.added_users))
        
        page_db = pagenation.DB()

        page_db.update(repo_db.table, repo_github_api.page_num + 1)
        print(" * Updated page number: %s" % page_db.get_page_number(repo_db.table)[0])

        self.exec_end_time = datetime.datetime.now()
        print(" * Exec end time: %s" % self._print_dt_fmt(self.exec_end_time))
        exec_time = (self.exec_end_time - self.exec_start_time)
        print(" * Exec time: %s" % exec_time)

    def _print_dt_fmt(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    # checking on config file.
    if not config.GITHUB_API_TOKEN:
        print(" * please setting GITHUB_API_TOKEN.")
        exit(1)
    if not config.SEARCH_ROOT_USER:
        print(" * please setting SEARCH_ROOT_USER.")
        exit(1)
    if mylib.is_exceed_rate_limit():
        pass
    # start main program.
    collector = RepositoryCollector()
    while(True):
        if collector.access_count >= collector.access_limit:
            print(" * Over api access limit.")
            break
        collector.access_count = collector.access_count + 1
        collector.main()
    print(" * Github Api access count: %s" % collector.access_count)
