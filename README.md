wikipediaで検索をするのでライブラリをインストールしてください。
pip install wikipedia

1_import_words.py:
  words.db(SQLiteデータベース)を作成して、words.txtを登録する。

2_get_meaning.py:
  words.db(SQLiteデータベース)に意味の登録が無いものをwikipediaから取得する。

3_input_words.py:
  words.db(SQLiteデータベース)に入力した単語を登録する

words.db:
  単語を登録したSQLiteのデータベース

words.txt:
  一行ごとに単語を書き、1_import_words.pyで読み込ませて登録します。
