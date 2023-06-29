from .db_connection import conn


def get_followed_accounts(account_id):
    """
    Get all accounts followed by an account.

    param account_id: The id of the account.
    return: A list of account ids.
    """
    cur = conn.cursor()
    cur.execute(
        "SELECT target_account_id FROM follows WHERE account_id = %s;", (account_id,)
    )
    follows = cur.fetchall()
    cur.close()
    return [follow[0] for follow in follows]
