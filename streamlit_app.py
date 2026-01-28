import streamlit as st
import pandas as pd
from supabase import create_client, Client

# 1. ページ設定
st.set_page_config(page_title="旅行先コンシェルジュ Pro", page_icon="🗺️", layout="wide")

# 2. Supabase接続設定
@st.cache_resource
def init_connection():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_connection()

# 3. データの読み込み (Supabaseから取得)
@st.cache_data(ttl=600)
def load_data():
    response = supabase.table("travel_spots").select("*").execute()
    return pd.DataFrame(response.data)

df = load_data()

# 4. 検索項目の準備
all_tags = set()
for tags in df['tags'].str.split(','):
    for tag in tags:
        all_tags.add(tag.strip())
sorted_tags = sorted(list(all_tags))
sorted_regions = ["すべて"] + sorted(df['region'].unique().tolist())

# 5. UI (サイドバー)
st.title("🧳 日本全国 旅行先コンシェルジュ")

with st.sidebar:
    st.header("🔍 絞り込み条件")
    selected_region = st.selectbox("地域を選ぶ", options=sorted_regions)
    selected_tags = st.multiselect("やりたいこと", options=sorted_tags, default=[sorted_tags[0]])
    
    st.divider()
    st.subheader("⭐ 保存されたお気に入り")
    # 永続化されたデータを表示
    fav_res = supabase.table("favorites").select("spot_name").order("created_at", desc=True).execute()
    if fav_res.data:
        for f in fav_res.data:
            st.write(f"✅ {f['spot_name']}")
    else:
        st.caption("まだ保存されていません")

# 6. フィルタリング処理
filtered_df = df.copy()
if selected_region != "すべて":
    filtered_df = filtered_df[filtered_df['region'] == selected_region]
if selected_tags:
    mask = filtered_df['tags'].apply(lambda x: any(tag in x for tag in selected_tags))
    filtered_df = filtered_df[mask]

# --- 7. 結果の表示 (エラーを修正した完全版) ---
st.subheader(f"🔍 あなたの好みに合うおすすめ ({len(filtered_df)}件)")

# データが空っぽでないか確認
if not filtered_df.empty:
    # 2列ずつ表示するためのループ
    for i in range(0, len(filtered_df), 2):
        cols = st.columns(2)
        
        for j in range(2):
            # 表示するデータがまだ残っているか確認
            if i + j < len(filtered_df):
                # ここで「row」を定義します。これより下で row が使えます。
                row = filtered_df.iloc[i + j]
                
                with cols[j]:
                    with st.container(border=True):
                        # ここは row['region'] が使える範囲（インデントの中）です
                        st.caption(f"📍 {row['region']}")
                        st.markdown(f"### {row['name']}")
                        st.info(row['desc_text'])
                        
                        # キャプションをタブで詳しく表示
                        t1, t2 = st.tabs(["😋 ご当地グルメ", "✨ おすすめの魅力"])
                        with t1:
                            # row.get('カラム名') を使うと、もし列がなくてもエラーになりません
                            food = row.get('local_food', "情報を準備中...")
                            st.write(food if food else "情報を準備中...")
                        with t2:
                            site = row.get('recommended_site', "魅力を調査中...")
                            st.write(site if site else "魅力を調査中...")
                        
                        st.divider()
                        
                        # お気に入りボタン
                        if st.button(f"❤️ お気に入りに保存", key=f"fav_{row['id']}"):
                            supabase.table("favorites").insert({"spot_name": row['name']}).execute()
                            st.toast(f"{row['name']} を保存しました！")
                            st.rerun()
else:
    st.warning("条件に合う場所が見つかりませんでした。別のキーワードを選んでみてください。")
        
