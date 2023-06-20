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

def get_all_tags():
    """
    Get all tags.

    :return: A list of all tags.
    """
    cur = conn.cursor()
    cur.execute("SELECT id, name, display_name FROM tags;")
    tags = cur.fetchall()
    cur.close()
    return [tag[0:3] for tag in tags]

def get_tags_by_toot_id(toot_id):
    """
    Get all tags.

    :return: A list of all tags.
    """
    cur = conn.cursor()
    cur.execute("SELECT tag_id FROM statuses_tags WHERE status_id = %s;", (toot_id,))
    tags = cur.fetchall()
    cur.close()
    return [tag[0] for tag in tags]

def persist_status_tag_relation(status_id, tag_id):
    """
    Persist a relation between status and tag.

    :return: Boolean.
    """
    cur = conn.cursor()
    cur.execute("INSERT INTO statuses_tags (status_id, tag_id) VALUES (%s, %s);", (status_id, tag_id,))
    cur.close()
    return True

def get_toot_by_id(toot_id):
    """
    Get a toot by id.

    :return: A specific toot by id.
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM statuses WHERE id = %s;", (toot_id,))
    response = cur.fetchall()[0]

    toot = {
        "id": response[0], 
        "uri": response[1], 
        "text": response[2],
        "created_at": response[3],
        "updated_at": response[4],
        "in_reply_to_id": response[5],
        "reblog_of_id": response[6],
        "url": response[7],
        "sensitive": response[8],
        "visibility": response[9],
        "spoiler_text": response[10],
        "reply": response[11],
        "language": response[12],
        "conversation_id": response[13],
        "local": response[14],
        "account_id": response[15],
        "application_id": response[16],
        "in_reply_to_account_id": response[17],
        "poll_id": response[18],
        "deleted_at": response[19],
        "edited_at": response[20],
        "trendable": response[21],
        "ordered_media_attachment_ids": response[22],
    }

    cur.close()
    return toot