import os
from dotenv import load_dotenv
import atexit
import psycopg2


# Load database connection parameters
load_dotenv("recommender_api/.env.vagrant.sample")
load_dotenv()

print(os.getenv("DB_NAME"))
# Connect to the database
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
)


def cleanup():
    """
    Close the database connection when the program is terminated.
    """
    conn.close()


# Register the cleanup function to be called when the program is terminated
atexit.register(cleanup)
