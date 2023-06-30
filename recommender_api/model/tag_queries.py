from .db_connection import conn


def get_all_tags_with_id_and_name():
    """
    Get all tags.

    return: A list of all tags.
    """
    cur = conn.cursor()
    cur.execute("SELECT id, name, display_name FROM tags;")
    tags = cur.fetchall()
    cur.close()
    return [tag[0:3] for tag in tags]

def get_all_tags_with_name_and_id():
    """
    Get all tags, but only with id and name.

    return: A list of all tags.
    """
    cur = conn.cursor()
    cur.execute("SELECT name, id FROM tags;")
    tags = cur.fetchall()
    cur.close()
    return [tag[0:2] for tag in tags]


def get_tags_by_status_id(status_id):
    """
    Get all tags.

    param status_id: The id of the status.
    return: A list of all tags.
    """
    cur = conn.cursor()
    cur.execute("SELECT tag_id FROM statuses_tags WHERE status_id = %s;", (status_id,))
    tags = cur.fetchall()
    cur.close()
    return [tag[0] for tag in tags]


def get_tags_by_account_id(account_id):
    """
    Get all tags of an account.

    param account_id: The id of the account.
    return: A list of all tags.
    """
    cur = conn.cursor()
    cur.execute("SELECT tag_id FROM tag_follows WHERE account_id = %s;", (account_id,))
    tags = cur.fetchall()
    cur.close()
    return [tag[0] for tag in tags]
