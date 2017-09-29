import json, collections, pymysql, web
from bson import json_util

urls = (

    '/user', 'Users',
    '/user/(.*)', 'User'
)
app = web.application(urls, globals())

class User:
    def GET(self, user):
        connection = pymysql.connect(host='testdb.chvxt94wiqg2.us-east-1.rds.amazonaws.com', port=3306,
                                     user='barmaley', password='barmaley', db='test_db')
        sql = "SELECT * FROM users WHERE uuid = '%s'" % user
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        field_names = json_print(rows, cursor)
        cursor.close()
        connection.close()
        return field_names

    def DELETE(self, uuid):
        print uuid
        connection = pymysql.connect(host='testdb.chvxt94wiqg2.us-east-1.rds.amazonaws.com', port=3306,
                                     user='barmaley', password='barmaley', db='test_db')
        sql = "DELETE FROM users WHERE uuid = '%s'" % uuid
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
        return 'User with nickname "%s" is removed\n' % uuid

    def PUT(self, uuid):
        data = json.loads(web.data())
        fn, ln, email = data["first_name"], data["last_name"], data["email"]
        connection = pymysql.connect(host='testdb.chvxt94wiqg2.us-east-1.rds.amazonaws.com', port=3306,
                                     user='barmaley', password='barmaley', db='test_db')
        sql = "UPDATE users SET first_name = '%s', last_name = '%s', email = '%s' WHERE uuid = '%s'" % (fn, ln, email, uuid)
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
        return 'User with nickname "%s" is updated\n' % uuid

class Users:
    def GET(self):
        connection = pymysql.connect(host='testdb.chvxt94wiqg2.us-east-1.rds.amazonaws.com', port=3306,
                                     user='barmaley', password='barmaley', db='test_db')
        sql = "SELECT * FROM users"
        cursor = connection.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        field_names = json_print(rows, cursor)
        cursor.close()
        connection.close()
        return field_names

    def POST(self):
        connection = pymysql.connect(host='testdb.chvxt94wiqg2.us-east-1.rds.amazonaws.com', port=3306,
                                     user='barmaley', password='barmaley', db='test_db')
        data = json.loads(web.data())
        uuid, fn, ln, email = data["uuid"], data["first_name"], data["last_name"], data["email"]
        user_check = 'SELECT * FROM users WHERE  uuid = "%s"' %uuid
        add_user = 'INSERT INTO users (uuid, first_name, last_name, email, data) ' \
                   'VALUES ("%s", "%s", "%s","%s", now())' % (uuid, fn, ln, email)
        cursor = connection.cursor()
        cursor.execute(user_check)
        rows = cursor.fetchall()

        print rows
        if not rows:

            cursor.execute(add_user)
            connection.commit()
            cursor.close()
            connection.close()
            
            return 'User "%s" created\n' % uuid
        else:
            cursor.close()
            connection.close()
            return 'User with uuid "%s" exists\n' %uuid



def json_print(rows, cursor):
        field_names = [i[0] for i in cursor.description]
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d[ field_names[0] ] = row[0]
            d[ field_names[1] ] = row[1]
            d[ field_names[2] ] = row[2]
            d[ field_names[3] ] = row[3]
            d[ field_names[4] ] = row[4]
            d[ field_names[5] ] = row[5]
            objects_list.append(d)
        json_string = json.dumps( objects_list, default=json_util.default )
        return json_string
if __name__ == "__main__":
    app.run()