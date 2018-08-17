# coding: utf-8

import sqlite3


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
            result = c.execute(sql).fetchone()
        if result:
            return result[0]
        return None
