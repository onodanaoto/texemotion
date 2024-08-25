import streamlit as st
import sys

st.write(f"Python version: {sys.version}")
st.write(f"Streamlit version: {st.__version__}")

try:
    from openai import OpenAI
    st.write("OpenAI imported successfully")
except ImportError as e:
    st.error(f"Failed to import OpenAI: {e}")

# ... 既存のコード ...

st.write(f"API key found: {'Yes' if api_key else 'No'}")

try:
    client = OpenAI(api_key=api_key)
    st.write("OpenAI client created successfully")
except Exception as e:
    st.error(f"Failed to create OpenAI client: {e}")





# 以下は変更なし----


# OpenAI クライアントの初期化
client = OpenAI(api_key=api_key)

# APIキーが正しく設定されているか確認
try:
    models = client.models.list()
    st.success("OpenAI APIの接続テストに成功しました。")
except Exception as e:
    st.error(f"OpenAI APIの接続テストに失敗しました: {str(e)}")
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
