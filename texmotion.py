import streamlit as st
from openai import OpenAI, error
import os
import pyperclip

# OpenAI クライアントの初期化
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# APIキーの一部を表示（セキュリティのため、全体は表示しない）
st.write("API Key (部分):", api_key[:4] + "****" + api_key[-4:] if api_key else "None")

# APIキーが設定されていない場合のエラー処理
if not client.api_key:
    st.error("OpenAI API keyが設定されていません。環境変数OPENAI_API_KEYを設定してください。")
    st.stop()

def enhance_message(message, emotion, use_emoji):
    try:
        prompt = f"以下のメッセージを、「{emotion}」の感情を込めて改善してください。"
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
    except error.OpenAIError as e:
        st.error(f"OpenAI APIエラー: {str(e)}")
        st.write("エラーの詳細:", e.http_status, e.error_code, e.user_message)
        return None
    except Exception as e:
        st.error(f"予期しないエラー: {str(e)}")
        st.write("エラーの詳細:", e)
        return None

def main():
    st.title("メッセージ改善アプリ")

    message = st.text_area("メッセージを入力してください：")

    emotions = ["残念に思っている", "嬉しく思っている", "仲良くしたい", "申し訳なく思っている", "急いでほしい", "怒っている"]
    emotion = st.selectbox("感情を選択してください：", emotions)

    use_emoji = st.checkbox("絵文字を使用する")

    if st.button("メッセージを改善"):
        if message:
            with st.spinner("メッセージを改善中..."):
                improved_message = enhance_message(message, emotion, use_emoji)
            if improved_message:
                st.subheader("改善されたメッセージ：")
                st.write(improved_message)

                if st.button("コピー"):
                    try:
                        pyperclip.copy(improved_message)
                        st.success("クリップボードにコピーしました！")
                    except pyperclip.PyperclipException:
                        st.warning("クリップボードへのコピーに失敗しました。手動でコピーしてください。")
        else:
            st.warning("メッセージを入力してください。")

if __name__ == "__main__":
    main()
