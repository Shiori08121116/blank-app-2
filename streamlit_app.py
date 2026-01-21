import streamlit as st
import pandas as pd
import io

# 1. 必ず一番最初に書く（これより上に st.write などがあるとエラーになります）
st.set_page_config(
    page_title="旅行先コンシェルジュ",
    page_icon="🗺️",
    layout="wide"
)

# --- 2. データの準備 ---
csv_data = """region,name,tags,desc
北海道,知床,"自然, 食べ物, 絶景",世界遺産の原生林と新鮮なカニ・イクラ。
東北,奥入瀬渓流,"自然, 絶景, 癒やし",美しい清流と苔むした岩々が続く、涼やかな散策路。
関東,浅草,"歴史, 食べ物, 都会",雷門や仲見世通りでの食べ歩きと下町情緒。
関東,箱根,"温泉, 自然, 歴史",芦ノ湖の絶景と温泉、美術館巡りも楽しめる人気エリア。
中部,上高地,"自然, 絶景, 癒やし",日本屈指の山岳リゾート。澄んだ空気と清流。
中部,金沢,"食べ物, 歴史, 伝統文化",近江町市場の海鮮と、風情ある茶屋街の散策。
近畿,嵐山,"自然, 歴史, 散策",竹林の道や渡月橋。四季折々の景色と寺院巡り。
近畿,城崎温泉,"温泉, 食べ物, 散策",浴衣で外湯巡りを楽しめる温泉街とカニ料理。
中国,宮島,"歴史, 絶景, 食べ物",海に浮かぶ大鳥居と、焼き牡蠣やもみじ饅頭。
四国,小豆島,"自然, 食べ物, アート",瀬戸内海の穏やかな景色とオリーブ・うどん。
九州,糸島,"自然, 食べ物, インスタ映え",青い海と白い砂浜。おしゃれなカフェと牡蠣小屋。
九州,阿蘇,"自然, 絶景, ドライブ",世界最大級のカルデラと雄大な草原。
沖縄,石垣島,"自然, 絶景, マリンスポーツ",エメラルドグリーンの海と満天の星空。
"""

# --- 3. データの読み込み ---
@st.cache_data
def load_data():
    return pd.read_csv(io.StringIO(csv_data))

df = load_data()

# --- 4. 検索項目の準備 ---
all_tags = set()
for tags in df['tags'].str.split(','):
    for tag in tags:
        all_tags.add(tag.strip())
sorted_tags = sorted(list(all_tags))
sorted_regions = ["すべて"] + sorted(df['region'].unique().tolist())

# --- 5. UI（メイン画面とサイドバー） ---
st.title("🧳 日本全国 旅行先コンシェルジュ")

with st.sidebar:
    st.header("絞り込み条件")
    selected_region = st.selectbox("地域を選ぶ", options=sorted_regions)
    selected_tags = st.multiselect(
        "やりたいことを選ぶ",
        options=sorted_tags,
        default=["自然"]
    )
    strict_mode = st.checkbox("選択したタグをすべて満たす")

# --- 6. フィルタリング ---
filtered_df = df.copy()

if selected_region != "すべて":
    filtered_df = filtered_df[filtered_df['region'] == selected_region]

if selected_tags:
    if strict_mode:
        mask = filtered_df['tags'].apply(lambda x: all(tag in x for tag in selected_tags))
    else:
        mask = filtered_df['tags'].apply(lambda x: any(tag in x for tag in selected_tags))
    filtered_df = filtered_df[mask]

# --- 7. 表示 ---
st.subheader(f"🔍 おすすめの旅行先 ({len(filtered_df)}件)")

if not filtered_df.empty:
    for i in range(0, len(filtered_df), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(filtered_df):
                row = filtered_df.iloc[i + j]
                with cols[j]:
                    with st.container(border=True):
                        st.caption(f"📍 {row['region']}")
                        st.markdown(f"### {row['name']}")
                        st.write(row['desc'])
                        tag_labels = " ".join([f"`{t.strip()}`" for t in row['tags'].split(',')])
                        st.markdown(tag_labels)
else:
    st.warning("条件に合う場所が見つかりませんでした。")
