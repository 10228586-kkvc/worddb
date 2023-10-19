# words.db(SQLiteデータベース)を作成して、words.txtを登録する。
# 実行される度に単語が追加されます。
# word   : 登録したい単語
# sub    : 単語が曖昧な場合の補足(wikipediaの検索で曖昧場合こちらを使用)
# option : 曖昧な場合の補足候補(wikipediaで曖昧な場合の候補)
# meaning: 単語の意味
import sqlite3

# SQLiteデータベースに接続
conn = sqlite3.connect('words.db')

# カーソルを取得
cur = conn.cursor()

# テーブルを作成（存在しない場合）
# （word:登録したい単語, sub:単語が曖昧な場合の補足, option:曖昧な場合の補足候補, meaning:単語の意味）
cur.execute('''CREATE TABLE IF NOT EXISTS words (word TEXT PRIMARY KEY, sub TEXT, option TEXT, meaning TEXT)''')

# テキストファイルから単語を読み込んでデータベースに登録
with open('words.txt', 'r', encoding="utf-8") as file:
	for line in file:
		word = line.strip()  # 改行文字を取り除く
		# 重複する単語が存在しない場合のみ登録
		cur.execute("SELECT * FROM words WHERE word=?", (word,))
		existing_word = cur.fetchone()
		if existing_word is None:
			cur.execute("INSERT INTO words (word) VALUES (?)", (word,))

# 変更をコミット
conn.commit()

# 接続を閉じる
conn.close()

print("単語がデータベースに登録されました。")
