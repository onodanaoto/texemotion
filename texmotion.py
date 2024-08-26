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

# OpenAI APIキーの取得（Streamlit Cloud用）
api_key = st.secrets["OPENAI_API_KEY"]

st.write(f"API key found: {'Yes' if api_key else 'No'}")
st.write(f"API key type: {type(api_key)}")

if api_key:
    st.write(f"APIキーの先頭: {api_key[:5]}...")
else:
    st.error("OpenAI API keyが見つかりません。Streamlit Cloudの'Secrets'セクションでOPENAI_API_KEYを設定してください。")
    st.write("Available keys in st.secrets:", list(st.secrets.keys()))
    st.stop()

# OpenAIクライアントの初期化
try:
    client = OpenAI(api_key=api_key)
    st.write("OpenAI client created successfully")
except Exception as e:
    st.error(f"Failed to create OpenAI client: {e}")
    st.stop()

# 以下、既存のコード（enhance_message関数とmain関数）
...

if __name__ == "__main__":
    main()
