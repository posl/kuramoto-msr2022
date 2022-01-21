import os
import glob
import sys
import my_log
from tqdm import tqdm
import math
import csv
import ast

csv.field_size_limit(sys.maxsize)

def main():

    #ログ関係のインスタンス生成
    # parsing_issue_done_list.csv
    input = my_log.mylog(file_name = 'out/out_for_issue',
                        create_file = False)
    # words_idf_list.csv
    output = my_log.mylog(file_name = 'out/out_for_issue',
                            field_names = ["word",
                                            "idf",
                                            "num_of_files"],
                            create_file = False)

    # src/で実行
    wd = os.getcwd()
    repos = glob.glob(f"{wd}/out/out_for_issue/*")
#================================= idf session =================================#
    print("\n\t=========== idf session ===========\n")
    for repo in repos:
        repo_name = myget_name_right(repo,"out/out_for_issue/")
        print(f"{repo_name}",flush=True)
        if repo_name == "__logfile__":
            print("\t------>\tpass")
        else:
            input.setup_file(f"out/out_for_issue/{repo_name}/parsing_issue_done_list.csv")
            output.setup_file(f"out/out_for_issue/{repo_name}/words_idf_list.csv")
            output.reset_file()

            input_len = input.get_len(include_name_field=False)

            target_dics = input.get_columns(column_id = input.get_column_id("issue_words"))
            out = {}
            # キャッシュ
            ast_literal_eval = ast.literal_eval
            math_log = math.log
            for idx in tqdm(range(1,input_len)):
                target_text = target_dics[idx]
                target_dic = ast_literal_eval(target_text)
                out_keys = out.keys()
                for dic_key in target_dic.keys():
                    if dic_key in out_keys:
                        out[dic_key] += 1
                    else:
                        out.setdefault(dic_key, 1)
                        out_keys = out.keys()
            print("   >>  Now Exporting...\t",end="",flush=True)
            for dic_key in out.keys():
                word = dic_key
                num_of_files = out[dic_key]
                idf = math_log(input_len/num_of_files)
                output.write_row([word, idf, num_of_files])
            output.export()
            print("Done",end="\n\n")

#================================= tf-idf session =================================#
    print("\n\t=========== tf-idf session ===========\n")
    for repo in repos:
        repo_name = myget_name_right(repo,"out_for_issue/")
        print(f"{repo_name}",flush=True)
        if repo_name == "__logfile__":
            print("\t------>\tpass")
        else:
            input.setup_file(f"out/out_for_issue/{repo_name}/parsing_issue_done_list.csv")
            input_len = input.get_len()
            output.setup_file(f"out/out_for_issue/{repo_name}/words_idf_list.csv")
            sum_of_words = 0
            # キャッシュ
            ast_literal_eval = ast.literal_eval
            out_key_col = output.get_column_id("word")
            out_idf_col = output.get_column_id("idf")
            in_col = input.get_column_id("issue_words")
            target_dics = input.get_columns(column_id = in_col)
            for idx in range(1,input_len):
                # sum_of_words is summary of number of words in the one issue.
                target_text = target_dics[idx]
                target_dic = ast_literal_eval(target_text)
                for dic_value in target_dic.values():
                    sum_of_words += dic_value

                # calculate th-idf_value and export it to inputFile.
            for idx in tqdm(range(1,input_len)):

                target_text = target_dics[idx]
                target_dic = ast_literal_eval(target_text)

                # parsing_issue_done_list.csvの更新
                # 文字の出現回数 -> tf-idf値
                remove_keys = []
                for dic_key in target_dic.keys():
                    tf_value = target_dic[dic_key]/sum_of_words
                    index = output.search_target(target=dic_key,column1=out_key_col)
                    idf_value = float(output.get_specific_item(index=index,column_id=out_idf_col))
                    if idf_value < 1:# 頻繁に出現する単語は除外
                        remove_keys.append(dic_key)
                    else:
                        tf_idf_value = tf_value * idf_value
                        target_dic[dic_key] = round(tf_idf_value, 10)
                for dic_key in remove_keys:
                    target_dic.pop(dic_key)
                input.rewrite_specific_item(idx=idx,column_id=in_col,new_data=target_dic)
            input.export()


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