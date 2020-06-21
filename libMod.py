# coding: utf-8

import urllib
import requests
import userInfo
import config

class Search(object):
    def __init__(self, user=config.SEARCH_ROOT_USER):
        self.search_url = "https://api.github.com/search/users"
        self.user       = user

    def search(self):
        response = github_api_request(self.search_url, params={"q": self.user})
        return response.json()


def is_exceed_rate_limit(url=None):
    u"""APIのレート制限を越えていないか"""
    if not url:
        s = Search()
        result = s.search()
        user = userInfo.User(result["items"][0])
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
