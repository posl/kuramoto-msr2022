from matplotlib import pyplot
import pingouin as pg
from numpy import column_stack
import pandas
import os
import pickle
import scipy.stats as stats
import scikit_posthocs as sp

def main():
    if not(os.path.exists("data/analyzer_RQ1_test/")):
        os.mkdir("out/data/analyzer_RQ1_test/")
    print("\033[32m data \033[0m")
    columns_stack  = ["issue_open_time","first_comment_time","num_of_comments","num_of_char"]
    with open('out/data/data_for_RQ1/_samplingDataFrame.pickle', 'rb') as f:
        df = pickle.load(f)
    df_none = df.query('issue_type == "None"')
    df_img  = df.query('issue_type in ["Img", "Both"]')
    df_mov  = df.query('issue_type in ["Mov", "Both"]')
    with open('out/data/data_for_RQ1/_samplingDataFrame_for_comment_time.pickle', 'rb') as f:
        df_for_comment_time = pickle.load(f)
    df_ct_none = df_for_comment_time.query('issue_type == "None"')
    df_ct_img  = df_for_comment_time.query('issue_type in ["Img", "Both"]')
    df_ct_mov  = df_for_comment_time.query('issue_type in ["Mov", "Both"]')
    
    for col in columns_stack:
        if col == "first_comment_time":
            df_none_col = df_ct_none[col]
            df_img_col  = df_ct_img[col]
            df_mov_col  = df_ct_mov[col]
        else:
            df_none_col = df_none[col]
            df_img_col  = df_img[col]
            df_mov_col  = df_mov[col]
        # 正規性検定
        print(f"\033[32m {col} ---->>> #K-S検定 (正規性検定) \033[0m")
        fig,ax = pyplot.subplots(1,3,figsize=(8,8))
        ax=ax.ravel()
        for i in range(3):
            cols = [df_none_col,df_img_col,df_mov_col][i]
            stats.probplot(cols, dist="norm", plot=ax[i])
            ax[i].set_title(["None","Img","Mov"][i])
            # コルモゴロフ・スミルノフ検定(K-S検定)
            # シャピロ・ウィルク検定(S-W検定)よりも高速で，データ数が多い時は上を使う
            result = stats.kstest(cols, "norm")
            print(f"正規性{result}")
        # Levene検定
        result = stats.levene(df_none_col,df_img_col,df_mov_col)
        print(f"等分散性{result}")
        pyplot.tight_layout()
        pyplot.savefig(f"out/data/analyzer_RQ1_test/plobplot_#{col}.png",dpi=100)
        pyplot.close()
        pyplot.figure()

        # ANOVA(パラメトリック)
        print(f"\033[32m {col} ---->>> #ANOVA (群間有意差検定)\033[0m")
        result = stats.f_oneway(df_none_col, df_img_col, df_mov_col)
        print(result)

        # Kruskal-Wallis test(一元配置分散分析のノンパラメトリック版)
        print(f"\033[32m {col} ---->>> #Kruskal-Wallis test (群間有意差検定)\033[0m")
        result = stats.kruskal(df_none_col, df_img_col, df_mov_col)
        print(result)

        # ノンパラメトリック多重比較
        print(f"\033[32m {col} ---->>> #Steel-Dwass test (多重比較)\033[0m")
        if col == "first_comment_time":
            df_none_temp = df_ct_none
            df_img_temp  = df_ct_img.replace('Both','Img')
            df_mov_temp  = df_ct_mov.replace('Both','Mov')
        else:
            df_none_temp = df_none
            df_img_temp  = df_img.replace('Both','Img')
            df_mov_temp  = df_mov.replace('Both','Mov')
        x = pandas.concat([df_none_temp, df_img_temp, df_mov_temp], axis=0)
        result = sp.posthoc_dscf(a=x,val_col=col,group_col='issue_type')
        print(f"{result}")

        print(f"\033[32m {col} ---->>> #Games-Howell test (正規性ありの多重比較)\033[0m")
        result = pg.pairwise_gameshowell(dv=col, between='issue_type', data=x)
        print(f"{result}")
        print(f"\033[32m {col} ---->>> #Turkey test (正規性ありの多重比較)\033[0m")
        result = pg.pairwise_tukey(dv=col, between='issue_type', data=x)
        print(f"{result}")
        print("95%信頼区間は±1.96*SE")
        print("****************************************************************")
        print("****************************************************************")

if __name__=="__main__":
    main()
    print("\n\n\033[32m...........all tasks done!!...........\033[0m\n")