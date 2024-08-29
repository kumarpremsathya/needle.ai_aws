import sys
import traceback
import pandas as pd
from config import pop_config
from functions import get_data_count_database, send_mail, log


def insert_excel_data_to_mysql(final_excel_sheets_path, cursor):

    try:
        df = pd.read_excel(final_excel_sheets_path)
        table_name = "aggregators"
        df = df.where(pd.notnull(df), None)
        for index, row in df.iterrows():
            insert_query = f"""
                INSERT INTO {table_name} (name_of_pop, registration_number, issued_date, activity_registered)
                VALUES (%s, %s, %s, %s)
            """

            values = (row[1], row[2], row[3], row[4])
            cursor.execute(insert_query, values)
        pop_config.connection.commit()
        pop_config.log_list[1] = "Success"
        pop_config.log_list[2] = pop_config.no_data_avaliable
        pop_config.log_list[3] = pop_config.no_data_scraped
        pop_config.log_list[4] = get_data_count_database.get_data_count_database(pop_config.cursor)
        print(pop_config.log_list)
        log.insert_log_into_table(pop_config.cursor, pop_config.log_list)
        pop_config.connection.commit()
        pop_config.connection.close()
        pop_config.log_list = [None] * 8
        print("Data inserted into the database table")

    except Exception as e:
        pop_config.log_list[1] = "Failure"
        pop_config.log_list[4] = get_data_count_database.get_data_count_database(pop_config.cursor)
        pop_config.log_list[5] = "error in insert part"
        print(pop_config.log_list)
        log.insert_log_into_table(pop_config.cursor, pop_config.log_list)
        pop_config.connection.commit()
        pop_config.log_list = [None] * 8
        traceback.print_exc()
        send_mail.send_email("PFRDA aggregators script error",  e)
        sys.exit("script error")
