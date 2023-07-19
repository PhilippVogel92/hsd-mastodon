from .db_connection import conn


def persist_status_interest_relation(status_id, interest_id):
    """
    Persist a relation between status and interest.

    param status_id: The id of the status.
    param interest_id: The id of the interest.
    return: Boolean.
    """
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO interests_statuses (status_id, interest_id)
        VALUES (%s, %s)
        ON CONFLICT (status_id, interest_id) DO NOTHING;
        """,
        (
            status_id,
            interest_id,
        ),
    )
    conn.commit()
    cur.close()
    return True

def get_status_by_id(status_id):
    """
    Get a status by id.

    param status_id: The id of the status.
    return: A specific status by id.
    """
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
    return status


def get_statuses_by_account_id(account_id):
    """
    Get all statuses of an account.

    param account_id: The id of the account.
    return: A list of statuses.
    """
    cur = conn.cursor()
    cur.execute("SELECT text FROM statuses WHERE account_id = %s;", (account_id,))
    statuses = cur.fetchall()
    cur.close()
    return [status[0] for status in statuses]


def get_status_with_interest_ids_and_stats_by_status_id(status_id):
    """
    Get status with joined interest ids by id.

    param status_id: The id of the status.
    return: A specific status by id with joined interest_id as list.
    """
    cur = conn.cursor()
    cur.execute(
        "SELECT statuses.*, array_agg(interests_statuses.interest_id) AS interest_ids, status_stats.replies_count, status_stats.reblogs_count, status_stats.favourites_count FROM statuses LEFT JOIN interests_statuses ON statuses.id = interests_statuses.status_id LEFT JOIN status_stats ON statuses.id = status_stats.status_id WHERE statuses.id = %s GROUP BY statuses.id, status_stats.reblogs_count, status_stats.favourites_count, status_stats.replies_count;",
        (status_id,),
    )
    response = cur.fetchone()

    # Get the column names
    column_names = [desc[0] for desc in cur.description]

    # Convert the result to a dictionary
    status = dict(zip(column_names, response))

    cur.close()
    return status


def get_status_stats_by_status_id(status_id):
    """
    Get all statuses of an account.

    param account_id: The id of the account.
    return: A list of statuses.
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM status_stats WHERE status_id = %s;", (status_id,))
    status_stats = cur.fetchone()
    cur.close()
    return status_stats
