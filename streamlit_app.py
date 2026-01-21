import streamlit as st
import pandas as pd
import io

# 1. ページの設定
st.set_page_config(
    page_title="日本全国 旅行先コンシェルジュ",
    page_icon="🗺️",
    layout="wide"
)

# --- 2. データの準備（有名な観光地を大幅追加） ---
csv_data = """region,name,tags,desc
北海道,知床,"自然, 絶景, 世界遺産",世界遺産の原生林と新鮮なカニ・イクラ。
北海道,富良野,"自然, 絶景, 映え",広大なラベンダー畑と丘の景色。メロンも絶品。
北海道,函館,"食べ物, 夜景, 歴史",五稜郭や朝市の海鮮丼。100万ドルの夜景。
東北,奥入瀬渓流,"自然, 絶景, 癒やし",美しい清流と苔むした岩々が続く、涼やかな散策路。
東北,松島,"絶景, 歴史, 食べ物",日本三景の一つ。松島湾の絶景と焼き牡蠣。
東北,銀山温泉,"温泉, 歴史, 映え",大正ロマンあふれる温泉街。冬の雪景色は絶景。
関東,浅草,"歴史, 食べ物, 都会",雷門や仲見世通りでの食べ歩きと下町情緒。
関東,箱根,"温泉, 自然, アート",芦ノ湖の絶景と温泉、美術館巡りも楽しめる人気エリア。
関東,日光,"歴史, 世界遺産, 自然",東照宮の豪華絢爛な建築と華厳の滝。
関東,鎌倉,"歴史, 海, 散策",大仏や古い寺院。江ノ電に乗って海辺の散策も。
中部,上高地,"自然, 絶景, 癒やし",日本屈指の山岳リゾート。澄んだ空気と清流。
中部,金沢,"食べ物, 歴史, 伝統文化",近江町市場の海鮮と、風情ある茶屋街の散策。
中部,白川郷,"世界遺産, 歴史, 絶景",合掌造りの集落。日本の原風景が残る場所。
中部,伊勢神宮,"歴史, パワースポット, 食べ物",日本人の心のふるさと。おかげ横丁での食べ歩き。
近畿,嵐山,"自然, 歴史, 散策",竹林の道や渡月橋。四季折々の景色と寺院巡り。
近畿,清水寺,"歴史, 世界遺産, 映え",「清水の舞台」で有名。参道の土産店巡りも楽しい。
近畿,奈良公園,"歴史, 自然, 癒やし",東大寺の大仏と、自由に歩き回るシカたち。
近畿,道頓堀,"食べ物, 都会, 賑やか",たこ焼き・お好み焼き。巨大看板が並ぶ大阪の象徴。
近畿,城崎温泉,"温泉, 食べ物, 散策",浴衣で外湯巡りを楽しめる温泉街とカニ料理。
中国,宮島,"歴史, 絶景, 世界遺産",海に浮かぶ大鳥居。焼き牡蠣やもみじ饅頭が名物。
中国,出雲大社,"歴史, パワースポット, 縁結び",縁結びの神様として知られる日本最古級の神社。
中国,鳥取砂丘,"自然, 絶景, アクティビティ",日本最大級の砂丘。ラクダ乗りやパラグライダー。
四国,小豆島,"自然, 映え, アート",瀬戸内海の穏やかな景色とオリーブ・うどん。
四国,道後温泉,"温泉, 歴史, アート",日本最古といわれる温泉。千と千尋のモデルとも。
四国,高知・桂浜,"自然, 歴史, 絶景",坂本龍馬像が立つ、太平洋を望む美しい砂浜。
九州,糸島,"自然, 食べ物, 映え",青い海と白い砂浜。おしゃれなカフェと牡蠣小屋。
九州,阿蘇,"自然, 絶景, ドライブ",世界最大級のカルデラと雄大な草原。
九州,別府温泉,"温泉, 食べ物, 癒やし",日本一の湧出量を誇る温泉郷。地獄蒸し料理が名物。
九州,由布院,"温泉, 映え, 散策",おしゃれな雑貨店やカフェが並ぶ、女性に人気の温泉地。
九州,屋久島,"自然, 絶景, 世界遺産",縄文杉。神秘的な苔の森が広がる世界遺産の島。
沖縄,石垣島,"自然, 絶景, 海",エメラルドグリーンの海と満天の星空。
沖縄,国際通り,"食べ物, 都会, お土産",沖縄料理の屋台や雑貨店がひしめく活気ある通り。
沖縄,美ら海水族館,"絶景, 家族向け, 自然",巨大なジンベエザメが泳ぐ、世界最大級の水槽。
"""

# --- 3. データの読み込み処理 ---
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

# --- 5. ユーザーインターフェース ---
st.title("🧳 日本全国 旅行先コンシェルジュ")
st.write("地域と「やりたいこと」を組み合わせて、次の旅先を見つけましょう！")

with st.sidebar:
    st.header("🔍 絞り込み条件")
    selected_region = st.selectbox("地域を選ぶ", options=sorted_regions)
    selected_tags = st.multiselect(
        "やりたいことを選ぶ",
        options=sorted_tags,
        default=["自然", "食べ物"]
    )
    strict_mode = st.checkbox("選択したタグをすべて満たす")

# --- 6. フィルタリング処理 ---
filtered_df = df.copy()

if selected_region != "すべて":
    filtered_df = filtered_df[filtered_df['region'] == selected_region]

if selected_tags:
    if strict_mode:
        mask = filtered_df['tags'].apply(lambda x: all(tag in x for tag in selected_tags))
    else:
        mask = filtered_df['tags'].apply(lambda x: any(tag in x for tag in selected_tags))
    filtered_df = filtered_df[mask]

# --- 7. 結果の表示 ---
st.subheader(f"おすすめの旅行先 ({len(filtered_df)}件)")

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
                        
                        # Google検索へのリンクボタンを追加
                        search_url = f"https://www.google.com/search?q={row['name']}+観光"
                        st.link_button(f"✨ {row['name']} を詳しく調べる", search_url)
else:
    st.warning("条件に合う場所が見つかりませんでした。別の条件を試してみてください！")

st.divider()
st.caption("© 2024 Travel Concierge App with Streamlit")
