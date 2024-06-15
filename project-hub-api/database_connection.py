import psycopg2
from psycopg2 import sql

# Database connection parameters
DB_NAME = "db"
DB_USER = "test"
DB_PASSWORD = "test"
DB_HOST = "localhost"
DB_PORT = "8015"

def create_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connection to the database established successfully.")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def get_user_by_id(conn, user_id):
    try:
        with conn.cursor() as cur:
            query = sql.SQL("SELECT * FROM users WHERE user_id = %s")
            cur.execute(query, (user_id,))
            user = cur.fetchone()
            if user:
                print(f"User found: {user}")
                return user
            else:
                print("User not found.")
                return None
    except psycopg2.Error as e:
        print(f"Error retrieving user: {e}")
        return None

def main():
    conn = create_connection()
    if conn is not None:
        user_id = int(input("Enter user ID to retrieve: "))
        get_user_by_id(conn, user_id)
        conn.close()

if __name__ == "__main__":
    main()
