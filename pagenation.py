# coding: utf-8

import sqlite3


class DB(object):

    def __init__(self):
        self.db_name = "pagenation.db"
        self.table   = "pagenation"
        self.conn    = self._get_conn()
        self._create_table()

    def _get_conn(self):
        return sqlite3.connect(self.db_name)

    def _create_table(self):
        with self.conn as conn:
             c = conn.cursor()
             sql = """create table if not exists %s(
                      id integer primary key autoincrement,
                      name integer default null,
                      page_num integer default 0,
                      created_at TIMESTAMP DEFAULT (DATETIME('now','localtime')),
                      updated_at TIMESTAMP DEFAULT (DATETIME('now','localtime')));
                 """ % self.table
             c.execute(sql)
             sql = """CREATE TRIGGER if not exists  trigger_pagenation_updated_at 
             AFTER UPDATE ON %s
                      BEGIN
                        UPDATE %s SET updated_at = DATETIME('now', 'localtime') WHERE rowid == NEW.rowid;
                      END;
                      """ % (self.table, self.table)
             c.execute(sql)
             conn.commit()

    def insert(self, name):
        with self.conn as conn:
            c = conn.cursor()
            sql = "insert into %s(name) values('%s');" % (self.table, name)
            c.execute(sql)
            conn.commit()

    def update(self, name, page_num):
        with self.conn as conn:
            c = conn.cursor()
            sql = "update %s set page_num = '%s' where name = '%s';" % (self.table, page_num, name)
            c.execute(sql)
            conn.commit()

    def get_page_number(self, name):
        with self.conn as conn:
            c = self.conn.cursor()
            sql = "select page_num from %s where name = '%s';" % (self.table, name)
            return c.execute(sql).fetchone()
