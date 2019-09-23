# -*- coding: UTF-8 -*-
import datetime
import re

import torndb
from db_config import db_configs


class DBBase(object):
    def __init__(self, db_names):
        self.db_clients = {}
        self.main_db = ''
        if isinstance(db_names, str):
            self.__add_db_client(db_names)
            self.main_db = db_names
        elif isinstance(db_names, list) and db_names:
            map(self.__add_db_client, db_names)
            self.main_db = db_names[0]

    def __add_db_client(self, db_name):
        if db_name not in db_configs:
            raise RuntimeError("DB config not found for %s" % db_name)
        db_config = db_configs[db_name]
        host = "%s:%s" % (db_config["host"], 3306 if "port" not in db_config else db_config["port"])
        db_client = torndb.Connection(host, db_config["db"], db_config["user"], db_config["pwd"], connect_timeout=30)
        self.db_clients[db_name] = db_client

    def close(self):
        for k, v in self.db_clients.items():
            v.close()


    def execute(self, sql, *params, **kwargs):
        return self.db_clients[self.main_db].execute(sql, *params, **kwargs)

    def executemany(self, sql, *params, **kwargs):
        return self.db_clients[self.main_db].executemany(sql, *params, **kwargs)

    def execute_rowcount(self, sql, *params, **kwargs):
        return self.db_clients[self.main_db].execute_rowcount(sql, *params, **kwargs)

    def executemany_rowcount(self, sql, *params, **kwargs):
        return self.db_clients[self.main_db].executemany_rowcount(sql, *params, **kwargs)

    def get(self, sql, *params, **kwargs):
        return self.db_clients[self.main_db].get(sql, *params, **kwargs)

    def query(self, sql, *params, **kwargs):
        return self.db_clients[self.main_db].query(sql, *params, **kwargs)

    def update(self, sql, *params, **kwargs):
        return self.db_clients[self.main_db].update(sql, *params, **kwargs)

    def delete_outdated_rows(self, table, dt):
        delete_sql = "delete from `%s` where dt != '%s'" % (table, dt)
        return self.execute_rowcount(delete_sql)

    def write_db_with_df(self, table, df, insert_ignore=False):
        desc_sql = 'desc %s' % table
        field_rows = self.query(desc_sql)
        fields = [f['Field'] for f in field_rows]
        df_cols = df.columns
        # 处理symbol
        if 'symbol' in fields and ('symbol' not in df_cols and 'ts_code' in df_cols):
            symbols = df['ts_code'].str.split('.').str[0]
            df['symbol'] = symbols
        if 'dt' in fields and ('dt' not in df_cols and 'trade_date' in df_cols):
            df['dt'] = df['trade_date'].copy()
        miss_col = [col for col in df_cols if col not in fields]
        df = df.fillna(value=-100000)
        if miss_col:
            df = df.drop(miss_col, axis=1)
        self.write_db(table, df.to_dict('records'), insert_ignore)

    def write_db_with_df_inner(self, table, df, insert_ignore=False):
        desc_sql = 'desc %s' % table
        field_rows = self.query(desc_sql)
        fields = [f['Field'] for f in field_rows]
        df_cols = df.columns
        miss_col = [col for col in df_cols if col not in fields]
        df = df.fillna(value=-100000)
        if miss_col:
            df = df.drop(miss_col, axis=1)
        self.write_db(table, df.to_dict('records'), insert_ignore)

    def write_db(self, table, result, insert_ignore=False):
        """Write data to db.
        """
        # build data.
        data = []
        sql = ""
        if isinstance(result, list):
            for item in result:
                keys = item.keys()
                keys.sort()
                values = [item[i] for i in keys]
                data.append(tuple(values))
                if not sql:
                    sql_keys = map(lambda x: '`%s`' % x, keys)
                    sql = "%s INTO %s (%s) VALUES (%s)" % ("INSERT IGNORE" if insert_ignore else "REPLACE",
                                                           table, ", ".join(sql_keys),
                                                           ", ".join(["%s" for i in xrange(len(keys))]))
        elif isinstance(result, dict):
            keys = result.keys()
            keys.sort()
            values = [result[i] for i in keys]
            data.append(tuple(values))
            if not sql:
                sql_keys = map(lambda x: '`%s`' % x, keys)
                sql = "%s INTO %s (%s) VALUES (%s)" % ("INSERT IGNORE" if insert_ignore else "REPLACE",
                                                       table, ", ".join(sql_keys),
                                                       ", ".join(["%s" for i in xrange(len(keys))]))
        # exec sql.
        return self.db_clients[self.main_db].executemany_rowcount(sql, data)

    def write_db_with_update(self, table, result, get_rowcount=True):
        """Write data to db.
        """
        # build data.
        data = []
        sql = ""
        select_sql = ""
        select_keys = []
        select_data = []
        is_many = True
        if isinstance(result, list):
            for item in result:
                keys = item.keys()
                keys.sort()
                values = [item[i] for i in keys]
                data.append(tuple(values))
                if not sql:
                    sql_keys = map(lambda x: '`%s`' % x, keys)
                    sql = "INSERT INTO %s(%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s" % (table,
                                                                                         ", ".join(sql_keys),
                                                                                         ", ".join(["%s" for i in
                                                                                                    xrange(len(keys))]),
                                                                                         ", ".join(
                                                                                             i + " = VALUES(%s)" % (i)
                                                                                             for i in sql_keys if
                                                                                             i != "`ip`"))
        elif isinstance(result, dict):
            is_many = False
            keys = result.keys()
            keys.sort()
            # values =
            data = [result[i] for i in keys]
            select_keys = [i for i in keys if result[i]]
            select_data = [result[i] for i in keys if result[i]]
            if not sql:
                sql_keys = map(lambda x: '`%s`' % x, keys)
                sql = "INSERT INTO %s(%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s" % (table,
                                                                                     ", ".join(sql_keys),
                                                                                     ", ".join(["%s" for i in
                                                                                                xrange(len(keys))]),
                                                                                     ", ".join(
                                                                                         i + " = VALUES(%s)" % (i) for i
                                                                                         in sql_keys if i != "`ip`"))
            if not select_sql:
                select_sql = "select * from `%s` where " % table
                select_sql += " and ".join(["`%s` = %%s" % k for k in select_keys])
                # print select_sql
        # exec sql.
        db_client = None
        if isinstance(self.main_db, str):
            db_client = self.db_clients[self.main_db]
        else:
            raise RuntimeError("Unsupported db argument type: %s" % self.main_db)
        if is_many:
            if get_rowcount:
                return db_client.executemany_rowcount(sql, data)
            else:
                return db_client.executemany_lastrowid(sql, data)
        else:
            if get_rowcount:
                return db_client.execute_rowcount(sql, *data)
            else:
                db_client.execute_lastrowid(sql, *data)
                return db_client.get(select_sql, *select_data)
