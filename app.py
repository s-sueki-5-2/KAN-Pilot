import streamlit as st
import requests
import time

# --- 画面設定 ---
st.set_page_config(page_title="KAN-Pilot", page_icon="✈️", layout="centered")

st.title("✈️ KAN-Pilot (Webアプリ版)")
st.caption("AI飲み会幹事ナビゲーション ＆ ネコレース")

# --- API Keyの自動取得（Secretsから優先取得、無ければ入力欄を表示） ---
api_key = st.secrets.get("DIFY_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("Dify API Key", type="password", help="設定されていない場合はここに入力してください")

# --- メインフォーム ---
with st.form("input_form"):
    st.subheader("📝 飲み会条件の入力")
    
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("開催エリア", value="門前仲町")
    with col2:
        target_dates = st.text_input("候補日時", value="2026/09/01 19:00")
        
    budget_list = st.text_area(
        "参加者と予算の目安", 
        value="Aさん: 8000円\nBさん: 5000円\nCさん: 5000円\nDさん: 7000円",
        height=120
    )
    
    allergies = st.text_input("アレルギー・NG食材", value="パクチー")
    decision_mode = st.selectbox("お店の決定方法", ["あみだくじ", "起案者が決める", "AIにおまかせ"])
    
    submit_btn = st.form_submit_button("🏁 KAN-Pilot 出撃（ネコレース開始！）")

# --- 処理実行 ---
if submit_btn:
    if not api_key:
        st.error("API Key が設定されていません。")
    else:
        # --- ネコレース演出 ---
        st.subheader("🐾 幹事決定ネコレース 開催中！")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        cat_emojis = ["🐈‍⬛", "🐈", "🐱", "🐆"]
        for percent_complete in range(100):
            time.sleep(0.02)
            progress_bar.progress(percent_complete + 1)
            cat = cat_emojis[(percent_complete // 5) % len(cat_emojis)]
            status_text.text(f"ネコたちが激走中... {cat} " + "💨" * (percent_complete // 10))
            
        status_text.text("🏁 ネコたちがゴールインしました！レポートを生成中...")

        # --- Dify API呼び出し ---
        url = "https://api.dify.ai/v1/workflows/run"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": {
                "location": location,
                "target_dates": target_dates,
                "budget_list": budget_list,
                "allergies": allergies,
                "decision_mode": decision_mode
            },
            "response_mode": "blocking",
            "user": "web_app_user"
        }

        try:
            with st.spinner("AIが最適プランをフライト計算中..."):
                res = requests.post(url, headers=headers, json=payload)
                data = res.json()
                
                if res.status_code == 200:
                    report = data.get("data", {}).get("outputs", {}).get("text", "")
                    st.success("✈️ フライトプランが完成しました！")
                    st.markdown("---")
                    st.markdown(report)
                else:
                    st.error(f"APIエラー: {data.get('message', '不明なエラー')}")
        except Exception as e:
            st.error(f"通信エラー: {e}")