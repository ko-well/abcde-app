import streamlit as st
import google.generativeai as genai

# --- ページ設定とデザイン ---
st.set_page_config(page_title="ABCDE理論 思考の変換サポートAI", layout="wide")

st.markdown("""
<style>
h1, h2, h3 { color: #1A5276 !important; }
label p, [data-testid="stWidgetLabel"] p { font-size: 18px !important; color: #2874A6 !important; font-weight: bold !important; }
[data-testid="stFormSubmitButton"] { display: flex; justify-content: center; margin-top: 20px; margin-bottom: 20px; }
[data-testid="stFormSubmitButton"] button { background-color: #E67E22 !important; color: white !important; font-size: 20px !important; font-weight: bold !important; padding: 15px 50px !important; border-radius: 10px !important; border: none !important; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
[data-testid="stFormSubmitButton"] button:hover { background-color: #D35400 !important; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

st.title("ABCDE理論 思考の変換サポートAI")
st.write("モヤモヤする出来事と思い込みを入力すると，AIが客観的な視点で「合理的な思考」への変換をサポートします。")

# --- はじめての方へ（APIキー入力） ---
with st.expander("🔑 ご利用には無料のAPIキーが必要です（取得方法はこちら）", expanded=False):
    st.markdown("""
    **Q. 「API（エーピーアイ）」って何ですか？** A. このアプリの画面と，裏側で客観的な視点を提供する「AI（頭脳）」を安全に繋ぐための「専用の直通電話」のようなものです。この高性能なAIを無料で利用していただくための「通行手形」として，利用者様ご自身に取得をお願いしております。（※もちろん料金が発生することはありませんので，ご安心ください）

    ---
    **【図解】無料APIキーの取得手順（所要時間：約3分）**
    
    **ステップ1：Google AI Studioにアクセス** Googleアカウントにログインした状態で，[Google AI Studio](https://aistudio.google.com/) にアクセスします。

    **ステップ2：APIキーを発行** 画面左側のメニューから「Get API key」を選び，「Create API key」ボタンをクリックして新しいキーを作成します。

    **ステップ3：キーをコピーしてアプリに貼り付け** 画面に表示された `AIza...` から始まる長い文字列をコピーし，このアプリの左側（サイドバー）にある「Gemini APIキー」の入力欄に貼り付けてください。設定はこれだけで完了です！
    """)

st.sidebar.header("🔑 セキュリティ設定")
api_key = st.sidebar.text_input("Gemini APIキー", type="password")

# --- 入力フォーム ---
with st.form("abcde_form"):
    st.subheader("【事前情報】あなた自身について（任意）")
    st.caption("※入力していただくと，AIがあなたの経験や立場に寄り添った，より実践的なアドバイスを提供しやすくなります。")
    
   # 追加：お名前入力欄
    nickname = st.text_input("お名前（相談結果にてあなたのお名前で表現します。苗字（ひらがなでも可）のみでも構いません）")

    col1, col2 = st.columns(2)
    with col1:
        age_group = st.selectbox("年代", ["回答しない", "10代", "20代", "30代", "40代", "50代", "60代以上"])
    with col2:
        current_status = st.selectbox("現在の状況", ["回答しない", "求職中", "在職中", "職業訓練中", "学生", "その他"])
    
    background = st.text_area("これまでの経験や得意なこと（例：事務経験10年，コツコツ作業が得意，など）")

    st.markdown("---")

    st.subheader("【A】出来事（Activating Event）")
    event = st.text_area("あなたを悩ませている，または感情が揺さぶられた「客観的な出来事」を書いてください。")
    
    st.subheader("【B】信念・思い込み（Belief）")
    belief = st.text_area("その出来事に対して，あなたは「どうあるべきだ」「どうせ〜だ」と考えましたか？")
    
    st.subheader("【C】結果・感情（Consequence）")
    consequence = st.text_area("その結果，どんなネガティブな感情（怒り，不安，落ち込みなど）や行動が生じましたか？")

    st.markdown("---")
    agreement = st.checkbox("⚠️【確認】AIの提案はひとつの客観的な視点として受け止め，自分自身の思考を整理するために活用します。")
    submit_btn = st.form_submit_button("D（反論）とE（効果）をAIに相談する")

# --- 実行処理 ---
if submit_btn:
    if not agreement:
        st.error("⚠️ 実行するには，上の確認事項にチェックを入れてください。")
    elif not api_key:
        st.error("⚠️ 左側のメニューにAPIキーを入力してください。")
    elif not event or not belief:
        st.warning("⚠️ 「出来事」と「信念・思い込み」は最低限入力してください。")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        # 名前の出し分け処理（入力がなければ「あなた」とする）
        user_name = nickname if nickname else "あなた"

        prompt = f"""
        あなたは経験豊富な心理カウンセラーであり，キャリアコンサルタントです。
        アルバート・エリスのABCDE理論（論理療法）に基づき，クライアントの非合理的な思い込み（イラショナル・ビリーフ）を，柔軟で合理的な思考（ラショナル・ビリーフ）へと変容させるためのサポートを行ってください。

        【クライアントの背景情報】
        - 呼称：{user_name}
        - 年代：{age_group}
        - 現在の状況：{current_status}
        - これまでの経験・得意なこと：{background}

        【クライアントの入力情報】
        - A（出来事）: {event}
        - B（信念）: {belief}
        - C（結果・感情）: {consequence}

        【AIへの特別な指示】
        ・クライアントへの呼びかけには，必ず「{user_name}さん」（または入力がない場合は「あなた」）を使用し，親身で温かく寄り添うトーンで対話してください。
        ・クライアントの「背景情報」を十分に加味して回答を作成してください。例えば，社会人経験が豊富な方にはこれまでの実績や乗り越えてきた経験を肯定するようなアプローチを，経験が浅い方にはポテンシャルや今後の成長に寄り添うアプローチを心がけてください。

        【出力要件】
        以下の2つのセクションに分けて，温かく受容的なトーンで出力してください。

        1. 【D】Dispute（反論・問いかけ）
        クライアントの「B（信念）」に対する非合理性を優しく指摘し，別の視点に気づかせるための具体的な問いかけや客観的な反論を3つ提示してください。その際，ただ一般論を述べるのではなく，クライアントのこれまでの経験や強み（背景情報）を根拠として交えることで，納得感を高めてください。
        
        2. 【E】Effect（効果・新しい信念）
        Dの反論を踏まえ，クライアントが心を軽くするための「新しい合理的な思考（ラショナル・ビリーフ）」の候補を2パターン提案し，前向きな行動を促す励ましの言葉を添えてください。
        
        【制約条件】
        ・読点：文章中の読点には必ず「，」を使用すること（「、」は使用しないこと）
        """

        with st.spinner('キャリアコンサルタントAIが客観的な視点を整理しています...'):
            try:
                response = model.generate_content(prompt)
                st.success("分析が完了しました！")
                st.markdown("---")
                st.markdown(response.text)
                
                # --- ダウンロードボタン ---
                st.markdown("---")
                st.download_button(
                    label="📝 この分析結果をテキストファイルで保存（ダウンロード）する",
                    data=response.text,
                    file_name="abcde_result.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"エラーが発生しました。詳細: {e}")
