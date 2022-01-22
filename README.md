# kuramoto-msr2022

## A description of the data source. <br>
データセットの調査項目は以下の8つ
（$はpygithubより直接取得可能）
- issue_open_time <br>
    $repo.issue.created_at <br>
    $repo.issue.closed_at <br>
    以上の差分を求めて取得（ともにpython.Datetimeクラス）
- first_comment_time <br>
    $repo.issue.created_at <br>
    $repo.issue.comment.created_at <br>
    以上の差分を求めて取得（ともにpython.Datetimeクラス）
- num_of_comments <br>
    for i in $repo.issue.comments: <br>
      num_of_comment += 1
- num_of_char <br>
    len( $repo.issue.body ) <br>
    ただし，動画及び画像URLは事前に除く
- num_of_img <br>
    $repo.issue.bodyから正規表現で取得 <br>
    XXX.mp4では不十分 <br>
    ログ貼り付けたものも含まれていまう <br>
    https://user-images.githubusercontent.com/XXX.拡張子 で取得する
- num_of_mov <br>
    $repo.issue.bodyから正規表現で取得 <br>
    https://user-images.githubusercontent.com/XXX.拡張子 で取得する
- words <br>
    $repo.issue.bodyから正規表現[\w]+で取得 <br>
    注意) it's　==>> (it, s) 
- issue_created_at_year <br>
    at = $repo.issue.created_at <br>
    at.yearで取得
## A description of the methodology used to gather the data (including provenance and the tool used to create/generate/gather the data, if any). <br>
[pyGitHub](https://pygithub.readthedocs.io/en/latest/introduction.html)を用いてデータを収集した．
  
本調査のデータの取得手順は以下（出力先：`src/out_for_issue/`）
  1. 本リポジトリのクローン
  2. `src/config/github-token.config`にgithub-access-tokenを入れておく
      <br>github-access-tokenは，(GitHub)Setting > Developer settings > personal_access_token > Generate new token
  3. `src/results.csv`に取得したいリポジトリ名を入力（カンマ区切り値） <br> (Example)
      ~~~
      repo_name <- 最初の行はそのまま（書いても実行されない）
      sunchit/coding-decoded
      codenameone/codenameone
      ssynhtn/wave-view
      hmage/norm
      ~~~
      また，最初の列のみ参照されるため，以下の様な形式でも構わない
      ~~~
      repo_name             , num_of_star , url             , ....
      sunchit/coding-decoded, 10          , ht_tps://~~~~~~ , ....
      ~~~
      
      `org_name/repo_name`は例えば，`posl/kuramoto-msr2022`
  4. Docker container起動（以下，コンテナ内で行う）
  5. python parser_for_issue.py
  6. python body2word.py
  7. python tf-idf.py
  8. python data_shaper.py
  9. python count_up.py
  10. python analyzer.py
  11. python analyzer_test.py

~~~
データセットの調査項目は以下の8つ
（$はpygithubより直接取得可能）
- issue_open_time
    $repo.issue.created_at
    $repo.issue.closed_at 
    以上の差分を求めて取得（ともにpython.Datetimeクラス）
- first_comment_time 
    $repo.issue.created_at 
    $repo.issue.comment.created_at 
    以上の差分を求めて取得（ともにpython.Datetimeクラス）
- num_of_comments 
    for i in $repo.issue.comments: 
      num_of_comment += 1
- num_of_char 
    len( $repo.issue.body ) 
    ただし，動画及び画像URLは事前に除く
- num_of_img 
    $repo.issue.bodyから正規表現で取得 
    XXX.mp4では不十分 
    ログ貼り付けたものも含まれていまう 
    https://user-images.githubusercontent.com/XXX.拡張子 で取得する
- num_of_mov 
    $repo.issue.bodyから正規表現で取得 
    https://user-images.githubusercontent.com/XXX.拡張子 で取得する
- words 
    $repo.issue.bodyから正規表現[\w]+で取得 
    注意) it's　==>> (it, s) 
- issue_created_at_year
    at = $repo.issue.created_at
    at.yearで取得
~~~

## A description of the storage mechanism, including a schema if applicable. <br>
- ?
## If the data has been used by the authors or others, a description of how this was done including references to previously published papers. <br>
- 該当しない
## A description of the originality of the data set (that is, even if the data set has been used in a published paper, its complete description must be unpublished) and similar existing datasets (if any) <br>
- 動画及び画像の添付数を調べるのは初（調査の限り）
## A description of the design of the tool, and how to use the tool in practice ideas for future research questions that could be answered using the data set. <br>
- さまざまなパラメータの関係性を分析できる
- 動画及び画像を含む時の出単語分析から報告者の心理状況を分析するなど，行動経済学にも応用できる可能性がある．
## Ideas for further improvements that could be made to the data set. <br>
- ボットを取り除く工程の追加
- 複数のgithub-access-tokenを用いたデータの並列取得を可能にする
## Any limitations and/or challenges in creating or using the data set. <br>
- github-access-token の late-limit（5000requests/hour）の制約は極めて大きなネックになる
