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
cursor = sql_cnx.cursor(prepared=True)

def get_sql_connection():
    global sql_cnx

    if not sql_cnx:
        # Create a new connection
        sql_cnx = mysql.connector.connect(**config)
        sql_cnx.cachedCursor = sql_cnx.cursor(prepared=True)
        return sql_cnx

    if sql_cnx.is_connected():
        # Return current open connection
        if "cachedCursor" not in dir(sql_cnx):
            sql_cnx.cachedCursor = sql_cnx.cursor(prepared=True)
        return sql_cnx

    # Refresh old connection
    sql_cnx = mysql.connector.connect(**config)
    sql_cnx.cachedCursor = sql_cnx.cursor(prepared=True)
    return sql_cnx


def main():
    app.run()


if __name__ == "__main__":
    main()
