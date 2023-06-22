from .db_connection import conn


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


def get_tags_by_status_id(status_id):
    """
    Get all tags.

    :return: A list of all tags.
    """
    cur = conn.cursor()
    cur.execute("SELECT tag_id FROM statuses_tags WHERE status_id = %s;", (status_id,))
    tags = cur.fetchall()
    cur.close()
    return [tag[0] for tag in tags]
