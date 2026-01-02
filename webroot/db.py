import MySQLdb
import pandas as pd


class DB:
    host = 'qgiv-analytics-db.cmk0lktild28.us-east-1.rds.amazonaws.com'
    user ='jeremy'
    password = 'f00d4Thought'
    database = 'qgivanalytics'


def select_rows(table, fields=['*'], where=None, limit=None, order_by=None, group_by=None):
    query = "SELECT "+", ".join(fields)+" FROM "+str(table)

    if where is not None:
        query = query + " WHERE " + str(where)

    if group_by is not None:
        query = query + " GROUP BY " + ", ".join(group_by)

    if order_by is not None:
        if order_by[0] == '-':
            order_by = order_by[1:]
            direction = 'DESC'
        else:
            direction = 'ASC'
        query = query + " ORDER BY " + str(order_by) + " " + direction

    if limit is not None:
        query = query + " LIMIT " + str(limit)

    db = get_db()
    df = pd.read_sql(query, con=db)

    return df


def insert_rows(table, data=[], columns=[], debug=False):
    db = get_db()
    cursor = db.cursor()

    query = "INSERT IGNORE INTO "+str(table)+" ("+", ".join(columns)+") VALUES ("+", ".join(["'%s'" for _ in columns])+")"

    if debug:
        print("\tINSERT_ROWS query: {}".format(query))
    
    for d in range(0, len(data)):
        if type(data[d]) == dict:
            cursor.execute(query, data[d].values())
        else:
            cursor.execute(query, data[d])

    db.commit()
    cursor.close()


def update_rows(table, data=[], columns=[], where=None, debug=False):
    db = get_db()
    cursor = db.cursor()

    column_arr = ["{}=%s".format(c) for c in columns]

    query = "UPDATE "+str(table)+" SET "+", ".join(column_arr)
    
    if where is not None:
        query = query+" WHERE "+str(where)

    if debug:
        print("UPDATE_ROWS query: {}".format(query))

    for d in range(0, len(data)):
        cursor.execute(query, data[d])

    db.commit()
    cursor.close()


def execute_query(query):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(query)

    db.commit()
    cursor.close()


def insert_dataframe(table, df):
    db = get_db()
    cursor = db.cursor()

    query = "INSERT IGNORE INTO "+str(table)+" ("+", ".join(df.columns)+") VALUES ("+", ".join(['%s' for i in range(0, len(df.columns))])+")"

    try:
        for i, r in df.iterrows():
            cursor.execute(query, r)
    except Exception, e:
        print(e)
        print("Last query:")
        print(cursor._last_executed)
        return

    db.commit()
    cursor.close()


def insert_csv(table, file_name, start_index=0):
    import csv

    cols = []
    counter = 0
    data_cache = []

    with open(file_name) as f:
        reader = csv.reader(f)
        for row in reader:
            if len(cols) == 0:
                cols = row[start_index:]
            else:
                if counter >= 100:
                    data_cache.append(row[start_index:])
                    # accumulated 100, insert data
                    insert_rows(table, data=data_cache, columns=cols)
                    data_cache = []
                    counter = 0
                else:
                    # less than 100, aggregate rows
                    data_cache.append(row[start_index:])
                    counter = counter + 1
        if len(data_cache) > 0:
            insert_rows(table, data=data_cache, columns=cols)


def select_to_dataframe(table):
    db = get_db()
    df = pd.read_sql('SELECT * FROM '+str(table), con=db)
    return df


def get_db():
    db = MySQLdb.connect(
        host=DB.host,
        user=DB.user,
        passwd=DB.password,
        db=DB.database
    )
    return db
