import json
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import atexit
import psycopg2


# Load database connection parameters
load_dotenv()

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



def get_account_id(data):
    json_string = data.account.split(", 'display_name'")[0] + "}"
    json_string = json_string.replace("'", '"')
    json_string = json_string.replace("False", "false")
    json_string = json_string.replace("True", "true")
    json_object = json.loads(json_string)
    data.drop("account")
    return json_object["id"]


def get_account_toots(account_id):
    """
    Get all toots of an account.

    :param account_id: The id of the account.
    :return: A list of toots.
    """
    cur = conn.cursor()
    cur.execute("SELECT text FROM statuses WHERE account_id = %s;", (account_id,))
    toots = cur.fetchall()
    cur.close()
    return [toot[0] for toot in toots]


def get_followed_accounts(account_id):
    """
    Get all accounts followed by an account.

    :param account_id: The id of the account.
    :return: A list of account ids.
    """
    cur = conn.cursor()
    cur.execute("SELECT target_account_id FROM follows WHERE account_id = %s;", (account_id,))
    follows = cur.fetchall()
    cur.close()
    return [follow[0] for follow in follows]
