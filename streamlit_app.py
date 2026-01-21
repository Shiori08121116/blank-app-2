import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
st.write("最初の第一歩")
import streamlit as st
import pandas as pd

st.set_page_config(page_title="旅行先提案アプリ", layout="wide")

st.title("🌿 気分で選ぶ旅行先ガイド")
st.caption("「自然」「食べ物」「歴史」など、やりたいことを入力してください")

# 1. データの読み込み
# 本来は CSV から読み込みますが、ここではサンプル用に辞書で作ります
data = [
    {"name": "北海道・知床", "tags": "自然, 食べ物", "desc": "世界遺産の原生林と、カニ・イクラなどの絶景＆グルメ。"},
    {"name": "福岡・糸島", "tags": "自然, 食べ物", "desc": "青い海と白い砂浜。産直市場での新鮮な食材も魅力。"},
    {"name": "京都・嵐山", "tags": "自然, 歴史", "desc": "竹林の道や渡月橋。四季折々の景色と寺院巡り。"},
    {"name": "石川・金沢", "tags": "食べ物, 歴史", "desc": "近江町市場の海鮮と、風情ある茶屋街の散策。"},
]
df = pd.DataFrame(data)

# 2. ユーザー入力
query = st.text_input("例：自然と食べ物、歴史を感じたい など", placeholder="キーワードを入力...")

# 3. フィルタリング処理
if query:
    # ユーザーが入力したキーワードが含まれる行を抽出
    # (スペース区切りなどで複数の単語に対応させることも可能です)
    keywords = query.replace("と", " ").replace("、", " ").split()
    
    results = df[df['tags'].apply(lambda x: any(k in x for k in keywords))]

    # 4. 結果表示
    if not results.empty:
        st.subheader(f"「{query}」におすすめの旅行先")
        
        # カラムを使って綺麗に並べる
        cols = st.columns(len(results))
        for i, (index, row) in enumerate(results.iterrows()):
            with cols[i % len(cols)]:
                st.info(f"### {row['name']}")
                st.write(row['desc'])
                st.caption(f"タグ: {row['tags']}")
    else:
        st.warning("該当する場所が見つかりませんでした。別のキーワードを試してみてください。")

else:
    st.write("左の検索窓にキーワードを入れてみてください。")
