# coding: utf-8

from bottle import route, run, template, view
import repository

@route('/')
@view('index_template')
def index():
    repo_db = repository.DB()
    return dict(
        repositories=repo_db.get_famous_repo_list(10),
        total_repo=len(repo_db.get_records()))

@route('/list')
@route('/list/<page_no>')
@view('list_template')
def list(page_no=None):
    repo_db = repository.DB()
    limit = 50
    if page_no:
        offset = limit * int(page_no)
    return dict(
        repositories=repo_db.get_famous_repo_list(limit, offset),
        total_repo=len(repo_db.get_records()),
        limit=limit,
        page_no=page_no)

run(host='localhost', port=8080, debug=True)