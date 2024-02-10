import clickhouse_driver

# CONN_STR = "clickhouse://[login]:[password]@[host]:[port]/[database]"
CONN_STR = "clickhouse://clickhousero:clickhousero_pass@localhost:9000/wiki"

def execute(sql):
    """
    Execute sql
    """
    with clickhouse_driver.dbapi.connect(CONN_STR) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        col_names = tuple(el[0] for el in cursor.description)
        rows = cursor.fetchall()
    return _reformat_cols(col_names, rows)

def _reformat_cols(col_names, rows):
    """
    Reformat into columns=keys dictionary
    """
    data = {val: tuple(row[i] for row in rows) for i, val in enumerate(col_names)}
    return data

def groupby_traces(data, group, x, y, type):
    traces = list()
    for key in set(data[group]):
        bool_map = tuple(key == entry for entry in data[group])
        trace = {
            "type": type,
            "name": key,
            "x": tuple(entry for i, entry in enumerate(data[x]) if bool_map[i]),
            "y": tuple(entry for i, entry in enumerate(data[y]) if bool_map[i]),
        }
        traces.append(trace)
    return traces
