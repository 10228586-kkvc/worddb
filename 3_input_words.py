# words.db(SQLiteデータベース)に入力した単語を登録する
# word   : 登録したい単語
# sub    : 単語が曖昧な場合の補足(wikipediaの検索で曖昧場合こちらを使用)
# option : 曖昧な場合の補足候補(wikipediaで曖昧な場合の候補)
# meaning: 単語の意味
# pip install wikipedia
import sqlite3
import wikipedia

# SQLiteデータベースに接続
conn = sqlite3.connect('words.db')
cur = conn.cursor()

# テーブルが存在しない場合は作成
cur.execute('''CREATE TABLE IF NOT EXISTS words (word TEXT PRIMARY KEY, sub TEXT, option TEXT, meaning TEXT)''')


while True:
	# ユーザーから単語を入力
	word = input("単語を入力してください（終了する場合はqを入力）: ")

	if word != '':

		# 終了条件をチェック
		if word.lower() == 'q':
			break

		# データベース内で単語を検索
		cur.execute("SELECT * FROM words WHERE word=?", (word,))
		existing_word = cur.fetchone()

		# 単語が存在しない場合は新しい単語を登録
		if existing_word is None:
			try:
				# 検索ワードを用いて検索
				page = wikipedia.search(word)
				if page:
					meaning = str(wikipedia.summary(page[0]))
					meaning = re.sub('\n', '', meaning)
					print(meaning)

					# Wikipediaのサマリーを取得してデータベースを更新
					cur.execute("INSERT INTO words (word, meaning) VALUES (?, ?)", (word, meaning))

					# 変更をコミット
					conn.commit()
				else:
					# Wikipediaの選択肢を取得してデータベースを更新
					cur.execute("INSERT INTO words (word) VALUES (?)", (word))

					# 変更をコミット
					conn.commit()
					pass

			except wikipedia.exceptions.DisambiguationError as e:
				# 選択肢が複数ありあいまいな場合
				option = ",".join(e.options)
				print(option)

				# Wikipediaの選択肢を取得してデータベースを更新
				cur.execute("INSERT INTO words (word, option) VALUES (?, ?)", (word, option))


				# 変更をコミット
				conn.commit()
				pass

			except:
				# Wikipediaの選択肢を取得してデータベースを更新
				cur.execute("INSERT INTO words (word) VALUES (?)", (word))

				# 変更をコミット
				conn.commit()
				pass

			print(f"{word}がデータベースに登録されました。")
		else:
			print(f"{word}は既にデータベースに存在します。")

# 接続を閉じる
conn.close()
