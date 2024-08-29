import sys
import traceback
import pandas as pd
from datetime import datetime
from config import pop_config
from sqlalchemy import create_engine
from functions import get_data_count_database, log, insert_excel_sheet_data_to_mysql, send_mail


def check_increment_data(excel_path):
    try:
        database_uri = f'mysql://{pop_config.user}:{pop_config.password}@{pop_config.host}/{pop_config.database}?auth_plugin={pop_config.auth_plugin}'

        engine = create_engine(database_uri)
        query = "SELECT registration_number FROM aggregators"
        database_df = pd.read_sql(query, con=engine)

        excel_df = pd.read_excel(excel_path)

        # missing_rows_in_db = excel_df[~excel_df[2].isin(database_df["registration_number"])].copy()
        # missing_rows_in_excel = database_df[~database_df["registration_number"].isin(excel_df[2])].copy()

        # print(len(missing_rows_in_db), "missing rows in database but not in Excel")
        # print(len(missing_rows_in_excel), "missing rows in Excel but not in database")

        # pop_config.no_data_avaliable = len(missing_rows_in_db)
        # pop_config.no_data_scraped = len(missing_rows_in_db)

        # pop_config.deleted_source = missing_rows_in_excel
        # pop_config.deleted_source_count = len(missing_rows_in_excel)

        # if len(missing_rows_in_excel) > 0:
        #     pop_config.log_list[1] = "Success"
        #     pop_config.log_list[4] = get_data_count_database.get_data_count_database(pop_config.cursor)
        #     pop_config.log_list[6] = "Some data are deleted in the website"
        #     log.insert_log_into_table(pop_config.cursor, pop_config.log_list)
        #     print(pop_config.log_list)
        #     pop_config.log_list = [None] * 8
        #     sys.exit()
        # elif len(missing_rows_in_db) == 0:
        #     pop_config.log_list[1] = "Success"
        #     pop_config.log_list[4] = get_data_count_database.get_data_count_database(pop_config.cursor)
        #     pop_config.log_list[6] = "no new data"
        #     log.insert_log_into_table(pop_config.cursor, pop_config.log_list)
        #     print(pop_config.log_list)
        #     pop_config.log_list = [None] * 8
        #     sys.exit()
        missing_rows_in_db = []
        missing_rows_in_excel = []

        for index, row in database_df.iterrows():
            if row["registration_number"] not in excel_df[2].values:
                missing_rows_in_excel.append(row)

        for index, row in excel_df.iterrows():
            if row[2] not in database_df["registration_number"].values:
                missing_rows_in_db.append(row)

        for row in missing_rows_in_excel:
            print(missing_rows_in_excel)
            pop_config.deleted_sources += row["registration_number"] + ", "

        print(pop_config.deleted_sources, "deleted sources in excel")
        print(len(missing_rows_in_db), "missing rows in database")
        print(len(missing_rows_in_excel), "missing rows in Excel")
        print(missing_rows_in_db, "missing rows in db")

        pop_config.no_data_avaliable = len(missing_rows_in_db)
        pop_config.no_data_scraped = len(missing_rows_in_db)
        pop_config.deleted_source_count = len(missing_rows_in_excel)
        if len(missing_rows_in_excel) > 0 and len(missing_rows_in_db) == 0:
            pop_config.log_list[1] = "Success"
            pop_config.log_list[4] = get_data_count_database.get_data_count_database(pop_config.cursor)
            pop_config.log_list[6] = "Some data are deleted in the website"
            log.insert_log_into_table(pop_config.cursor, pop_config.log_list)
            print(pop_config.log_list)
            pop_config.log_list = [None] * 8
            sys.exit()
        elif len(missing_rows_in_db) == 0:
            pop_config.log_list[1] = "Success"
            pop_config.log_list[4] = get_data_count_database.get_data_count_database(pop_config.cursor)
            pop_config.log_list[6] = "no new data"
            log.insert_log_into_table(pop_config.cursor, pop_config.log_list)
            print(pop_config.log_list)
            pop_config.log_list = [None] * 8
            sys.exit()

        current_date = datetime.now().strftime("%Y-%m-%d")
        increment_file_name = f"incremental_excel_sheet_{current_date}.xlsx"
        increment_data_excel_path = fr"C:\Users\mohan.7482\Desktop\PFRDA\Aggregaters_PFRDA\data\increment_data\{increment_file_name}"
        # missing_rows_in_db.to_excel(increment_data_excel_path, index=False)
        pd.DataFrame(missing_rows_in_db).to_excel(increment_data_excel_path, index=False)
        insert_excel_sheet_data_to_mysql.insert_excel_data_to_mysql(increment_data_excel_path, pop_config.cursor)

    except Exception as e:
        traceback.print_exc()
        pop_config.log_list[1] = "Failure"
        pop_config.log_list[4] = get_data_count_database.get_data_count_database(pop_config.cursor)
        pop_config.log_list[5] = "error in checking part"
        log.insert_log_into_table(pop_config.cursor, pop_config.log_list)
        print(pop_config.log_list)
        send_mail.send_email("PFRDA aggregators script error", e)
        pop_config.log_list = [None] * 8
        sys.exit()
