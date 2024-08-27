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

def init_openai_client():
    if st.session_state.api_key and st.session_state.api_key_confirmed:
        try:
            return OpenAI(api_key=st.session_state.api_key)
        except Exception as e:
            st.error(f"Failed to create OpenAI client: {e}")
    return None

def api_key_form():
    with st.form("api_key_form"):
        input_api_key = st.text_input("OpenAI APIキーを入力してください:", type="password")
        confirm_save = st.checkbox("APIキーをブラウザに保存することを理解し、同意します。")
        submit_button = st.form_submit_button("APIキーを設定")
        
        if submit_button:
            if confirm_save:
                st.session_state.api_key = input_api_key
                st.session_state.api_key_confirmed = True
                st.success("APIキーが設定されました。")
            else:
                st.error("APIキーの保存に同意していただく必要があります。")

def display_warning():
    st.warning("""
    注意: このアプリケーションはChromeブラウザでの使用を前提としています。
    入力したAPIキーはブラウザのローカルストレージに保存されます。
    公共のコンピューターや共有デバイスでは使用しないでください。
    """)

def enhance_message(client, message, emotions, use_emoji):
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
    
    api_key_form()
    display_warning()
    
    client = init_openai_client()
    if not client:
        st.warning("APIキーが設定されていないか、保存に同意していません。上のフォームでAPIキーを入力し、同意チェックボックスにチェックを入れてください。")
        return

    message = st.text_area("メッセージを入力してください：")
    
    # 絵文字の使用オプションを感情選択の前に移動し、デフォルトでチェックを入れる
    use_emoji = st.checkbox("絵文字を使用する", value=True)
    
    st.write("感情を選択してください（複数選択可）：")
    
    emotions = {
        "残念": "残念に思っている",
        "嬉しい": "嬉しく思っている",
        "仲良く": "仲良くしたい",
        "申し訳ない": "申し訳なく思っている",
        "急ぐ": "急いでほしい",
        "怒り": "怒っている"
    }
    
    selected_emotions = [emotion for emotion, description in emotions.items() if st.checkbox(description)]

    if st.button("メッセージを改善"):
        if message and selected_emotions:
            with st.spinner("メッセージを改善中..."):
                improved_message = enhance_message(client, message, selected_emotions, use_emoji)
            if improved_message:
                st.subheader("改善されたメッセージ：")
                st.write(improved_message)
        elif not message:
            st.warning("メッセージを入力してください。")
        elif not selected_emotions:
            st.warning("少なくとも1つの感情を選択してください。")

if __name__ == "__main__":
    main()
