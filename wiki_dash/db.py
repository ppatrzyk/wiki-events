import clickhouse_driver
import os

# "clickhouse://[login]:[password]@[host]:[port]/[database]"
CONN_STR = os.environ["CONN_STR"]

def execute(**params):
    """
    Execute sql
    """
    with clickhouse_driver.dbapi.connect(CONN_STR) as conn:
        cursor = conn.cursor()
        cursor.execute(**params)
        col_names = tuple(el[0] for el in cursor.description)
        rows = cursor.fetchall()
    return _reformat_cols(col_names, rows)

def _reformat_cols(col_names, rows):
    """
    Reformat into columns=keys dictionary
    """
    data = {val: tuple(row[i] for row in rows) for i, val in enumerate(col_names)}
    return data
