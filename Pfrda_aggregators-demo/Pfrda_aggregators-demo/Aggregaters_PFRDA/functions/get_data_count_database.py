def get_data_count_database(cursor):
    cursor.execute("SELECT COUNT(*) FROM aggregators;")
    return cursor.fetchone()[0]
