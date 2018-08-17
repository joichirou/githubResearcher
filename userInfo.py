# coding: utf-8

import libMod as mylib


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
        res = mylib.github_api_request(self.following_url.replace("{/other_user}", ""))
        self.followings = []
        for f_user in res.json():
            self.followings.append(User(f_user))
        return self.followings

    def get_repos(self):
        res = mylib.github_api_request(self.repos_url)
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
