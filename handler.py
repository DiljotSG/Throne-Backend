import api
import mysql.connector
import os

config = {
    'user': 'admin',
    'password': os.getenv('DB_PASSWORD', ''),
    'host': os.getenv('DB_HOSTNAME', ''),
    'database': 'db',
}

app = api.create()
sql_cnx = mysql.connector.connect(**config)


def get_sql_connection():
    global sql_cnx

    if not sql_cnx:
        # Create a new connection
        sql_cnx = mysql.connector.connect(**config)
        return sql_cnx

    if sql_cnx.is_connected():
        # Return current open connection
        return sql_cnx

    # Refresh old connection
    sql_cnx = mysql.connector.connect(**config)
    return sql_cnx


def main():
    app.run()


if __name__ == "__main__":
    main()
