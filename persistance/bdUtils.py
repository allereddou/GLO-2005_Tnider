def getUserFromEmail(email):
    from server import app, get_db
    with app.app_context():
        cursor = get_db()

        sql = "SELECT * FROM user WHERE email='{}';"
        cursor.execute(sql.format(email))
        result = cursor.fetchall()

        if len(result) != 1:
            return False
        return result[0]
