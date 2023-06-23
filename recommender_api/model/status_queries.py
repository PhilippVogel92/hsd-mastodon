from .db_connection import conn


def persist_status_tag_relation(status_id, tag_id):
    """
    Persist a relation between status and tag.

    :return: Boolean.
    """
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
    return True


def get_status_by_id(status_id):
    """
    Get a status by id.

    :return: A specific status by id.
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


def get_account_statuses(account_id):
    """
    Get all statuses of an account.

    :param account_id: The id of the account.
    :return: A list of statuses.
    """
    cur = conn.cursor()
    cur.execute("SELECT text FROM statuses WHERE account_id = %s;", (account_id,))
    statuses = cur.fetchall()
    cur.close()
    return [status[0] for status in statuses]