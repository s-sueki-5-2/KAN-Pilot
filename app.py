import streamlit as st
import time
import random
from google import genai

st.set_page_config(page_title="KAN-Pilot", page_icon="✈️", layout="centered")

st.title("✈️ KAN-Pilot (Gemini AI 直結版)")
st.caption("AI飲み会幹事ナビゲーション ＆ ネコレース")

# サイドバーにGemini API Keyの入力欄を設定
gemini_api_key = st.sidebar.text_input(
    "Gemini API Key", 
    type="password", 
    help="Google AI Studioで取得したAPIキーを入力してください"
)

with st.form("input_form"):
    st.subheader("📝 飲み会条件の入力")
    col1, col2 = st.columns(2)
    with col1:
        location = st.text_input("開催エリア", value="東京")
    with col2:
        target_dates = st.text_input("候補日時", value="2026/09/01 19:00")
        
    budget_list = st.text_area(
        "参加者と予算の目安", 
        value="Aさん: 8000円\nBさん: 5000円\nCさん: 5000円\nDさん: 7000円",
        height=120
    )
    allergies = st.text_input("アレルギー・NG食材", value="パクチー")
    decision_mode = st.selectbox("お店の決定方法", ["ネコレースで決定", "起案者が決める", "多数決"])
    
    submit_btn = st.form_submit_button("🏁 KAN-Pilot 出撃（ネコレース開始！）")

if submit_btn:
    if not gemini_api_key:
        st.error("左側のサイドバーに Gemini の API Key を入力してください！")
    else:
        # --- ネコレース演出 ---
        st.subheader("🐾 幹事決定ネコレース 開催中！")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        cats = ["ミケ🐈", "トラ🐈‍⬛", "タマ🐱", "レオ🐆"]
        for percent in range(100):
            time.sleep(0.02)
            progress_bar.progress(percent + 1)
            runner = cats[(percent // 5) % len(cats)]
            status_text.text(f"ネコたちが激走中... {runner} " + "💨" * (percent // 10))
            
        winner_cat = random.choice(cats)
        status_text.text(f"🏁 ゴール！ 幹事は {winner_cat} に決定！ AIがプランをフライト計算中...")

        # --- Gemini APIの呼び出し ---
        try:
            client = genai.Client(api_key=gemini_api_key)
            
            prompt = f"""
あなたは優秀な飲み会幹事AI「KAN-Pilot」です。
以下の条件に基づいて、参加者がワクワクするような最高の飲み会案内文とおすすめのお店案を作成してください。

【条件】
- 開催エリア: {location}
- 候補日時: {target_dates}
- 参加者と予算:
{budget_list}
- NG食材・アレルギー: {allergies}
- 決定方法のレース結果: 幹事は「{winner_cat}」に決定しました。

【出力形式】
1. 幹事決定のお祝いと挨拶
2. 開催概要まとめ
3. 予算傾斜のアドバイス（誰がいくら払うべきかの目安提案）
4. {location}周辺でおすすめの店舗ジャンルやプラン提案（3パターンほど）
5. 参加者への案内文（LINE等にそのままコピペできるフォーマット）
"""

            with st.spinner("Geminiが最適な案内文を生成中..."):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                st.success("✈️ フライトプラン（幹事案内文）が完成しました！")
                st.markdown("---")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"API通信エラーが発生しました: {e}")
