# --- Gemini API呼び出し（混雑自動回避・フォールバック機能付き） ---
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
1. 幹事決定のお祝いと挨拶（「{winner_name}さん、幹事おめでとうございます＆引き受けありがとうございます！」という人間に対する自然な挨拶）
2. 開催概要まとめ
3. 予算傾斜のアドバイス（誰がいくら払うべきかの目安提案）
4. {location}周辺でおすすめの店舗ジャンルやプラン提案（3パターンほど）
5. 参加者への案内文（LINE等にそのままコピペできるフォーマット）
"""

            with st.spinner("Geminiが最適な案内文を計算中..."):
                # 混雑時に試行するモデルの優先順位リスト
                candidate_models = [
                    'gemini-3.8-flash',
                    'gemini-2.0-flash',
                    'gemini-2.5-flash',
                    'gemini-1.5-flash'
                ]
                
                response = None
                last_error = None
                
                # 順に試して最初に成功したモデルの結果を採用する
                for model_name in candidate_models:
                    try:
                        response = client.models.generate_content(
                            model=model_name,
                            contents=prompt,
                        )
                        if response:
                            break
                    except Exception as e:
                        last_error = e
                        continue
                
                if response:
                    st.success("✈️ フライトプラン（幹事案内文）が完成しました！")
                    st.markdown("---")
                    st.markdown(response.text)
                else:
                    st.error(f"AIの混雑により生成に失敗しました。少し時間をおいて再試行してください: {last_error}")

        except Exception as e:
            st.error(f"API通信エラーが発生しました: {e}")
