# CsvDownloader

## 概要
「SpreadSheetにGoogleDriveの画像リンクを各自張り付けてねー」形式にしたら、100個以上あるリンクから画像を一つ一つDLするのがダルすぎて死にそうだった（自分のせいでもある）。<br>
ということで、SpreadSheetのCSVをダウンロードして食わせると自動でGoogle DriveからのURLをスクレイピングしてローカルにダウンロードする処理を書いてみた。

## 既知の問題・バグ・改善点（ビッグバグを残しているので先頭に）
死ぬほどバグがある。その中でもわかっていて直せてないバグは以下の通り。

| 問題 | 内容 | 優先度 |
| :-- | :-- | :-- |
| Googleさん頼んます問題 | ダウンロードを回し続けると、なんと78リクエスト目くらいで「403 Forbidden」を食らってしまう！！ | 💀💀 |
| たびたびファイルが正しくDLされない問題 | たびたびファイルが正しくDLされない問題、原因調査中 | ★★★ |
| DL速度が遅い問題 | なんでだろうね | ★☆☆ |
| エラーログ間違い問題 | 初めのファイル指定で、入力を間違えても全部「that is not a directory path. type again」と吐かれる。うざいので直す | ★☆☆ |

## 仕様
- 開発環境
  - Python 3.7.6
- 開発OS
  - Windows 10 pro
- 対応ファイル形式
  - 画像
    - jpg
    - png
    - etc.
  - プロジェクトファイル
    - psd

## 使い方
### 実行環境
Python 3の実行環境から実行してください。<br>
Windowsで開発してますが、たぶんMacでも動くと思う。<br>
リポジトリの構造は以下の通り
- root
  - csv_downloader.py (ソースファイル、これを実行する)
  - README.md (readmeファイル)

### 対応しているファイル構造
原則として対象はCSVファイルで、かつ以下のような一列目二列目はヘッダで、三列目以降にリンクが来るようなもの。<br>
リンクの数はいくつでもよく、行ごとにバラバラでもよい。<br>
※リンクは必ずGoogleDriveの共有リンクでなければならない。あの、GoogleDriveでファイルを右クリックして「共有可能なリンクを作成」みたいなので取得できるやつ。

| クラス | 個人名 | リンク1 | リンク2 | ... | リンクn |
| :-- | :-- | :-- | :-- | :-- | :-- |
| クラス1 | おかもと | url_1_1 | url_1_2 | ... | url_1_n |
| | たかはし | url_2_1 | url_2_2 | ... | url_2_n |
| | さいとう | url_3_1 | | | |
| クラス2 | たなか | url_4_1 | url_4_2 | url_4_3 | |
| | ベッキー | url_5_1 | url_5_2 | ... | url_5_n |

### 結果
上のCSVファイルで実行すると、指定したディレクトリに以下のようなファイル群が生成される。
- file download 202x_mt_dd_hh_mn_sc
  - クラス1
    - おかもと
      - ファイルたち
    - たかはし
    - さいとう
  - クラス2
    - たなか
    - ベッキー

### 実行方法
Python 3がインストールされているPCで、コマンドラインからダウンロードもしくはクローンしたディレクトリを開き、
``` 
$ python csv_downloader.py
 ```
と実行する。すると、3つの質問が効かれる。
```
$ python csv_downloader.py
input file path?
$ ~/Desctop/file.csv  <= 食わせたいcsvファイルのパス
output directory? (brank means D:\sistem\Programing\GitHub\CsvDownloader)
$ ~/Desctop/output    <= 出力したい、存在するディレクトリ。入力せずエンターで上記のパスが指定される。
ignore lines? (split with space, start with 1)
1 2 15                <= ヘッダーなどで無視したい行があれば指定。スペースで区切る。
```

質問の途中に```exit()```を押すと、実行が終了します。<br>
それぞれに回答してエンターを押すと、自動的にディレクトリを生成してダウンロードを始めます。<br>
制作展から来た人は、必ず```ignore lines?```に```1 2 15```を指定してください。
