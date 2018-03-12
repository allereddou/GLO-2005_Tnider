import pymysql

db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     db='PROJET_BD')

cursor = db.cursor(pymysql.cursors.DictCursor)


sql = "INSERT INTO users(id) VALUES ('sandou')"
cursor.execute(sql)


sql = "SELECT * FROM users"
cursor.execute(sql)

for row in cursor:
    print(row)


