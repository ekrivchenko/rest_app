#!/usr/bin/env python
import xml.etree.ElementTree as ET
import MySQLdb as db
import json, collections, pymysql, web

urls = (
    '/user', 'add_user',
    '/users', 'list_users',
    '/user/(.*)', 'get_user'
)
app = web.application(urls, globals())
connection = pymysql.connect(host='testdb.chvxt94wiqg2.us-east-1.rds.amazonaws.com', port=3306, user='barmaley', password='barmaley', db='test_db')

class get_user:
    def GET(self, user):
        sql = "SELECT * FROM users WHERE uuid = '%s'" % user
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        field_names = json_print(rows, cursor)
        return field_names
class list_users:
    def GET(self):
        sql = "SELECT * FROM users"
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        field_names = json_print(rows, cursor)
        return field_names
class add_user:
    def POST(self):
        data = json.loads(web.data())
        uuid, fn, ln, email = data["uuid"], data["first_name"], data["last_name"], data["email"]
        add_user = 'INSERT INTO users (uuid, first_name, last_name, email) VALUES ("%s", "%s", "%s"," %s")' % (uuid, fn, ln, email)
        cursor = connection.cursor()
        cursor.execute(add_user)
        connection.commit()
        cursor.close()
        connection.close()
        return add_user
def json_print(rows, cursor):
        field_names = [i[0] for i in cursor.description]
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d[ field_names[0] ] = row[0]
            d[ field_names[1] ] = row[1]
            objects_list.append(d)
        json_string = json.dumps( objects_list )
        return json_string
if __name__ == "__main__":
    app.run()