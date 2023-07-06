from .db_connection import conn
import psycopg2

def persist_status_tag_relation(status_id, tag_id):
    """
    Persist a relation between status and tag.

    param status_id: The id of the status.
    param tag_id: The id of the tag.
    return: Boolean.
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO statuses_tags (status_id, tag_id) VALUES (%s, %s);",
            (
                status_id,
                tag_id,
            ),
        )
        conn.commit()
        cur.close()
    except psycopg2.DatabaseError as error:
        print(error)
    return True


def get_status_by_id(status_id):
    """
    Get a status by id.

    param status_id: The id of the status.
    return: A specific status by id.
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM statuses WHERE id = %s;", (status_id,))
        response = cur.fetchall()[0]

        status = {
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
    except psycopg2.DatabaseError as error:
        print(error)
    return status


def get_statuses_by_account_id(account_id):
    """
    Get all statuses of an account.

    param account_id: The id of the account.
    return: A list of statuses.
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT text FROM statuses WHERE account_id = %s;", (account_id,))
        statuses = cur.fetchall()
        cur.close()
    except psycopg2.DatabaseError as error:
        print(error)
    return [status[0] for status in statuses]


def get_status_with_tag_ids_and_stats_by_status_id(status_id):
    """
    Get status with joined tag ids by id.

    param status_id: The id of the status.
    return: A specific status by id with joined tag_id as list.
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT statuses.*, array_agg(statuses_tags.tag_id) AS tag_ids, status_stats.replies_count, status_stats.reblogs_count, status_stats.favourites_count FROM statuses LEFT JOIN statuses_tags ON statuses.id = statuses_tags.status_id LEFT JOIN status_stats ON statuses.id = status_stats.status_id WHERE statuses.id = %s GROUP BY statuses.id, status_stats.reblogs_count, status_stats.favourites_count, status_stats.replies_count;",
            (status_id,),
        )
        response = cur.fetchone()

        # Get the column names
        column_names = [desc[0] for desc in cur.description]

        # Convert the result to a dictionary
        status = dict(zip(column_names, response))

        cur.close()
    except psycopg2.DatabaseError as error:
        print(error)
    return status


def get_status_stats_by_status_id(status_id):
    """
    Get all statuses of an account.

    param account_id: The id of the account.
    return: A list of statuses.
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM status_stats WHERE status_id = %s;", (status_id,))
        status_stats = cur.fetchone()
        cur.close()
    except psycopg2.DatabaseError as error:
        print(error)
    
    return status_stats
