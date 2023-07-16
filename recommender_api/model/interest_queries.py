from .db_connection import conn
import time
import datetime

def get_all_interests_with_name_and_id():
    """
    Get all interest, but only with id and name.

    return: A list of all interests.
    """
    cur = conn.cursor()
    cur.execute("SELECT name, id FROM interests;")
    interests = cur.fetchall()
    cur.close()
    return [interest[0:2] for interest in interests]


def get_interests_by_status_id(status_id):
    """
    Get all interests of a specific status.

    param status_id: The id of the status.
    return: A list of all interests associated with the status.
    """
    cur = conn.cursor()
    cur.execute("SELECT interest_id FROM interests_statuses WHERE status_id = %s;", (status_id,))
    interests = cur.fetchall()
    cur.close()
    return [interest[0] for interest in interests]


def get_interests_by_account_id(account_id):
    """
    Get all interests of an account.

    param account_id: The id of the account.
    return: A list of all interests.
    """
    cur = conn.cursor()
    cur.execute("SELECT interest_id FROM interest_follows WHERE account_id = %s;", (account_id,))
    interests = cur.fetchall()
    cur.close()
    return [interest[0] for interest in interests]


def persist_interest(name):
  """
  Persist an interest.

  param status_id: The id of the status.
  param interest_id: The id of the interest.
  return: Boolean.
  """
  ts = time.time()
  timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
  cur = conn.cursor()
  cur.execute(
    """
    INSERT INTO interests (name, display_name, created_at, updated_at)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
    """,
    (
      name,
      name,
      timestamp,
      timestamp
    ),
  )
  conn.commit()
  cur.close()
  return True
