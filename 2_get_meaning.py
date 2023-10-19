# words.db(SQLiteデータベース)に意味の登録が無いものをwikipediaから取得する。
# 曖昧な場合な場合はoptionに候補が保存されるので、それを参考にsubに補足の単語を入れてください。
# なおwords.db(SQLiteデータベース)の編集にはDB Browser for SQLite等を使用してください。
# word   : 登録したい単語
# sub    : 単語が曖昧な場合の補足(wikipediaの検索で曖昧場合こちらを使用)
# option : 曖昧な場合の補足候補(wikipediaで曖昧な場合の候補)
# meaning: 単語の意味
# pip install wikipedia
import re, sqlite3
import wikipedia

# SQLiteデータベースに接続
conn = sqlite3.connect('words.db')

# カーソルを取得
cur = conn.cursor()

# 言語を日本語に設定
wikipedia.set_lang("jp")

# データベースから登録されている単語を取得
cur.execute("SELECT word, sub FROM words WHERE meaning IS NULL")
words = cur.fetchall()

for word_tuple in words:
	word = word_tuple[0]
	sub  = word_tuple[1]

	# サブのワードがなければ
	if sub is None:
		try:
			# 検索ワードを用いて検索
			page = wikipedia.search(word)
			if page:
				meaning = str(wikipedia.summary(page[0]))
				meaning = re.sub('\n', '', meaning)
				print(meaning)

				# Wikipediaのサマリーを取得してデータベースを更新
				cur.execute("UPDATE words SET meaning=? WHERE word=?", (meaning, word))

				# 変更をコミット
				conn.commit()

		except wikipedia.exceptions.DisambiguationError as e:
			# 選択肢が複数ありあいまいな場合
			option = ",".join(e.options)
			print(option)

			# Wikipediaの選択肢を取得してデータベースを更新
			cur.execute("UPDATE words SET option=? WHERE word=?", (option, word))
			# 変更をコミット
			conn.commit()
			pass
	else:
		try:
			# サブワードを用いて検索
			page = wikipedia.search(sub)
			if page:
				meaning = str(wikipedia.summary(page[0]))
				meaning = re.sub('\n', '', meaning)
				print(meaning)

				# Wikipediaのサマリーを取得してデータベースを更新
				cur.execute("UPDATE words SET meaning=? WHERE word=?", (meaning, word))

				# 変更をコミット
				conn.commit()

		except:
			print("サブワードエラー")
			pass

# 接続を閉じる
conn.close()

print("単語の意味がデータベースに更新されました。")
