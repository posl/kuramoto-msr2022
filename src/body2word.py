import os
import glob
import re
import sys
import my_log
from tqdm import tqdm
import csv
csv.field_size_limit(sys.maxsize)

# rm not_necessary_word
rm_tags = ("'")

def main():

    #ログ関係のインスタンス生成
    mylog = my_log.mylog(file_name = 'out/out_for_issue',
                        field_names = ["repo_id",
                                        "repo_org",
                                        "issue_id",
                                        "issue_title",
                                        "issue_number",
                                        "issue_created_at",
                                        "issue_created_by",
                                        "issue_closed_at",
                                        "issue_labels",
                                        "pullrequest_id",
                                        "pullrequest_created_at",
                                        "pullrequest_merged_at",
                                        "num_of_mov",
                                        "num_of_img",
                                        "datetime.datetime.now()",
                                        "issue_comments",
                                        "num_of_comments",
                                        "num_of_char",
                                        "issue_words"],
                        create_file = False)
    mylog2 = my_log.mylog(file_name = 'out/out_for_issue',
                        field_names = ["repo_org",
                                        "issue_number",
                                        "issue_created_at",
                                        "issue_closed_at",
                                        "num_of_mov",
                                        "num_of_img",
                                        "issue_comments",
                                        "num_of_comments",
                                        "num_of_char",
                                        "num_of_words"],
                        create_file = False)
    column_id_repo_org      = mylog.get_column_id("repo_org")
    column_id_issue_number  = mylog.get_column_id("issue_number")
    column_id_issue_create  = mylog.get_column_id("issue_created_at")
    column_id_issue_close   = mylog.get_column_id("issue_closed_at")
    column_id_num_of_mov    = mylog.get_column_id("num_of_mov")
    column_id_num_of_img    = mylog.get_column_id("num_of_img")
    column_id_comments      = mylog.get_column_id("issue_comments")
    column_id_num_comments  = mylog.get_column_id("num_of_comments")
    column_id_num_char      = mylog.get_column_id("num_of_char")
    column_id               = mylog.get_column_id("issue_words")
    # src/で実行
    wd = os.getcwd()

    repos = glob.glob(f"{wd}/out/out_for_issue/*")
    for repo in repos:
        repo_name = myget_name_right(repo,"out/out_for_issue/")
        print(f"{repo_name}")
        if repo_name == "__logfile__":
            print("   ------>  pass")
        else:
            mylog.setup_file(f"out/out_for_issue/{repo_name}/parsing_issue_done_list.csv")
            mylog2.setup_file(f"out/out_for_issue/{repo_name}/parsing_issue_done_list_light.csv")

            for idx in tqdm(range(1,mylog.get_len(include_name_field=True))):
                ## issue_comment
                # "[]" or "[['name','date','body']]"
                target_comments = mylog.get_specific_item(idx,column_id_comments)
                target_comments_dict = {}
                if target_comments == "[]":
                    pass
                else:
                    target_comments = target_comments[2:-2]
                    target_comments = target_comments.split(",")
                    i = 0
                    while get_dateline(target_comments[i]) == None:
                        target_comments[0] = target_comments[i]
                        i += 1
                    target_comments[1] = target_comments[i]
                    target_comments[2] = target_comments[i+1]


                    # list ['name','date','body']
                    target_comments[0] = target_comments[0].strip()
                    target_comments[1] = target_comments[1]
                    target_comments[2] = target_comments[2].strip()
                    # name
                    target_comments[0] = target_comments[0].replace("'","")
                    target_comments[0] = target_comments[0].replace('"',"")
                    target_comments[0] = target_comments[0].replace("  "," ")
                    # date == 'Tue Feb 25 22:22:21 2020'
                    target_comments[1] = target_comments[1].replace("Mon ","")
                    target_comments[1] = target_comments[1].replace("Tue ","")
                    target_comments[1] = target_comments[1].replace("Wed ","")
                    target_comments[1] = target_comments[1].replace("Thu ","")
                    target_comments[1] = target_comments[1].replace("Fri ","")
                    target_comments[1] = target_comments[1].replace("Sat ","")
                    target_comments[1] = target_comments[1].replace("Sun ","")
                    target_comments[1] = target_comments[1].replace("Jan","1")
                    target_comments[1] = target_comments[1].replace("Feb","2")
                    target_comments[1] = target_comments[1].replace("Mar","3")
                    target_comments[1] = target_comments[1].replace("Apr","4")
                    target_comments[1] = target_comments[1].replace("May","5")
                    target_comments[1] = target_comments[1].replace("Jun","6")
                    target_comments[1] = target_comments[1].replace("Jul","7")
                    target_comments[1] = target_comments[1].replace("Aug","8")
                    target_comments[1] = target_comments[1].replace("Sep","9")
                    target_comments[1] = target_comments[1].replace("Oct","10")
                    target_comments[1] = target_comments[1].replace("Nov","11")
                    target_comments[1] = target_comments[1].replace("Dec","12")
                    target_comments[1] = target_comments[1].replace("'","")
                    target_comments[1] = target_comments[1].replace('"',"")
                    target_comments[1] = target_comments[1].replace("  "," ")
                    # body
                    target_comments[2] = target_comments[2].replace("'","")
                    target_comments[2] = target_comments[2].replace('"',"")
                    target_comments[2] = target_comments[2].replace("  "," ")
                    words = re.findall("[a-zA-Z']+", target_comments[2].lower())
                    l = list(words)
                    for rm_tag in rm_tags:
                        try:
                            while True:
                                l.remove(rm_tag)
                        except ValueError:
                            pass
                    words = tuple(l)
                    # 単語を数え上げ dictionary形式
                    issue_comment_word = {}
                    issue_comment_word_setdefault = issue_comment_word.setdefault
                    issue_comment_word_keys = issue_comment_word.keys
                    issue_comment_word_keys_cache = issue_comment_word_keys()
                    for word in words:
                        if len(word)<3 or 8<len(word):
                            pass
                        else:
                            if word in issue_comment_word_keys_cache:
                                issue_comment_word[word] = issue_comment_word[word]+1
                            else:# ヒットしなかったら新しく追加
                                issue_comment_word_setdefault(word, 1)
                                issue_comment_word_keys_cache = issue_comment_word_keys()
                    # 辞書型にして保存
                    target_comments_dict.setdefault('created_by', target_comments[0])
                    target_comments_dict.setdefault('created_at', target_comments[1])
                    target_comments_dict.setdefault('commentBody',issue_comment_word)

                ## issue_wordの整形
                target_text = mylog.get_specific_item(idx,column_id)
                # 大文字を小文字に変換
                target_text = target_text.lower()

                words = re.findall("[a-zA-Z]+", target_text)

                l = list(words)
                for rm_tag in rm_tags:
                    try:
                        while True:
                            l.remove(rm_tag)
                    except ValueError:
                        pass
                words = tuple(l)

                # 単語を数え上げ dictionary形式
                my_counter = {}
                my_counter_setdefault = my_counter.setdefault
                my_counter_keys = my_counter.keys
                my_counter_keys_cache = my_counter_keys()
                num_of_words = 0
                for word in words:
                    num_of_words += 1
                    if word in my_counter_keys_cache:
                        my_counter[word] = my_counter[word]+1
                    else:# ヒットしなかったら新しく追加
                        my_counter_setdefault(word, 1)
                        my_counter_keys_cache = my_counter_keys()
                #############################################

                mylog.rewrite_specific_item(idx = idx,
                                            column_id = column_id_comments,
                                            new_data = target_comments_dict)
                mylog.rewrite_specific_item(idx = idx,
                                            column_id = column_id,
                                            new_data = my_counter)

                row = mylog.get_specific_row(index=idx)
                mylog2.write_row([row[column_id_repo_org],
                                row[column_id_issue_number],
                                row[column_id_issue_create],
                                row[column_id_issue_close],
                                row[column_id_num_of_mov],
                                row[column_id_num_of_img],
                                row[column_id_comments],
                                row[column_id_num_comments],
                                row[column_id_num_char],
                                num_of_words])
            mylog.export()
            mylog2.export()

def get_dateline(text):
    # date == 'Tue Feb 25 22:22:21 2020'
    l = re.findall("\w+\s\w+\s+[0-9]+\s[0-9]+:[0-9]+:[0-9]+\s[0-9]+",  text)
    if len(l) > 0:
        return l
    else:
        return None


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