import pymysql

TABLENAME = "gamespider"

class connSql(object):

    def __init__(self, host="47.57.190.6", port=3306, usr="game", passwd="3Lbx4FFpPD8YDz3L", database="game"):
        self.conn = pymysql.connect(host=host, port=port, user=usr, passwd=passwd, db=database,
                                    charset="utf8")
        self.db = self.conn.cursor()

    def __del__(self):
        self.db.close()
        self.conn.close()

    def select_data(self, item_info):
        string_list = []
        for i in item_info.keys():
            string = '%s="%s"' % (i, str(item_info.get(i)))
            string_list.append(string)
        sql_string = ' and '.join(string_list)

        select_sql = "select urlList, othList from {} where {};".format(TABLENAME, sql_string)
        self.conn.ping(reconnect=True)
        self.db.execute(select_sql)
        res = self.db.fetchall()
        if res:
            return res[0]
        else:
            return False




if __name__ == '__main__':
    sql = connSql()
    # sql.select_data(table_name="cjrkcompanyinfo")