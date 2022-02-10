from re import X
from matplotlib import pyplot
from datetime import datetime as dt
from numpy.lib.shape_base import _put_along_axis_dispatcher
import my_log
import os
import numpy as np
import glob
import ast
import csv
import sys
import warnings
import seaborn
import pandas
import pickle
import math

SAMPLE_SIZE = 1
MAX_NUM_OF_WORDS = 50

pyplot.rcParams['font.size'] = 5
seaborn.set_context('talk', font_scale=0.9)
warnings.filterwarnings('ignore') # 警告メッセージを出ないようにしている
csv.field_size_limit(sys.maxsize)
# imgの出力先
out_imgfile = "out/data/analyzer_Result/"
try:
    os.mkdir("out/data/analyzer_Result/")
except FileExistsError:
    pass
def main():
    infile = my_log.mylog(file_name='data/',create_file=False)
    outfile = my_log.mylog(file_name='data/',create_file=False)
    out_text = my_log.mylog(file_name="data/",create_file=False)
    wd = os.getcwd()
    repos = glob.glob(f"{wd}/out/data/data_for_RQ1/*")

    # 初期化
    y_0_none = [0,0,0,0,0,0,0]
    y_0_img  = [0,0,0,0,0,0,0]
    y_0_mov  = [0,0,0,0,0,0,0]
    data_4_dic_none = {}
    data_4_dic_img = {}
    data_4_dic_mov = {}

    len_repos = len(repos)
    len_repos_img = len_repos
    len_repos_mov = len_repos
    for repo in repos:
        repo_name = myget_name_right(text=repo,target="data_for_RQ1/")
        repo_name = myget_name_left(text=repo_name,target=".")
        if repo_name in ("_all_repository","_samplingDataFrame","_samplingDataFrame_for_comment_time"):
            len_repos_img -= 1
            len_repos_mov -= 1
            len_repos -= 1
        else:
            print(repo_name)
            infile.setup_file(f"out/data/data_for_RQ1/{repo_name}.csv")
            infile.set_field_names()
            # カラム番号取得
            col_num_of_img = infile.get_column_id('num_of_img')
            col_num_of_mov = infile.get_column_id('num_of_mov')
            col_created_at = infile.get_column_id('issue_created_at')
            col_issue_words = infile.get_column_id('issue_words')

        ########### repo_high_tf-idf
            printName = f"high_tfidf_words#{repo_name}"
            print(f"\t{printName}")
            data_len = infile.get_len()
            data_dic_none = {}
            data_dic_img = {}
            data_dic_mov = {}
            for i in range(1, data_len):
                row_data = infile.get_specific_row(index=i)
                ### 計算 ###
                data = ast.literal_eval(row_data[col_issue_words])
                if int(row_data[col_num_of_mov]) > 0:
                    dic = data_dic_mov
                elif int(row_data[col_num_of_img]) > 0:
                    dic = data_dic_img
                else : # int(row_data[col_num_of_img])==0 and int(row_data[col_num_of_mov])==0
                    dic = data_dic_none
                dic_keys = dic.keys()
                for key in data.keys():
                    if key in dic_keys:
                        dic[key] += data[key]
                    else:
                        dic.setdefault(key, data[key])
                        dic_keys = dic.keys()
            # 出力処理
            data_dic_none2= sorted(data_dic_none.items(), key=lambda x:x[1], reverse=True)
            data_dic_img2 = sorted(data_dic_img.items(), key=lambda x:x[1], reverse=True)
            data_dic_mov2 = sorted(data_dic_mov.items(), key=lambda x:x[1], reverse=True)
            # 上位num個の単語を選択
            num = MAX_NUM_OF_WORDS
            print(f"========>>> {max(num,len(data_dic_none2))}")
            data_dic_none = {k:l for k,l in data_dic_none2[:max(num,len(data_dic_none2))]}
            data_dic_img  = {k:l for k,l in data_dic_img2[:max(num,len(data_dic_img2))]}
            data_dic_mov  = {k:l for k,l in data_dic_mov2[:max(num,len(data_dic_mov2))]}
            outfile.set_field_names(["repo_org","type","high_tfidf_words"])
            outfile.setup_file(f"out/data/analyzer_tfidf/{printName}.csv")
            outfile.write_row([repo_name,"none",data_dic_none])
            outfile.write_row([repo_name,"img",data_dic_img])
            outfile.write_row([repo_name,"mov",data_dic_mov])
            outfile.export()

        ########### issue_created_at
            printName = f"issue_created_at#_ALL_REPOSITORY"
            print(f"\t{printName}")
            x = ['~2015','2016','2017','2018','2019','2020','2021']
            data_len = infile.get_len()
            for i in range(1, data_len):
                row_data = infile.get_specific_row(index=i)
                ### 時間を計算 ###
                data = row_data[col_created_at]
                if data == "" or data == None:
                    pass
                else:
                    # data = "2021/12/02  9:29:47"
                    data = dt.strptime(data, '%Y-%m-%d  %H:%M:%S')
                    if data.year-2015 < 0:
                        data_level = 0
                    else:
                        if data.year== 2022: data_level = 2021-2015
                        else: data_level = data.year-2015
                        
                ### グラフに反映 ###
                if int(row_data[col_num_of_img]) > 0:
                    y_0_img[data_level] += 1
                if int(row_data[col_num_of_mov]) > 0:
                    y_0_mov[data_level] += 1
                if int(row_data[col_num_of_img])==0 and int(row_data[col_num_of_mov])==0:
                    y_0_none[data_level] += 1

        ########### total_high_tf-idf
            printName = f"high_tfidf_words#_ALL_REPOSITORY"
            print(f"\t{printName}")
            data_len = infile.get_len()
            for i in range(1, data_len):
                row_data = infile.get_specific_row(index=i)
                ### 計算 ###
                data = ast.literal_eval(row_data[col_issue_words])
                if int(row_data[col_num_of_mov]) > 0:
                    dic = data_4_dic_mov
                elif int(row_data[col_num_of_img]) > 0:
                    dic = data_4_dic_img
                else: # int(row_data[col_num_of_img])==0 and int(row_data[col_num_of_mov])==0
                    dic = data_4_dic_none
                dic_keys = dic.keys()
                for key in data.keys():
                    if key in dic_keys:
                        dic[key] += data[key]
                    else:
                        dic.setdefault(key, data[key])
                        dic_keys = dic.keys()

########### 出力処理(issue_created_at)
    printName = f""
    x = ['~2015','2016','2017','2018','2019','2020','2021']
    for y in range(0,len(x)):
        total_issue = y_0_none[y]+y_0_img[y]+y_0_mov[y]
        if total_issue == 0:
            pass
        else:
            y_0_none[y] = y_0_none[y]/total_issue
            y_0_img[y]  = y_0_img[y]/total_issue
            y_0_mov[y]  = y_0_mov[y]/total_issue
    left = np.arange(len(y_0_img))  # numpyで横軸を設定
    width = 0.3
    pyplot.bar(left,y_0_img,label='img',width=width,align='center', hatch="\\")
    pyplot.bar(left+width,y_0_mov,label='mov',width=width,align='center', hatch="//")
    pyplot.xticks(left,x)
    pyplot.title(printName)
    pyplot.legend()
    pyplot.savefig(f"{out_imgfile}IssueCreatedYear#_ALL_REPOSITORY.png",dpi=200)
    pyplot.close()
    pyplot.figure()

    out_text.set_field_names(["type",'~2015','2016','2017','2018','2019','2020','2021'])
    out_text.setup_file(file_name=f"{out_imgfile}IssueCreatedYear#_ALL_REPOSITORY.csv")
    out_text.reset_file()
    out_text.write_row(["None"]+y_0_none)
    out_text.write_row(["Img"]+y_0_img)
    out_text.write_row(["Mov"]+y_0_mov)
    out_text.export()

########### 出力処理(total_high_tf-idf)
    printName = f"high_tfidf_words#_ALL_REPOSITORY"
    data_4_dic_none2= sorted(data_4_dic_none.items(), key=lambda x:x[1], reverse=True)
    data_4_dic_img2 = sorted(data_4_dic_img.items(), key=lambda x:x[1], reverse=True)
    data_4_dic_mov2 = sorted(data_4_dic_mov.items(), key=lambda x:x[1], reverse=True)
    # 上位num個の単語を選択
    num = 200
    data_4_dic_none = {k:l for k,l in data_4_dic_none2[:num]}
    data_4_dic_img  = {k:l for k,l in data_4_dic_img2[:num]}
    data_4_dic_mov  = {k:l for k,l in data_4_dic_mov2[:num]}
    outfile.set_field_names(["type","high_tfidf_words"])
    outfile.setup_file(f"out/data/analyzer_Result/_{printName}.csv")
    outfile.write_row(["none",data_4_dic_none.keys()])
    outfile.write_row(["img",data_4_dic_img.keys()])
    outfile.write_row(["mov",data_4_dic_mov.keys()])
    outfile.export()

########### 箱図
    printName_list  = ["issue_open_time","first_comment_time","num_of_comments","num_of_char"]
    printName_list2  = ["IssueResolvedTime","FirstCommentTime","#comments","#words"]
    df = pandas.read_csv("./data/data_for_RQ1/all_repository.csv",usecols=lambda x: x not in ['issue_number', 'issue_created_at_year'])
    df_none = df.query('issue_type == "None"')
    df_img  = df.query('issue_type in ["Img", "Both"]')
    df_mov  = df.query('issue_type in ["Mov", "Both"]')
    df_none = df_none.sample(n=SAMPLE_SIZE, replace=True)
    df_img  = df_img.sample(n=SAMPLE_SIZE, replace=True)
    df_mov  = df_mov.sample(n=SAMPLE_SIZE, replace=True)
    df_none_temp = df_none
    df_img_temp  = df_img.replace('Both','Img')
    df_mov_temp  = df_mov.replace('Both','Mov')
    x = pandas.concat([df_none_temp, df_img_temp, df_mov_temp], axis=0)
    df = df.dropna(how='any')
    df_none = df.query('issue_type == "None"')
    df_img  = df.query('issue_type in ["Img", "Both"]')
    df_mov  = df.query('issue_type in ["Mov", "Both"]')
    df_none = df_none.sample(n=SAMPLE_SIZE, replace=True)
    df_img  = df_img.sample(n=SAMPLE_SIZE, replace=True)
    df_mov  = df_mov.sample(n=SAMPLE_SIZE, replace=True)
    df_none_temp = df_none
    df_img_temp  = df_img.replace('Both','Img')
    df_mov_temp  = df_mov.replace('Both','Mov')
    x_for_comment_time = pandas.concat([df_none_temp, df_img_temp, df_mov_temp], axis=0)

    print(f"boxplot -->> ")
    fig,ax = pyplot.subplots(1,4,figsize=(16,4))
    ax=ax.ravel()
    for i in range(4):
        data = x
        # 箱図は外れ値を除いている（極めて見づらいのと，知りたいのは中央値付近だから）
        data.boxplot(column=printName_list[i], whis=1, by='issue_type',ax=ax[i],sym="")
        ax[i].ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
    [ax[i].set_title(printName_list2[i]) for i in range(4)]
    pyplot.tight_layout()
    pyplot.savefig(f"{out_imgfile}_boxplot.png",dpi=1000)
    pyplot.close()
    pyplot.figure()

    print(f"distplot -->> ")
    time = 0
    for i in printName_list:
        if i == "first_comment_time":
            data = x_for_comment_time
        else:
            data = x
        grid = seaborn.FacetGrid(data, col="issue_type")
        grid.map(seaborn.distplot, i, bins=7, kde=True)
        pyplot.savefig(f"{out_imgfile}_distplot_{printName_list2[time]}.png",dpi=100)
        pyplot.close()
        pyplot.figure()
        time += 1

    print(f"violinplot -->> ")
    for i in range(4):
        if printName_list[i] == "first_comment_time":
            data = x_for_comment_time
        else:
            data = x
        seaborn.catplot(x="issue_type", y=printName_list[i], kind="violin",data=data)
        pyplot.savefig(f"{out_imgfile}_violin_{printName_list2[i]}.png",dpi=100)
        pyplot.close()
        pyplot.figure()

    df2 = pandas.read_csv("./data/data_for_RQ1/all_repository.csv")
    df2_none = df2.query('issue_type == "None"')
    df2_img  = df2.query('issue_type in ["Img", "Both"]')
    df2_mov  = df2.query('issue_type in ["Mov", "Both"]')
    df2_none_temp = df2_none
    df2_img_temp  = df2_img.replace('Both','Img')
    df2_mov_temp  = df2_mov.replace('Both','Mov')
    x2 = pandas.concat([df2_none_temp, df2_img_temp, df2_mov_temp], axis=0)

    print(f"boxplot_all -->> ")
    fig,ax2 = pyplot.subplots(1,4,figsize=(16,4))
    ax2=ax2.ravel()
    for i in range(4):
        data = x2
        # 箱図は外れ値を除いている（極めて見づらいのと，知りたいのは中央値付近だから）
        data.boxplot(column=printName_list[i],whis=1.5,by='issue_type',ax=ax2[i],sym="")
        ax2[i].ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
    [ax2[i].set_title(printName_list2[i]) for i in range(4)]
    pyplot.tight_layout()
    pyplot.savefig(f"{out_imgfile}_boxplot_all.png",dpi=500)
    pyplot.close()
    pyplot.figure()

    for i in range(4):
        out_text.set_field_names(["type","min","1-4th","2-4th","3-4th","max","mean","SD"])
        out_text.setup_file(file_name=f"{out_imgfile}_data_{printName_list2[i]}.csv")
        out_text.reset_file()
        data = x2[x2["issue_type"]=="Img"][printName_list[i]]
        print(f"Img = {data.shape}")
        out_text.write_row(["Img"] +[data.min(),data.quantile(0.25),data.quantile(0.5),data.quantile(0.75),data.max(),data.mean(),math.sqrt(data.var())])
        data = x2[x2["issue_type"]=="Mov"][printName_list[i]]
        print(f"Mov = {data.shape}")
        out_text.write_row(["Mov"] +[data.min(),data.quantile(0.25),data.quantile(0.5),data.quantile(0.75),data.max(),data.mean(),math.sqrt(data.var())])
        data = x2[x2["issue_type"]=="None"][printName_list[i]]
        print(f"None = {data.shape}")
        out_text.write_row(["None"]+[data.min(),data.quantile(0.25),data.quantile(0.5),data.quantile(0.75),data.max(),data.mean(),math.sqrt(data.var())])
        data = x2[x2["issue_type"]=="Both"][printName_list[i]]
        print(f"Both = {data.shape}")
        out_text.write_row(["Both"]+[data.min(),data.quantile(0.25),data.quantile(0.5),data.quantile(0.75),data.max(),data.mean(),math.sqrt(data.var())])
        out_text.export()

    with open('out/data/data_for_RQ1/_samplingDataFrame.pickle', 'wb') as f:
        pickle.dump(x, f)
    with open('out/data/data_for_RQ1/_samplingDataFrame_for_comment_time.pickle', 'wb') as f:
        pickle.dump(x_for_comment_time, f)

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