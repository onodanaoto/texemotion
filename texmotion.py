import streamlit as st
from openai import OpenAI
import sys

# デバッグ情報の表示
st.write(f"Python version: {sys.version}")
st.write(f"Streamlit version: {st.__version__}")

# セッション状態の初期化
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
if 'api_key_confirmed' not in st.session_state:
    st.session_state.api_key_confirmed = False

# APIキー入力フォーム
with st.form("api_key_form"):
    input_api_key = st.text_input("OpenAI APIキーを入力してください:", type="password")
    
    # 確認チェックボックス
    confirm_save = st.checkbox("APIキーをブラウザに保存することを理解し、同意します。")
    
    submit_button = st.form_submit_button("APIキーを設定")

    if submit_button:
        if confirm_save:
            st.session_state.api_key = input_api_key
            st.session_state.api_key_confirmed = True
            st.success("APIキーが設定されました。")
        else:
            st.error("APIキーの保存に同意していただく必要があります。")

# 警告メッセージ
st.warning("""
注意: このアプリケーションはChromeブラウザでの使用を前提としています。
入力したAPIキーはブラウザのローカルストレージに保存されます。
公共のコンピューターや共有デバイスでは使用しないでください。
""")

# OpenAIクライアントの初期化
client = None
if st.session_state.api_key and st.session_state.api_key_confirmed:
    try:
        client = OpenAI(api_key=st.session_state.api_key)
        st.write("OpenAI client created successfully")
    except Exception as e:
        st.error(f"Failed to create OpenAI client: {e}")
        st.stop()
else:
    st.warning("APIキーが設定されていないか、保存に同意していません。上のフォームでAPIキーを入力し、同意チェックボックスにチェックを入れてください。")
    st.stop()

def enhance_message(message, emotions, use_emoji):
    if client is None:
        st.error("OpenAI clientが初期化されていません。APIキーを確認してください。")
        return None
    
    try:
        emotion_text = "、".join(emotions)
        prompt = f"以下のメッセージを、「{emotion_text}」の感情を込めて改善してください。"
        if use_emoji:
            prompt += "適切な絵文字も追加してください。"
        prompt += f"\n\nメッセージ: {message}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたはメッセージの改善を支援するアシスタントです。"},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content
    except Exception as e:
        st.error(f"OpenAI APIエラー: {str(e)}")
        return None

def main():
    st.title("メッセージ改善アプリ")

    message = st.text_area("メッセージを入力してください：")

    st.write("感情を選択してください（複数選択可）：")
    emotions = {
        "残念": st.checkbox("残念に思っている"),
        "嬉しい": st.checkbox("嬉しく思っている"),
        "仲良く": st.checkbox("仲良くしたい"),
        "申し訳ない": st.checkbox("申し訳なく思っている"),
        "急ぐ": st.checkbox("急いでほしい"),
        "怒り": st.checkbox("怒っている")
    }

    selected_emotions = [emotion for emotion, selected in emotions.items() if selected]

    use_emoji = st.checkbox("絵文字を使用する")

    if st.button("メッセージを改善"):
        if message and selected_emotions:
            with st.spinner("メッセージを改善中..."):
                improved_message = enhance_message(message, selected_emotions, use_emoji)
            if improved_message:
                st.subheader("改善されたメッセージ：")
                st.write(improved_message)
        elif not message:
            st.warning("メッセージを入力してください。")
        elif not selected_emotions:
            st.warning("少なくとも1つの感情を選択してください。")

if __name__ == "__main__":
    main()
