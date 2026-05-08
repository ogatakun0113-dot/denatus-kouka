import streamlit as st

# --- ページ設定 ---
st.set_page_config(page_title="ケーブル電圧降下計算アシスト", layout="centered")

# --- 見た目の設定（CSS） ---
st.markdown("""
    <style>
    /* クレジット表示用のCSS */
    .credit {
        text-align: right;
        font-size: 14px;
        color: #666;
        margin-bottom: -20px;
    }
    /* 入力欄のラベルスタイル */
    .stNumberInput label, .stSelectbox label {
        font-size: 18px !important;
        color: #8B4513 !important; /* 銅線イメージの茶色 */
        font-weight: 800 !important;
    }
    /* 計算結果ボックス */
    .result-box {
        background-color: #fffaf0;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #8B4513;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 右上にクレジットを表示
st.markdown('<p class="credit">開発/制作：緒方</p>', unsafe_allow_html=True)

st.title('📏 ケーブル電圧降下計算アシスト')
st.caption("※内線規程の簡易式に基づく算出（銅導体）")
st.markdown("---")

# --- 1. 基本設定 ---
col_opt1, col_opt2 = st.columns(2)
with col_opt1:
    phase = st.selectbox("配電方式を選択", ["単相2線式 (1Φ2W)", "単相3線式 (1Φ3W)", "三相3線式 (3Φ3W)"])
with col_opt2:
    v_base = st.number_input("基準電圧 (V)", value=100.0 if "単相" in phase else 200.0, step=1.0)

# 係数 K の設定
# 単相2線: 30.8, 単相3線/三相3線: 17.8
if phase == "単相2線式 (1Φ2W)":
    k_factor = 30.8
else:
    k_factor = 17.8

st.markdown("---")

# --- 2. 入力セクション ---
col_in1, col_in2 = st.columns(2)
with col_in1:
    current = st.number_input("負荷電流 I (A)", value=15.0, step=1.0, format="%.2f")
    length = st.number_input("電線路の長さ L (m)", value=20.0, step=1.0, format="%.1f")
with col_in2:
    # 一般的な電線サイズ (sq)
    sq_list = [0.75, 1.25, 2, 3.5, 5.5, 8, 14, 22, 38, 60, 100, 150, 200, 250, 325]
    sq = st.selectbox("電線断面積 A (sq)", sq_list, index=2) # デフォルト 2sq

# --- 3. 計算ロジック ---
# 電圧降下 e = (K * L * I) / (1000 * A)
v_drop = (k_factor * length * current) / (1000 * sq)
# 降下率 (%)
drop_rate = (v_drop / v_base) * 100

# --- 4. 結果表示 ---
st.markdown('<div class="result-box">', unsafe_allow_html=True)
st.subheader("📊 計算結果")

c_res1, c_res2 = st.columns(2)
with c_res1:
    st.metric("電圧降下 (e)", f"{v_drop:.2f} V")
with c_res2:
    # 基準として3%以内を青、それ以上を赤にする等の工夫も可能
    st.metric("電圧降下率", f"{drop_rate:.2f} %")

st.write(f"（条件）{phase} / {sq} sq / {length} m / {current} A")
st.markdown('</div>', unsafe_allow_html=True)

# 補足情報
with st.expander("ℹ️ 計算式について"):
    st.write(f"""
    本アプリでは、以下の簡易式（銅導体・導体温度75℃想定）を使用しています。
    - **単相2線式**: $e = 30.8 \cdot L \cdot I / (1000 \cdot A)$
    - **単相3線式・三相3線式**: $e = 17.8 \cdot L \cdot I / (1000 \cdot A)$

    # --- 画面下部中央に「戻る」ボタンを配置 ---
st.markdown("---")  # 区切り線
col1, col2, col3 = st.columns([1, 1, 1])

with col2:  # 中央の列を使用
    # 水色のアイコン（🏠）と「戻る」を表示するボタン
    if st.link_button("🏠\n\n戻る", "https://menue3-pkwzfkwnoxnnuljkqg7mdt.streamlit.app/", use_container_width=True):
        pass

# ボタンの色（水色）を調整するカスタム設定
st.markdown("""
    <style>
    div.stLinkButton > a {
        background-color: #00BFFF !important; /* 水色（DeepSkyBlue） */
        color: white !important;
        border-radius: 10px;
        text-align: center;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    ※単相3線式の場合、電圧降下(e)は外線と中性線間の値となります。
    """)


