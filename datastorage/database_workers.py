import logging

logger = logging.getLogger("sensorboard.database")


def database_query(conn):
    """ Return the average value of 'consider_last' available measurements
        in database.
    """
    query = f"""SELECT temperature, humidity
                FROM measurements ORDER by timestamp ASC"""
    result = conn.execute(query).all()
    return result
