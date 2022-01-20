# kuramoto-msr2022
2022投稿予定の論文が以下の複数のリポジトリで更新されている状態です．<br>
随時同期していますが，タイミングによっては最新ではない場合があります．

- posl / kuramoto-github-video　　
- posl / msr2022　　

# Data Showcase
## MSR Data showcase submissions are expected to include:

### A description of the data source. <br>

### A description of the methodology used to gather the data (including provenance and the tool used to create/generate/gather the data, if any). <br>
[pyGitHub](https://pygithub.readthedocs.io/en/latest/introduction.html)を用いてデータを収集した．
  
本調査のデータの取得手順は以下（出力先：`src/out_for_issue/`）
  1. 本リポジトリのクローン
  2. `src/github-token.config`にGitHubアクセストークンを入れておく
      <br>アクセストークンは，(GitHub)Setting > Developer settings > personal_access_token > Generate new token
  4. `src/results.csv`に取得したいリポジトリ名を入力（カンマ区切り値） <br> (Example)
      ~~~
      org_name/repo_name,
      sunchit/coding-decoded,
      codenameone/codenameone,
      ssynhtn/wave-view,
      hmage/norm,
      airar-dev/unity-ar-colormapping,
      vulcanjs/vulcanjs-cli,
      swapmyvote/swapmyvote,
      parrit/parrit,
      fingerprintjs/fingerprintjs,
      gokrazy/breakglass
      ~~~
      `org_name/repo_name`は例えば，`posl/kuramoto-msr2022`
  5. python parser_for_issue.py
  6. python body2word.py
  7. python tf-idf.py

### A description of the storage mechanism, including a schema if applicable. <br>
### If the data has been used by the authors or others, a description of how this was done including references to previously published papers. <br>
### A description of the originality of the data set (that is, even if the data set has been used in a published paper, its complete description must be unpublished) and similar existing datasets (if any) <br>
### A description of the design of the tool, and how to use the tool in practice ideas for future research questions that could be answered using the data set. <br>
### Ideas for further improvements that could be made to the data set. <br>
### Any limitations and/or challenges in creating or using the data set. <br>
