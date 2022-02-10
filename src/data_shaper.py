from re import T
import my_log
import os
import glob
from tqdm import tqdm
from datetime import datetime as dt
import ast
import csv
import sys
import math
csv.field_size_limit(sys.maxsize)
def main():
    wd = os.getcwd()
    repos = glob.glob(f"{wd}/out/out_for_issue/*")

    # ファイル操作オブジェクト
    in_f  = my_log.mylog(file_name="out/out_for_issue/",
                        create_file=False)
    out_f = my_log.mylog(file_name="out/out_for_issue/",create_file=False)

    movs_num_list = my_log.mylog(file_name = 'out/out_for_issue',
                                field_names = ['mov_number',
                                                'mov_url',
                                                'pixels_of_height',
                                                'pixels_of_width',
                                                'volume',
                                                'length_or_numOfSheets',
                                                'extension'],
                                create_file = False)

########## data_for_RQ1(repo issue words) ##########
    out_f.set_field_names(["repo_org",
                            "issue_number",
                            "issue_created_at",
                            "issue_open_time",
                            "num_of_img",
                            "num_of_mov",
                            "first_comment_time",
                            "first_comment_words",
                            "num_of_comments",
                            "issue_words",
                            "num_of_char"])
    for repo in repos:
        repo_name = myget_name_right(repo,"out/out_for_issue/")
        print(f"{repo_name}")
        if repo_name == "__logfile__":
            print("   ------>  pass")
        else:
            # ファイルセットアップ
            in_f.setup_file(file_name=f"out/out_for_issue/{repo_name}/parsing_issue_done_list.csv")
            in_f.set_field_names()
            out_f.setup_file(file_name=f"out/data/data_for_RQ1/{repo_name}.csv")
            out_f.reset_file()

            # row取り出し & データ処理
            rows = in_f.get_rows()
            for i in tqdm(range(1,in_f.get_len(include_name_field=True))):
                row = rows[i]
                repo_org = row[in_f.get_column_id("repo_org")]
                issue_number = row[in_f.get_column_id("issue_number")]
                issue_created_at = row[in_f.get_column_id("issue_created_at")]
                issue_open_time = None
                export_signal = True
                if row[in_f.get_column_id("issue_closed_at")] == None or row[in_f.get_column_id("issue_closed_at")] == '':
                    pass
                else:
                    date_time = dt.strptime(row[in_f.get_column_id("issue_closed_at")], '%Y-%m-%d %H:%M:%S')
                    date_time -= dt.strptime(row[in_f.get_column_id("issue_created_at")], '%Y-%m-%d %H:%M:%S')#ex)"2021/11/25  16:47:26"
                    issue_open_time = date_time.total_seconds()
                    if issue_open_time < 5:
                        export_signal = False
                    num_of_img = row[in_f.get_column_id("num_of_img")]
                    num_of_mov = row[in_f.get_column_id("num_of_mov")]
                    if row[in_f.get_column_id("issue_comments")] == None or row[in_f.get_column_id("issue_comments")] == "{}":
                        first_comment_time = issue_open_time
                        first_comment_words = {}
                    else:
                        first_comment = ast.literal_eval(row[in_f.get_column_id("issue_comments")])
                        date_time = dt.strptime(first_comment['created_at'], ' %m %d %H:%M:%S %Y')
                        date_time -= dt.strptime(issue_created_at, '%Y-%m-%d %H:%M:%S')
                        first_comment_time = date_time.total_seconds()
                        if first_comment_time > issue_open_time:
                            first_comment_time = issue_open_time
                        first_comment_words = first_comment["commentBody"]
                    num_of_comments = row[in_f.get_column_id("num_of_comments")]
                    num_of_char = row[in_f.get_column_id("num_of_char")]
                    issue_words = row[in_f.get_column_id("issue_words")]
                    # 書き出し
                    if export_signal == True:
                        out_f.write_row([repo_org,
                                        issue_number,
                                        issue_created_at,
                                        issue_open_time,
                                        num_of_img,
                                        num_of_mov,
                                        first_comment_time,
                                        first_comment_words,
                                        num_of_comments,
                                        issue_words,
                                        num_of_char])
            out_f.export()

########## data_for_RQ1(total_issue) ##########
    out_f.set_field_names(["repo_org",
                            "issue_number",
                            "issue_created_at_year",
                            "issue_open_time",
                            "num_of_img",
                            "num_of_mov",
                            "num_of_comments",
                            "first_comment_time",
                            "num_of_char",
                            "issue_type"])
    print("data_for_RQ1")
    total_counter = 0
    unseleccted_counter = 0
    for repo in repos:
        repo_name = myget_name_right(repo,"out_for_issue/")
        if repo_name == "__logfile__":
            print("   ------>  pass")
        else:
            # ファイルセットアップ
            in_f.setup_file(file_name=f"out/out_for_issue/{repo_name}/parsing_issue_done_list_light.csv")
            in_f.set_field_names()
            out_f.setup_file(file_name=f"out/data/data_for_RQ1/_all_repository.csv")

            # row取り出し & データ処理
            rows = in_f.get_rows()
            total_counter += in_f.get_len(include_name_field=False)
            if in_f.get_len(include_name_field=False) < 1:
                pass
            else:
                for i in tqdm(range(1,in_f.get_len(include_name_field=True))):
                    row = rows[i]
                    repo_org = row[in_f.get_column_id("repo_org")]
                    issue_number = row[in_f.get_column_id("issue_number")]
                    issue_created_at = dt.strptime(row[in_f.get_column_id("issue_created_at")], '%Y-%m-%d %H:%M:%S')#ex)"2021/11/25  16:47:26"
                    issue_created_at_year = issue_created_at.year
                    issue_open_time = None
                    export_signal = True
                    if row[in_f.get_column_id("issue_closed_at")] == None or row[in_f.get_column_id("issue_closed_at")] == '':
                        pass
                    else:
                        date_time = dt.strptime(row[in_f.get_column_id("issue_closed_at")], '%Y-%m-%d %H:%M:%S')
                        date_time -= dt.strptime(row[in_f.get_column_id("issue_created_at")], '%Y-%m-%d %H:%M:%S')#ex)"2021/11/25  16:47:26"
                        issue_open_time = date_time.total_seconds()
                        if issue_open_time>365*24*3600 or issue_open_time<30:
                            export_signal = False
                        else: 
                            pass

                        num_of_img = int(row[in_f.get_column_id("num_of_img")])
                        num_of_mov = int(row[in_f.get_column_id("num_of_mov")])
                        if num_of_img > 0 and num_of_mov > 0:
                            issue_type = "Both"
                        elif num_of_img > 0:
                            issue_type = "Img"
                        elif num_of_mov > 0:
                            issue_type = "Mov"
                        else:
                            issue_type = "None"

                        if row[in_f.get_column_id("issue_comments")] == None or row[in_f.get_column_id("issue_comments")] == "{}":
                            first_comment_time = ""
                        else:
                            first_comment = ast.literal_eval(row[in_f.get_column_id("issue_comments")])
                            date_time = dt.strptime(first_comment['created_at'], ' %m %d %H:%M:%S %Y')
                            date_time -= dt.strptime(row[in_f.get_column_id("issue_created_at")], '%Y-%m-%d %H:%M:%S')
                            first_comment_time = date_time.total_seconds()
                            if first_comment_time > issue_open_time:
                                first_comment_time = issue_open_time
                            if first_comment_time < 1:
                                export_signal = False
                            else:
                                pass

                        # 書き出し
                        if export_signal == True:
                            num_of_char = int(row[in_f.get_column_id("num_of_words")])
                            num_of_comments = int(row[in_f.get_column_id("num_of_comments")])
                            out_f.write_row([repo_org,
                                            issue_number,
                                            issue_created_at_year,
                                            issue_open_time,
                                            num_of_img,
                                            num_of_mov,
                                            num_of_comments,
                                            first_comment_time,
                                            num_of_char,
                                            issue_type])
                        else:
                            unseleccted_counter += 1
            out_f.export()
    print(f"selected_data : {(1-(unseleccted_counter/total_counter))*100}")

def myget_name_left(text, target):
    # ${target}より前を抽出したい
    idx = text.find(target)
    if idx == -1:
        return text
    else:
        return text[:idx]

def myget_name_right(text, target):
    # ${target}より後を抽出したい
    idx = text.find(target)
    if idx == -1:
        return ""
    else:
        return text[idx+len(target):]


if __name__ == "__main__":
    main()
    print("\n\n\033[32m...........all tasks done!!...........\033[0m\n")
