import itertools
from datetime import datetime, timedelta

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from db import SessionLocal, WordSet


# AIで単語リストを生成する関数
def generate_words_list(n: int):
    model = ChatOpenAI(model="gpt-4o-2024-05-13")

    # 単語リスト生成のプロンプトテンプレート
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                f"ランダムに{n}個の単語を生成してください。1行に1単語ずつ出力してください。",
            ),
        ]
    )

    # 出力パーサーを設定
    parser = StrOutputParser()

    # チェーンの実行
    chain = prompt | model | parser
    result = chain.invoke({}).strip()

    # 結果をリストに分割して返す
    words = result.splitlines()
    return [word.strip() for word in words if word.strip()]


# 共通点を生成する関数
def generate_commonality(word1: str, word2: str) -> str:
    model = ChatOpenAI(model="gpt-4o-2024-05-13")

    # 共通点生成のプロンプトテンプレート
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "次の2つの単語の共通点を考えてください:"),
            ("user", f"単語1: {word1}, 単語2: {word2}"),
        ]
    )

    # 出力パーサーを設定
    parser = StrOutputParser()

    # チェーンの実行
    chain = prompt | model | parser
    result = chain.invoke({}).strip()
    return result


# 単語セットをデータベースに追加する関数
def add_word_sets(num=5, date_time=None):
    db = SessionLocal()

    # 日付が指定されていない場合は現在の日付を使用
    if date_time is None:
        date_time = datetime.now()

    # 10個の単語を生成
    word_list = generate_words_list(num)

    # 単語の組み合わせを生成 (ペアにする)
    word_pairs = list(itertools.combinations(word_list, 2))

    # 各ペアについて共通点を生成し、データベースに保存
    for word1, word2 in word_pairs:
        commonality = generate_commonality(word1, word2)
        db.add(
            WordSet(
                word1=word1, word2=word2, commonality=commonality, created_at=date_time
            )
        )

    db.commit()
    db.close()


# 1週間分の問題セットを追加する関数
def add_word_sets_for_week(num):
    today = datetime.now() + timedelta(days=1)

    # 1週間分の日付を使ってバッチ処理を行う
    for i in range(20):
        date_for_set = today + timedelta(days=i)
        print(f"Creating word sets for: {date_for_set.strftime('%Y-%m-%d')}")
        add_word_sets(num=num, date_time=date_for_set)


if __name__ == "__main__":
    # add_word_sets()
    add_word_sets_for_week(4)
