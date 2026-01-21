import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
st.write("最初の第一歩")
import streamlit as st
import pandas as pd


import streamlit as st
import pandas as pd
import io

# ページの設定
st.set_page_config(
    page_title="旅行先コンシェルジュ",
    page_icon="✈️",
    layout="centered"
)

# --- 1. データの準備 ---
# レパートリーを増やす場合は、この文字列の中に項目を追加していくだけでOKです！
csv_data = """name,tags,desc
北海道・知床,"自然, 食べ物, 絶景",世界遺産の原生林と新鮮なカニ・イクラ。
福岡・糸島,"自然, 食べ物, インスタ映え",青い海と白い砂浜。おしゃれなカフェと牡蠣小屋。
京都・嵐山,"自然, 歴史, 散策",竹林の道や渡月橋。四季折々の景色と寺院巡り。
石川・金沢,"食べ物, 歴史, 伝統文化",近江町市場の海鮮と、風情ある茶屋街の散策。
長野・上高地,"自然, 絶景, 癒やし",日本屈指の山岳リゾート。澄んだ空気と清流。
沖縄・石垣島,"自然, 絶景, マリンスポーツ",エメラルドグリーンの海と満天の星空。
香川・小豆島,"自然, 食べ物, アート",瀬戸内海の穏やかな景色とオリーブ・うどん。
広島・宮島,"歴史, 絶景, 食べ物",海に浮かぶ大鳥居と、焼き牡蠣やもみじ饅頭。
山梨・富士五湖,"自然, 絶景, 富士山",富士山を間近に望む絶景スポットとキャンプ。
東京・浅草,"歴史, 食べ物, 都会",雷門や仲見世通りでの食べ歩きと下町情緒。
兵庫・城崎温泉,"温泉, 食べ物, 散策",浴衣で外湯巡りを楽しめる温泉街とカニ料理。
熊本・阿蘇,"自然, 絶景, ドライブ",世界最大級のカルデラと雄大な草原。
"""

# --- 2. データの読み込み処理 ---
@st.cache_data
def load_data():
    df = pd.read_csv(io.StringIO(csv_data))
    return df

df = load_data()

# --- 3. タグの自動抽出 ---
# データに含まれる全てのタグを重複なく取り出す
all_tags = set()
for tags in df['tags'].str.split(','):
    for tag in tags:
        all_tags.add(tag.strip())
sorted_tags = sorted(list(all_tags))

# --- 4. ユーザーインターフェース ---
st.title("🧳 気分で選ぶ旅行先コンシェルジュ")
st.write("「何をしたいか」を選んでください。ぴったりの場所を提案します。")

# 複数選択ボックス
selected_tags = st.multiselect(
    "興味のあるキーワードを選んでください（複数選択可）",
    options=sorted_tags,
    default=["自然", "食べ物"]
)

# 絞り込みの条件設定（「いずれかを含む」か「すべて含む」か）
strict_mode = st.checkbox("選択した条件をすべて満たす場所のみ表示する")

# --- 5. フィルタリングと表示 ---
if selected_tags:
    if strict_mode:
        # すべての選択タグが含まれているか確認
        mask = df['tags'].apply(lambda x: all(tag in x for tag in selected_tags))
    else:
        # いずれかの選択タグが含まれているか確認
        mask = df['tags'].apply(lambda x: any(tag in x for tag in selected_tags))
    
    filtered_df = df[mask]

    st.divider()
    st.subheader(f"🔍 おすすめの旅行先 ({len(filtered_df)}件)")

    if not filtered_df.empty:
        # 結果を表示
        for index, row in filtered_df.iterrows():
            with st.container():
                # デザインを整えるための枠組み
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.info(f"📍 **{row['name']}**")
                with col2:
                    st.write(row['desc'])
                    # タグをバッジ風に表示
                    tag_list = row['tags'].split(',')
                    st.caption(" ".join([f"#{t.strip()}" for t in tag_list]))
                st.divider()
    else:
        st.warning("条件に一致する場所が見つかりませんでした。条件を減らしてみてください。")
else:
    st.info("キーワードを選択してください。")

# --- 6. フッター ---
st.caption("© 2024 旅行先提案アプリ - Streamlitで作られたデモ")
