import streamlit as st
import sys
import os

# デバッグ情報の表示
st.write(f"Python version: {sys.version}")
st.write(f"Streamlit version: {st.__version__}")

# OpenAIのインポートを試みる
try:
    from openai import OpenAI
    import openai
    st.write(f"OpenAI imported successfully. Version: {openai.__version__}")
except ImportError as e:
    st.error(f"Failed to import OpenAI: {e}")
    st.stop()

# Streamlit Secrets の内容を確認
st.write("Streamlit Secrets:")
for key in st.secrets.keys():
    if isinstance(st.secrets[key], dict):
        st.write(f"{key}:")
        for subkey, subvalue in st.secrets[key].items():
            st.write(f"  {subkey}: {'*' * len(str(subvalue))}")
    else:
        st.write(f"{key}: {'*' * len(str(st.secrets[key]))}")

# OpenAI APIキーの取得
api_key = st.secrets.get("OPENAI_API_KEY")

if api_key:
    st.write(f"APIキーの先頭: {api_key[:5]}...")
else:
    st.error("OpenAI API keyが見つかりません。Streamlit Cloudの'Secrets'セクションでOPENAI_API_KEYを設定してください。")
    st.stop()

# OpenAIクライアントの初期化
try:
    client = OpenAI(api_key=api_key)
    st.write("OpenAI client created successfully")
except Exception as e:
    st.error(f"Failed to create OpenAI client: {e}")
    st.stop()

import pyperclip

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
    except Exception as e:
        st.error(f"OpenAI APIエラー: {str(e)}")
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
