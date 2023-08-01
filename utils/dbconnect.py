def connect_to_mysql(app, mysql):
    try:
        mysql_connection = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        return True, mysql_connection
    except mysql.connector.Error as err:
        return False, err