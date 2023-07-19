from .db_connection import conn
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
