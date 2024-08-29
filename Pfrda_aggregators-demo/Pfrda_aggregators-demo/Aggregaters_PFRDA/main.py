import sys
import traceback
from config import pop_config
from functions import pdf_download_convert_to_excel, log, get_data_count_database


def main():
    if pop_config.source_status == "Active":
        pdf_download_convert_to_excel.navigate_to_the_page()
        # check_increment_data.check_increment_data(r"C:\Users\mohan.7482\Desktop\PFRDA\Aggregaters_PFRDA\data\first_excel_sheet\first_excel_sheet2024-05-03.xlsx")
        print("finished")

    elif pop_config.source_status == "Hibernated":
        pop_config.log_list[1] = "not run"
        pop_config.log_list[4] = get_data_count_database.get_data_count_database(pop_config.cursor)
        print(pop_config.log_list)
        log.insert_log_into_table(pop_config.cursor, pop_config.log_list)
        pop_config.connection.commit()
        print(pop_config.log_list)
        pop_config.log_list = [None] * 8
        traceback.print_exc()
        sys.exit("script error")

    elif pop_config.source_status == "Inactive":
        pop_config.log_list[1] = "not run"
        pop_config.log_list[4] = get_data_count_database.get_data_count_database(pop_config.cursor)
        print(pop_config.log_list)
        log.insert_log_into_table(pop_config.cursor, pop_config.log_list)
        pop_config.connection.commit()
        print(pop_config.log_list)
        pop_config.log_list = [None] * 8
        traceback.print_exc()
        sys.exit("script error")


if __name__ == "__main__":
    main()
