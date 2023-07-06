from .db_connection import conn
import psycopg2

def get_followed_accounts(account_id):
    """
    Get all accounts followed by an account.

    param account_id: The id of the account.
    return: A list of account ids.
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT target_account_id FROM follows WHERE account_id = %s;", (account_id,)
        )
        follows = cur.fetchall()
        cur.close()
    except psycopg2.DatabaseError as error:
        print(error)
    return [follow[0] for follow in follows]

def get_muted_accounts(account_id):
    """
    Get all accounts muted by an account.

    param account_id: The id of the account.
    return: A list of account ids.
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT target_account_id FROM mutes WHERE account_id = %s;", (account_id,)
        )
        muted_accounts = cur.fetchall()
        cur.close()
    except psycopg2.DatabaseError as error:
        print(error)
    return [muted_account[0] for muted_account in muted_accounts]

def get_blocked_accounts(account_id):
    """
    Get all accounts blocked by an account.

    param account_id: The id of the account.
    return: A list of account ids.
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT target_account_id FROM blocks WHERE account_id = %s;", (account_id,)
        )
        blocked_accounts = cur.fetchall()
        cur.close()
    except psycopg2.DatabaseError as error:
        print(error)
    return [blocked_account[0] for blocked_account in blocked_accounts]
