from server.config import MYSQL_HOST_NAME, MYSQL_USER_NAME, MYSQL_USER_PASSWORD, MYSQL_DATABASE_NAME
import mysql.connector
from mysql.connector import pooling
import os


# Database configuration
DB_CONFIG = {
    "host": MYSQL_HOST_NAME,
    "user": MYSQL_USER_NAME,
    "password": MYSQL_USER_PASSWORD,
    "database": MYSQL_DATABASE_NAME,
}

# Create a connection pool
connection_pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **DB_CONFIG
)

# Database dependency
def get_db():
    connection = connection_pool.get_connection()
    yield connection
    #try:
    #    yield connection
    #finally:
    #    connection_pool.add_connection(connection)

def db_connect():
    return mysql.connector.connect(
        host=MYSQL_HOST_NAME,
        user=MYSQL_USER_NAME,
        password=MYSQL_USER_PASSWORD,
        database=MYSQL_DATABASE_NAME
    )

def initialize_tables():
    db_connection = db_connect()
    db_cursor = db_connection.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255),
        hashed_password VARCHAR(255)
    )
    """
    db_cursor.execute(query)
    db_connection.close()
    return

def get_user(email):
    db_connection = db_connect()
    db_cursor = db_connection.cursor()
    query = "SELECT id, email, hashed_password FROM users WHERE email=%s"
    values = (email,)
    db_cursor.execute(query, values)
    user = db_cursor.fetchone()
    if user:
        user_id = user[0]
        hashed_password = user[-1]
        db_connection.close()
        return {
            "id": user_id, 
            "email": email, 
            "hashed_password": hashed_password
        }
    else:
        return None
    

def create_user(email, hashed_password):
    db_connection = db_connect()
    db_cursor = db_connection.cursor()
    query = "INSERT INTO users (email, hashed_password) VALUES (%s, %s)"
    values = (email, hashed_password)
    db_cursor.execute(query, values)
    db_connection.commit()
    user_id = db_cursor.lastrowid
    db_connection.close()
    return {"user_id": user_id}

def drop_tables():

    db_connection = db_connect()
    db_cursor = db_connection.cursor()
    query = """
    DROP TABLE users
    """
    db_cursor.execute(query)
    db_connection.close()
    return

