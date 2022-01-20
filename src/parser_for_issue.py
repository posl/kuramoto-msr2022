# for main
import sys
import csv
from github import Github
import os
import time
from collections import Counter
from collections import defaultdict
import csv
from github.IssueComment import IssueComment
# for logfile
import my_log
import datetime
# for get_links
import re

print("\n\033[32m...........program booting...........\033[0m\n")

csv.field_size_limit(sys.maxsize)
who_am_i = "pc_for_research" # slackの通知名
args = sys.argv

# using username and password or using an access token
if len(args) == 2:
    token = args[1]
    g = Github(f"{token}",timeout=30)
else:
    try:
        with open("config/github-token.config", "r") as f:
            token = f.read()
            g = Github(f"{token}",timeout=30)
    except:
        print("github token = ",end="")
        token = input()
        g = Github(f"{token}",timeout=30)

rate_limit = g.get_rate_limit().core.limit
print(f"rate_limit = {rate_limit} per an hour")
timerValue = 3600/rate_limit
time.sleep(timerValue)

def main():
    wd = os.getcwd()
    if os.getcwd()[-3:] == "src" or os.getcwd()[-4:] == "src/":
        pass
    else:
        os.chdir("./src")
        wd = os.getcwd()
    try:
        os.mkdir("./out_for_issue")
    except FileExistsError:
        pass
    try:
        os.mkdir("./out_for_issue/__logfile__")
    except FileExistsError:
        pass
    
    #ログ関係のインスタンス生成
    mylog = my_log.mylog(file_name = 'out_for_issue',
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
    mylog.setup_slack()


    download_list = my_log.mylog(file_name = 'out_for_issue/__logfile__/download_list_issue.csv',
                                field_names = ['flag',
                                                'repo_name',
                                                'PR_id',
                                                'number',
                                                'url',
                                                'address',
                                                'img_or_mov'])
    movs_num_list = my_log.mylog(file_name = 'out_for_issue',
                                field_names = ['mov_number','mov_url'],
                                create_file = False)
    done_list = my_log.mylog(file_name = 'out_for_issue/__logfile__/logfile_parsing_issue_reponame.csv',
                            field_names = ['reponame_or_id','state'])

    # 選定済みリストの読み込み
    with open("results.csv", "r") as f:
        reader = csv.reader(f)
        l = [row for row in reader]
        my_repo_list = [row[0] for row in l[1:]]
    
    with open('out_for_issue/__logfile__/logfile_parsing_issue_reponame.csv', "r") as f:
        reader = csv.reader(f)
        l = [row for row in reader]
        my_repo_list2 = []
        if len(l) == 1:
            pass
        else:
            for row in l[1:]:
                if row[1] == "success":
                    my_repo_list2.append(row[0])
        my_repo_list = list(set(my_repo_list) - set(my_repo_list2))
        print(my_repo_list)

    for full_name_or_id in my_repo_list:
        idx,repo_done_state = done_list.search_target(target=full_name_or_id,column1=0,column2=1)
        if idx == -1:
            done_list.write_row([full_name_or_id,'closed'])
            repo_done_state = 'closed'
            done_list.export()
        else:
            pass
        try:
            r = g.get_repo(full_name_or_id)
        except Exception as e:
            time_saver(5)
            r = g.get_repo(full_name_or_id)
        time_saver(timerValue)
        print(f"get_repo = {r}")
        mov_exist = "n"

        # フォルダ作成
        abst_path = f"out_for_issue/{r.owner.login}_{r.name}"
        path = f"{wd}/{abst_path}"
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        mylog.setup_file(f"{path}/parsing_issue_done_list.csv")

        repo_myorg = f"{r.owner.login}_{r.name}"
        repo_org = f"{r.owner.login}/{r.name}"
        total_count = 1

        STATE_LIST = []
        if repo_done_state == 'closed':
            STATE_LIST.append('closed')
            STATE_LIST.append('open')
        elif repo_done_state == 'open':
            STATE_LIST.append('open')
        for STATE in STATE_LIST:
            mylog.slack(f"[{who_am_i}] start {STATE}_{full_name_or_id}")
            path_for_print = f"<{STATE}>" + myget_name_right(text=path, target="src/out_for_issue/")
            
            issues_list = r.get_issues(state=STATE)
            total_issues = issues_list.totalCount

            # 本調査ではclosed_issueのみを対象とする
            if STATE == "open":
                issues_list = []

            for issue in issues_list:
                issue_ID = issue.id
                issues_NUMBER = issue.number
                time_saver(timerValue)

                # logを見て、実行済みなら以下の処理はしない
                if mylog.search_target(issue_ID, column1=2) != -1:
                    print(f"\033[2m{total_count:06}({(total_count/total_issues)*100:.3f}%)[{path_for_print}]({issues_NUMBER})pass\033[0m")

                else:
                    # issue毎にid名のフォルダを作る
                    f_path = f"out_for_issue/{repo_myorg}/{str(issue_ID)}"
                    try:
                        os.mkdir(f_path)
                    except FileExistsError:
                        pass

                    issue_body = issue.body 
                    mov_exist,mov_urls = get_mov_urls(issue_body)
                    num_of_mov = 0
                    img_exist,img_urls = get_img_urls(issue_body)
                    num_of_img = 0
                    if img_exist:
                        for i in img_urls:
                            num_of_img += 1
                    if mov_exist:
                        counter = 1
                        movs_num_list.setup_file(f"{path}/{str(issue_ID)}/movs.csv")

                        for mov_url in mov_urls:
                            # img番号とURLの組を記述
                            download_list.write_row(["notDone",
                                                repo_org,
                                                issue_ID,
                                                counter,
                                                str(mov_url),
                                                f"{abst_path}/{str(issue_ID)}/mov{counter}{os.path.splitext(mov_url)[1]}",
                                                "mov"])
                            download_list.export()
                            movs_num_list.write_row([counter,
                                                str(mov_url)])
                            movs_num_list.export()
                            counter += 1
                        num_of_mov = counter - 1

                    if mov_exist:
                        # 処理を表示
                        print(f"\033[32m{total_count:06}({(total_count/total_issues)*100:.3f}%)[{path_for_print}]({issues_NUMBER})...done\033[0m")
                    if mov_exist == False and img_exist == False:
                        print(f"{total_count:06}({(total_count/total_issues)*100:.3f}%)[{path_for_print}]({issues_NUMBER})...done")
                    pullrequest = issue.pull_request
                    if pullrequest == None:
                        pullrequest_created_at = None
                        pullrequest_merged_at = None
                        pullrequest_id = None
                    else:
                        pullrequest_id = int(myget_name_right(pullrequest.html_url,"/pull/"))
                        pullrequest = r.get_pull(number=pullrequest_id)
                        time_saver(timerValue)
                        pullrequest_created_at = pullrequest.created_at
                        pullrequest_merged_at = pullrequest.merged_at

                    target_text = issue_body
                    
                    if target_text == None:
                        target_text = ""
                        num_of_char = 0
                    else:num_of_char = len(issue_body)

                    for rm_text in img_urls:
                        num_of_char -= len(rm_text)
                    for rm_text in mov_urls:
                        num_of_char -= len(rm_text)
                    
                    words = re.findall("[a-zA-Z']+", target_text)
                    target_text = ""
                    for word in words:
                        target_text += f" {word}"

                    my_dict = []
                    for comment in issue.get_comments():
                        time_saver(timerValue)
                        comment_text = comment.body
                        if comment_text == None:
                            comment_text = ""
                        words = re.findall("[a-zA-Z']+", comment_text)
                        comment_text = ""
                        for word in words:
                            comment_text += f" {word}"
                        comment_user = comment.user.name
                        if comment_user == None:
                            pass
                        else:
                            comment_user_tmp = comment_user.split(",")
                            if len(comment_user_tmp) > 1:
                                comment_user = comment_user_tmp[0]
                        my_dict.append([comment_user,comment.created_at.ctime(),comment_text])
                        break


                    num_of_comments = issue.comments
                    mylog.append_row_direct([r.id,
                                repo_org,
                                issue_ID,
                                issue.title,
                                issue.number,
                                issue.created_at,
                                issue.user.name,
                                issue.closed_at,
                                [label.name for label in issue.labels],
                                pullrequest_id,
                                pullrequest_created_at,
                                pullrequest_merged_at,
                                num_of_mov,
                                num_of_img,
                                datetime.datetime.now(),
                                my_dict,
                                num_of_comments,
                                num_of_char,
                                target_text])
                    if mov_exist:
                        pass
                    else:
                        os.rmdir(f_path)
                total_count += 1
                        
            # logのファイル出力
            mylog.export()
            if STATE == "closed":
                done_list.rewrite_row([full_name_or_id, 'open'],idx=done_list.search_target(target=full_name_or_id,column1=done_list.get_column_id('reponame_or_id')))
            else:# STATE == "open"
                done_list.rewrite_row([full_name_or_id, 'success'],idx=done_list.search_target(target=full_name_or_id,column1=done_list.get_column_id('reponame_or_id')))
            done_list.export()
            mylog.slack(f"[{who_am_i}] done {STATE}_{full_name_or_id}")

    # 全処理終了
    mylog.slack(f"[{who_am_i}] all done!")
    return 0




def time_saver(t):
    interval = 0.1
    counter = int(t/interval)
    time.sleep(t - counter*interval)
    for i in range(0, counter):
        if i % 4 == 0:
            print("|",end="",flush=True)
        elif i % 4 == 1:
            print("/",end="",flush=True)
        elif i % 4 == 2:
            print("-",end="",flush=True)
        else :# i % 4 == 3
            print("\\",end="",flush=True)
        time.sleep(0.1)
        print("\b",end="",flush=True)
    print(" \b",end="",flush=True)
        

def get_mov_urls(text):
    # gifまたはmov,mp4を含むかを判定
    mov_urls = None
    if type(text) == str:
        mov_urls = get_links_for_mov(text)

    if(mov_urls != None):# img_urlがあるかで判定
        return True, mov_urls
    else:
        return False, None

def get_img_urls(text):
    # jpg,pngを含むかを判定
    img_urls = None
    if type(text) == str:
        img_urls = get_links_for_img(text)

    if(img_urls != None):# img_urlがあるかで判定
        return True, img_urls
    else:
        return False, None

def get_links_for_mov(text):
    l_gif = re.findall(r"https://user-images.githubusercontent.com/[a-zA-Z0-9\-]+\.gif",  text)
    l_GIF = re.findall(r"https://user-images.githubusercontent.com/[a-zA-Z0-9\-]+\.GIF",  text)
    l_mp4 = re.findall(r"https://user-images.githubusercontent.com/[a-zA-Z0-9\-]+\.mp4",  text)
    l_MP4 = re.findall(r"https://user-images.githubusercontent.com/[a-zA-Z0-9\-]+\.MP4",  text)
    l_mov = re.findall(r"https://user-images.githubusercontent.com/[a-zA-Z0-9\-]+\.mov",  text)
    l = l_gif + l_GIF + l_mp4 + l_MP4 + l_mov
    if len(l) > 0:
        return l
    else:
        return None

def get_links_for_img(text):
    l_png = re.findall(r"https://user-images.githubusercontent.com/[a-zA-Z0-9\-]+\.png",  text)
    l_PNG = re.findall(r"https://user-images.githubusercontent.com/[a-zA-Z0-9\-]+\.PNG",  text)
    l_jpg = re.findall(r"https://user-images.githubusercontent.com/[a-zA-Z0-9\-]+\.jpg",  text)
    l_JPG = re.findall(r"https://user-images.githubusercontent.com/[a-zA-Z0-9\-]+\.JPG",  text)
    l_jpeg = re.findall(r"https://user-images.githubusercontent.com/[a-zA-Z0-9\-]+\.jpeg",  text)
    l = l_png + l_PNG + l_jpg + l_JPG + l_jpeg
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

if(__name__=="__main__"):
    main()
    print("\n\n\033[32m...........all tasks done!!...........\033[0m\n")
