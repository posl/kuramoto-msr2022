import sys
import csv 
import os
from tqdm import tqdm
import glob
csv.field_size_limit(sys.maxsize)

print("\n\033[32m...........program booting...........\033[0m\n")

def myget_name_left(text, target):
    # ${target}より前を抽出したい
    idx = text.find(target)
    t = text[:idx]
    return t
def myget_name_right(text, target):
    # ${target}より後を抽出したい
    idx = text.find(target)
    t = text[idx+len(target):]
    return t

wd = os.getcwd()

repos = glob.glob(f"{wd}/out/out_for_issue/*")
valid_repos = 0
all_issues = 0
all_closed_issue = 0
all_issues_img = 0
all_issues_mov = 0
all_issues_none = 0

for repo in repos:
    dir_name =  myget_name_right(repo,"out/out_for_issue/")
    print(f"{dir_name}")
    if dir_name == "__logfile__":
        print("\t------>\tpass")
    else:
        file_name = f"{wd}/out/out_for_issue/{dir_name}/parsing_issue_done_list.csv"
        img = 0
        mov = 0
        none = 0
        closed = 0
        with open(file_name, mode='r') as f_in:
            reader = csv.reader(f_in)
            l = [row for row in reader]
        len_l = len(l)
        if len_l > 0:
            valid_repos += 1
        for i in tqdm(range(1,len_l)):
            temp = l[i]
            numofimg = int(temp[13])
            numofmov = int(temp[12])
            is_closed = temp[7]
            if is_closed == None or is_closed == "":
                pass
            else:
                closed += 1
                if numofimg == 0:
                    pass
                elif numofimg >= 1:
                    img += 1
                if numofmov == 0:
                    pass
                elif numofmov >= 1:
                    mov += 1
                if numofimg == 0 and numofmov == 0:
                    none += 1

        print(f"num_of_issues (total) = {len(l)-1}")
        if len(l)-1 != 0:
            print(f"num_of_closed_issue = {closed:3}({round(100*closed/(len(l)-1), 2)}%)")
            print(f"num_of_issues (img)  = {img:3}({round(100*img/closed, 2)}%)")
            print(f"num_of_issues (mov)  = {mov:3}({round(100*mov/closed, 2)}%)")
            print(f"num_of_issues (none) = {none:3}({round(100*none/closed, 2)}%)")
            all_issues += len(l)-1
            all_closed_issue += closed
            all_issues_img += img
            all_issues_mov += mov
            all_issues_none += none
print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
print(f"total\t = {all_issues}")
if all_issues != 0:
    print(f"valid_repos = {valid_repos}")
    print(f"num_of_closed_issue = {all_closed_issue:3}({round(100*all_closed_issue/all_issues, 2)}%)")
    print(f"all_img = {all_issues_img:3}({round(100*all_issues_img/all_closed_issue, 2)}%)")
    print(f"all_mov = {all_issues_mov:3}({round(100*all_issues_mov/all_closed_issue, 2)}%)")
    print(f"all_none = {all_issues_none:3}({round(100*all_issues_none/all_closed_issue, 2)}%)")
print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
print("\n\033[32m...........all tasks done!!...........\033[0m\n")