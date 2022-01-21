# kuramoto-msr2022

## A description of the data source. <br>
- 
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
  9. python analyzer.py
  10. python analyzer_test.py

## A description of the storage mechanism, including a schema if applicable. <br>
- ?
## If the data has been used by the authors or others, a description of how this was done including references to previously published papers. <br>
- 該当しない
## A description of the originality of the data set (that is, even if the data set has been used in a published paper, its complete description must be unpublished) and similar existing datasets (if any) <br>
- 動画及び画像の添付数を調べるのは初（調査の限り）
## A description of the design of the tool, and how to use the tool in practice ideas for future research questions that could be answered using the data set. <br>
- 
## Ideas for further improvements that could be made to the data set. <br>
- ボットを取り除く工程の追加
- 複数のgithub-access-tokenを用いたデータの並列取得を可能にする
## Any limitations and/or challenges in creating or using the data set. <br>
- github-access-token の late-limit（5000requests/hour）の制約は極めて大きなネックになる
