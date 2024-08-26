import streamlit as st
from openai import OpenAI

# ... (前のコードは変更なし) ...

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

def enhance_message(message, emotions, use_emoji):
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

if __name__ == "__main__":
    main()
