import os
import logging
import mysql.connector

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config = {
    'user': 'admin',
    'password': os.getenv('DB_PASSWORD', ''),
    'host': os.getenv('DB_HOSTNAME', ''),
    'database': 'db',
}

use_db = True
sql_cnx = None
cursor = None

if config['password'] == '' or config['host'] == '':
    use_db = False
    os.environ["THRONE_NO_DB_CREDS"] = "true"
    if os.environ.get("IS_LAMBDA") or os.environ.get("THRONE_USE_DB"):
        logger.warning('Database password/hostname not defined! ' +
                       'Database will NOT be used for API queries.')


def get_sql_connection():
    global sql_cnx

    if not use_db:
        return None

    try:
        if not sql_cnx:
            # Create a new connection
            sql_cnx = mysql.connector.connect(**config)
            sql_cnx.cachedCursor = sql_cnx.cursor(prepared=True)
            logger.info('Successfully connected to database.')
            return sql_cnx

        if sql_cnx.is_connected():
            # Return current open connection
            if "cachedCursor" not in dir(sql_cnx):
                sql_cnx.cachedCursor = sql_cnx.cursor(prepared=True)

            logger.info('Using pooled database connection.')
            return sql_cnx

        # Refresh old connection
        sql_cnx = mysql.connector.connect(**config)
        sql_cnx.cachedCursor = sql_cnx.cursor(prepared=True)
        logger.info('Successfully re-connected to database.')

        return sql_cnx
    except mysql.connector.Error:
        logger.exception('Failed to connect to database.')
        return None
