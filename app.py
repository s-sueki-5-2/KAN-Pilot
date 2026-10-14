import streamlit as st
import time
import random
from google import genai

st.set_page_config(page_title="KAN-Pilot", page_icon="✈️", layout="centered")

st.title("✈️ KAN-Pilot (ネコ指名レース版)")
st.caption("AI飲み会幹事ナビゲーション ＆ 幹事決定ネコレース")

# サイドバーにGemini API Keyの入力欄を設定
gemini_api_key = st.sidebar.text_input(
    "Gemini API Key", 
    type="password", 
    help="Google AI Studio等で取得したAPIキーを入力してください"
)

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
        height=100
    )
    allergies = st.text_input("アレルギー・NG食材", value="パクチー")
    
    st.subheader("🐾 参加者の代理ネコを選択")
    st.caption("各参加者がエントリーするネコを選んでください（1着のネコの担当者が幹事になります！）")
    
    cat_options = ["ミケ🐈", "トラ🐈‍⬛", "タマ🐱", "レオ🐆", "クロ🐈‍⬛", "シロ🐱"]
    
    c1, c2 = st.columns(2)
    with c1:
        p1_name = st.text_input("参加者1の名前", value="Aさん")
        p1_cat = st.selectbox(f"{p1_name}のネコ", cat_options, index=0, key="cat1")
        
        p2_name = st.text_input("参加者2の名前", value="Bさん")
        p2_cat = st.selectbox(f"{p2_name}のネコ", cat_options, index=1, key="cat2")
        
    with c2:
        p3_name = st.text_input("参加者3の名前", value="Cさん")
        p3_cat = st.selectbox(f"{p3_name}のネコ", cat_options, index=2, key="cat3")
        
        p4_name = st.text_input("参加者4の名前", value="Dさん")
        p4_cat = st.selectbox(f"{p4_name}のネコ", cat_options, index=3, key="cat4")
        
    submit_btn = st.form_submit_button("🏁 出撃（幹事決定ネコレース開始！）")

if submit_btn:
    if not gemini_api_key:
        st.error("左側のサイドバーに Gemini の API Key を入力してください！")
    else:
        # エントリー情報の整理
        participants = [
            {"name": p1_name, "cat": p1_cat},
            {"name": p2_name, "cat": p2_cat},
            {"name": p3_name, "cat": p3_cat},
            {"name": p4_name, "cat": p4_cat},
        ]
        
        # --- ネコレース演出 ---
        st.subheader("🐾 幹事決定ネコレース 開催中！")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for percent in range(100):
            time.sleep(0.02)
            progress_bar.progress(percent + 1)
            current_runner = participants[(percent // 5) % len(participants)]
            status_text.text(f"ネコたちが激走中... {current_runner['name']}の{current_runner['cat']} " + "💨" * (percent // 10))
            
        # ランダムで優勝者を決定
        winner = random.choice(participants)
        winner_name = winner["name"]
        winner_cat = winner["cat"]
        
        status_text.text(f"🏁 ゴール！ 1着は {winner_name} の【{winner_cat}】！ 幹事は {winner_name} に決定！")
        st.balloons()
        time.sleep(1)

        # --- Gemini API呼び出し ---
        try:
            client = genai.Client(api_key=gemini_api_key)
            
            prompt = f"""
あなたは優秀な飲み会幹事AI「KAN-Pilot」です。
以下の条件に基づいて、参加者がワクワクするような最高の飲み会案内文とおすすめのお店案を作成してください。

【状況設定】
- 幹事決定レースにおいて、{winner_name}さんの代理ネコ「{winner_cat}」が1着でゴールしたため、今回の幹事は「{winner_name}さん」に決定しました。

【条件】
- 幹事: {winner_name}さん
- 開催エリア: {location}
- 候補日時: {target_dates}
- 参加者と予算:
{budget_list}
- NG食材・アレルギー: {allergies}

【出力形式】
1. 幹事決定のお祝いと挨拶（「{winner_name}さん、幹事おめでとうございます＆引き受けありがとうございます！」という人間に対する自然な挨拶にしてください）
2. 開催概要まとめ
3. 予算傾斜のアドバイス（誰がいくら払うべきかの目安提案）
4. {location}周辺でおすすめの店舗ジャンルやプラン提案（3パターンほど）
5. 参加者への案内文（LINE等にそのままコピペできるフォーマット）
"""

            with st.spinner("Geminiが最適な案内文を生成中..."):
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=prompt,
                )
                
                st.success("✈️ フライトプラン（幹事案内文）が完成しました！")
                st.markdown("---")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"API通信エラーが発生しました: {e}")
