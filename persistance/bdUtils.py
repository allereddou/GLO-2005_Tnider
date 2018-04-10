def getUserFromEmail(email):
    from server import app, get_db
    with app.app_context():
        cursor = get_db()

        sql = "SELECT * FROM user WHERE email='{}';"
        cursor.execute(sql.format(email))
        result = cursor.fetchall()

        print(result[0])

        if len(result) != 0:
            return False
        return result[0]
