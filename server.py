# coding: utf-8

from bottle import route, run, template, view
import repository

@route('/')
#@route('/<name>')
@view('index_template')
def index():
    repo_db = repository.DB()
    return dict(
        repositories=repo_db.get_famous_repo_list(),
        total_repo=len(repo_db.get_records()))

run(host='localhost', port=8080, debug=True)