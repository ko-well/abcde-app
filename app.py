import streamlit as st
import google.generativeai as genai

# --- ページ設定 ---
st.set_page_config(page_title="心のモヤモヤ解消・ストレスケアアシスタント", layout="centered")

st.markdown("""
<style>
h1, h2, h3 { color: #2C3E50 !important; }
label p, [data-testid="stWidgetLabel"] p { font-size: 18px !important; color: #2E86C1 !important; font-weight: bold !important; }
[data-testid="stFormSubmitButton"] button, .main-btn button { background-color: #34495E !important; color: white !important; font-size: 18px !important; font-weight: bold !important; width: 100% !important; border-radius: 8px !important; padding: 10px !important; }
.共感ボックス { background-color: #FADBD8; padding: 15px; border-radius: 8px; border-left: 5px solid #E74C3C; margin-bottom: 20px; }
.反論ボックス { background-color: #EBF5FB; padding: 15px; border-radius: 8px; border-left: 5px solid #3498DB; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# 💡 ご要望3：タイトルの変更と「ver.2」の小文字・スペース表示
st.markdown("<h1>💡 心のモヤモヤ解消・ストレスケアアシスタント <small style='font-size: 16px; color: #7F8C8D; font-weight: normal; vertical-align: middle;'>ver.2</small></h1>", unsafe_allow_html=True)

# 💡 ご要望2：求職者や働く人に向けた優しい説明文への変更
st.write("就職活動や仕事の中で感じるストレス，対人関係のモヤモヤした出来事を書き出すことで，AIがあなたの心に寄り添いながら，気持ちが軽くなる『新しい捉え方』を一緒に見つけます。")
st.markdown("---")

# --- APIキー設定 ---
st.sidebar.header("🔑 セキュリティ設定")
api_key = st.sidebar.text_input("Gemini APIキー", type="password")

# --- セッション状態の初期化 ---
if 'abcde_step' not in st.session_state:
    st.session_state.abcde_step = 1

# ==================================================
# ステップ1：お悩み入力画面
# ==================================================
if st.session_state.abcde_step == 1:
    with st.form("abcde_input_form"):
        user_name = st.text_input("お名前（苗字またはニックネームで可）", value="あなた")
        
        st.subheader("【A】モヤモヤした出来事（事実だけを客観的に）")
        st.caption("例：面接でうまく話せず、不採用の通知が届いた。 / 上司から書類のミスを厳しく注意された。")
        event = st.text_area("（いつ、どこで、何があったか）", key="input_a")
        
        st.subheader("【B】その時に頭に浮かんだ「思い込み」や「考え方のクセ」")
        st.caption("例：自分はどこからも必要とされない人間に違いない。 / 私は絶対にミスをしてはならない。")
        belief = st.text_area("（〜すべき、絶対に〜である、といった心の声をありのままに）", key="input_b")
        
        st.subheader("【C】その結果、生まれた「感情」や「ストレス度」")
        st.caption("例：ひどく落ち込んでしまい、次の応募をする元気が出ない。悔しくてイライラする。")
        consequence = st.text_area("（不安、焦り、怒りなどの気持ちや、体に起きた変化）", key="input_c")
        
        submit_1 = st.form_submit_button("AIに心を軽くする相談をする ✨")

    if submit_1:
        if not api_key:
            st.error("⚠️ 左側のメニューにAPIキーを入力してください。")
        elif not event or not belief or not consequence:
            st.warning("⚠️ すべての項目を入力してください。")
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # 💡 アイデア2：徹底的な共感を挟むためのプロンプト
            prompt1 = f"""
            あなたは相談者に深く寄り添う温かいキャリアコンサルタントです。
            心理学のABCDE理論に基づき，相談者の「〜すべき」という強迫観念（思い込み）をやさしく解きほぐしてください。

            【相談者の入力】
            - 呼称：{user_name}
            - 【A】出来事：{event}
            - 【B】思い込み：{belief}
            - 【C】感情・結果：{consequence}

            【出力要件】
            以下の2つのセクションに分けて出力してください。

            1. 【徹底的な共感と肯定】
            まずは相談者の辛い感情（C）に対して100%徹底的に共感し，そう思ってしまうのも無理はないと温かく認めてください。説教やアドバイスは一切せず，まずは味方であることを伝えてください。

            2. 【視点を変えるための、直球の反論（D）と効果（E）】
            相談者の思い込み（B）にある「〜すべき」「絶対に〜でなければならない」という極端な考え方に対して，客観的で論理的な「反論（D）」を、まずは直球で【1つだけ】やさしく提示してください。そして，その新しい捉え方をすることでどのように心が軽くなるか（E）を説明してください。

            【制約条件】
            - 読点には必ず「，」を使用すること（「、」は使用しない）。
            """
            
            with st.spinner('AIがあなたのお悩みに耳を傾けています...'):
                try:
                    response = model.generate_content(prompt1)
                    # データをセッションに保存して次へ
                    st.session_state.user_name = user_name
                    st.session_state.event = event
                    st.session_state.belief = belief
                    st.session_state.consequence = consequence
                    st.session_state.first_analysis = response.text
                    st.session_state.abcde_step = 2
                    st.rerun()
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

# ==================================================
# ステップ2：最初の回答 ＆ 納得度の確認
# ==================================================
elif st.session_state.abcde_step == 2:
    st.subheader(f"🗣️ AIキャリアコンサルタントからのメッセージ")
    st.markdown(st.session_state.first_analysis)
    
    st.markdown("---")
    # 💡 アイデア1＆ミックス案：納得度の確認フォーム
    st.subheader("💡 AIの「新しい捉え方」について，今のあなたのお気持ちを教えてください")
    st.write("優等生な正論を言われても，心が追いつかないことは当然あります。あなたの本音を教えてください。")
    
    with st.form("satisfaction_form"):
        satisfaction = st.radio(
            "現在の納得度はどのくらいですか？",
            ["👍 納得できた（少し気持ちが軽くなった）", 
             "🤔 あまり納得できない（モヤモヤが残る・まだ不安がある）", 
             "🙅 全然納得できない（自分の状況には合わない・正論すぎる）"],
            index=0
        )
        
        st.write("※「あまり納得できない」「全然納得できない」を選んだ方は，**納得いかない理由や，どうしても消えない不安**を下の欄に自由に書き出してください。")
        moya_reason = st.text_area("納得できない理由や、どうしても引っかかること（例：そうは言われても、やっぱり次の面接も落ちるのが怖いです）")
        
        submit_2 = st.form_submit_button("回答を送信する")
        
    if submit_2:
        # 「納得できた」場合はそのまま終了処理
        if "納得できた" in satisfaction:
            st.session_state.final_moya = "納得できました。"
            st.session_state.second_analysis = "ご納得いただけて良かったです！この新しい捉え方を胸に，あなたのペースで一歩ずつ進んでいきましょう。応援しています。"
            st.session_state.abcde_step = 3
            st.rerun()
        else:
            if not moya_reason:
                st.warning("⚠️ 納得できない場合は，その理由や引っかかっていることを入力してください。")
            elif not api_key:
                st.error("⚠️ APIキーが入力されていません。")
            else:
                # 💡 アイデア3：視点変更と再アプローチのプロンプト
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt2 = f"""
                あなたは相談者に深く寄り添う温かいキャリアコンサルタントです。
                先ほど提示した一般的な反論に対し，相談者は「納得がいかない・心が追いつかない」と感じています。
                
                【相談者の状況】
                - 出来事：{st.session_state.event}
                - 最初の思い込み：{st.session_state.belief}
                - 最初のAIの反論：{st.session_state.first_analysis}
                - 相談者が納得いかない理由（本音の抵抗）：{moya_reason}

                【出力要件】
                相談者が「そうは言っても…」と不安になる気持ちを、まずは「そうですよね，そう簡単に割り切れるものではないですよね」と完全に受け止めてください（絶対に否定したり論破しようとしないでください）。
                
                その上で，今度は【最初とは全く異なる角度の切り口】（例：あえてユーモアを交える，いっそ『最悪の事態』を極端に想像して笑い飛ばしてみる，あるいは大親友のように熱く励ますなど）から，相談者の本音のモヤモヤを打破するような，別の視点での再反論（D2）と新しい効果（E2）を優しく提案してください。
                一般論（優等生な回答）は厳禁です。

                【制約条件】
                - 読点には必ず「，」を使用すること。
                """
                
                with st.spinner('AIが別の角度から、あなたのモヤモヤを解消する方法を再考しています...'):
                    try:
                        response = model.generate_content(prompt2)
                        st.session_state.final_moya = moya_reason
                        st.session_state.second_analysis = response.text
                        st.session_state.abcde_step = 3
                        st.rerun()
                    except Exception as e:
                        st.error(f"エラーが発生しました: {e}")

# ==================================================
# ステップ3：最終回答 ＆ ダウンロード
# ==================================================
elif st.session_state.abcde_step == 3:
    st.subheader("🏁 カウンセリングの最終結果")
    
    st.markdown("### 📥 1回目の相談結果")
    with st.expander("確認する", expanded=False):
        st.markdown(st.session_state.first_analysis)
        
    st.markdown("### 💬 あなたの深層の本音（モヤモヤの理由）")
    st.info(st.session_state.final_moya)
    
    st.markdown("### 🔄 AIからの再アプローチ・別の視点")
    st.markdown(st.session_state.second_analysis)
    
    # --- ダウンロードテキストの組み立て ---
    download_text = f"""【心のモヤモヤ解消・ストレスケアシート】
■【A】出来事
{st.session_state.event}

■【B】思い込み・考え方のクセ
{st.session_state.belief}

■【C】感情・結果
{st.session_state.consequence}

==================================================
【1回目のAIからのメッセージ（共感と直球の反論）】
{st.session_state.first_analysis}

==================================================
【あなたの本音（納得いかなかった理由・引っかかり）】
{st.session_state.final_moya}

==================================================
【AIからの再アプローチ（別角度からの視点）】
{st.session_state.second_analysis}
"""
    
    st.markdown("---")
    st.download_button(
        label="📝 今回の対話内容と分析結果を保存（ダウンロード）する",
        data=download_text,
        file_name="stress_care_result.txt",
        mime="text/plain"
    )
    
    if st.button("もう一度最初から相談する"):
        st.session_state.abcde_step = 1
        st.rerun()

# --- ポータルサイトへ戻るボタン ---
st.markdown("---")
st.link_button("🏠 C.HARIGOMA キャリア支援ポータルへ戻る", "https://harigoma-career.streamlit.app/")
