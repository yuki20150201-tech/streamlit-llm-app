import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# 環境変数の読み込み
load_dotenv()

def get_llm():
    return ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

def get_expert_system_message(expert_type):
    """専門家のタイプに応じたシステムメッセージを返す"""
    if expert_type == "睡眠に関する専門家":
        return SystemMessage(content="""
あなたは睡眠に関する専門家です。安全なアドバイスを提供してください。
""")
    else:  
        return SystemMessage(content="""
あなたは教育に関する専門家です。安全なアドバイスを提供してください。
""")

st.title("お悩み相談アプリ")

# アプリの概要
st.markdown("""
## 📝 アプリについて
このアプリは、AI技術を活用したお悩み相談サービスです。専門分野に特化したAIが、あなたの質問に対して適切なアドバイスを提供します。

### 🔧 使い方
1. **専門家を選択**: 下記の専門家から相談したい分野を選んでください
2. **質問を入力**: テキストボックスに具体的な質問や相談内容を入力してください
3. **実行ボタンを押す**: AIが質問を分析し、専門的な回答を生成します

### 👨‍⚕️ 利用可能な専門家
""")

st.info("💡 **ヒント**: より具体的で詳しい質問をすると、より有用な回答を得られます。")

st.write("##### 🛏️ 睡眠に関する専門家")
st.write("• 睡眠の質の改善方法")
st.write("• 不眠症の対策")
st.write("• 睡眠リズムの調整")
st.write("• 快適な睡眠環境の作り方")

st.write("##### 📚 教育に関する専門家")
st.write("• 効果的な学習方法")
st.write("• モチベーションの維持")
st.write("• 勉強の効率化")
st.write("• 受験対策や子どもの教育")
selected_item = st.radio(
    "専門家を選択してください。",
    ["睡眠に関する専門家", "教育に関する専門家"]
)

st.divider()

input_message = st.text_input(label="専門家への質問を入力してください。")

if st.button("実行"):
    st.divider()
    
    if input_message:
        try:
            # LLMの取得
            llm = get_llm()
            
            # 専門家に応じたシステムメッセージの取得
            system_message = get_expert_system_message(selected_item)
            human_message = HumanMessage(content=input_message)
            
            # メッセージの作成
            messages = [system_message, human_message]
            
            # 回答生成中の表示
            with st.spinner(f"{selected_item}が回答を生成しています..."):
                result = llm(messages)
            
            # 回答の表示
            st.write(f"### {selected_item}からの回答:")
            st.write(result.content)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
            st.error("OpenAI APIキーが正しく設定されているか確認してください。")
    
    else:
        st.error("質問を入力してから「実行」ボタンを押してください。")

# サイドバーに追加情報を表示
with st.sidebar:
    st.header("📋 注意事項")
    st.warning("""
    ⚠️ **重要な注意点**
    - このアプリはAIによる一般的なアドバイスを提供します
    - 医療や法律に関する専門的な判断が必要な場合は、必ず専門機関にご相談ください
    - 緊急時は適切な機関（救急車、警察など）にご連絡ください
    """)
    
    st.header("❓ よくある質問")
    with st.expander("回答の精度について"):
        st.write("""
        AIは膨大なデータから学習していますが、100%正確な情報を保証するものではありません。
        重要な決定をする際は、複数の情報源を参考にすることをお勧めします。
        """)
    
    with st.expander("データの取り扱いについて"):
        st.write("""
        入力された質問内容は、回答生成のためにのみ使用され、
        個人を特定する情報は保存されません。
        """)
    
    with st.expander("回答に時間がかかる場合"):
        st.write("""
        AIが回答を生成するまでに数秒から数十秒かかる場合があります。
        「実行」ボタンを複数回押さず、しばらくお待ちください。
        """)




