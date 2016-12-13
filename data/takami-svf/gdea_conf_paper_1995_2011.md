# ファイルについて

- gdea_conf_paper_1995_2011.gml: NetworkX での読み込みでエラーが出たために、本当の大元のデータセットからラベル情報を除去したものだと思う。。。
- gdea_conf_paper_1995_2011.labels: データセットのラベル情報 --- 論文の著者名
- gdea_conf_paper_1995_2011_nographics.gml: iGraph での読み込みでエラーが出たために、`graphics` 構文を除去したもの。この作業のために以下のスクリプトを利用した。

    `sed '/^graphics/,/^]/d' gdea_conf_paper_1995_2011.gml > gdea_conf_paper_1995_2011_nographics.gml`
