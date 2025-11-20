"""
このファイルは、画面表示に特化した関数定義のファイルです。
"""

############################################################
# ライブラリの読み込み
############################################################
import logging
import streamlit as st
import constants as ct


############################################################
# 関数定義
############################################################

def display_app_title():
    """
    タイトル表示
    """
    st.markdown(f"## {ct.APP_NAME}")


def display_initial_ai_message():
    """
    AIメッセージの初期表示
    """
    with st.chat_message("assistant", avatar=ct.AI_ICON_FILE_PATH):
        st.markdown("こちらは対話型の商品レコメンド生成AIアプリです。「こんな商品が欲しい」という情報・要望を画面下部のチャット欄から送信いただければ、おすすめの商品をレコメンドいたします。")
        st.markdown("**入力例**")
        st.info("""
        - 「長時間使える、高音質なワイヤレスイヤホン」
        - 「机のライト」
        - 「USBで充電できる加湿器」
        """)


def display_conversation_log():
    """
    会話ログの一覧表示
    """
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar=ct.USER_ICON_FILE_PATH):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar=ct.AI_ICON_FILE_PATH):
                display_product(message["content"])


def display_product(result):
    """
    商品情報の表示

    Args:
        result: LLMからの回答
    """
    logger = logging.getLogger(ct.LOGGER_NAME)

    # LLMレスポンスのテキストを辞書に変換
    product_lines = result[0].page_content.split("\n")
    product = {}
    for item in product_lines:
        if ": " in item:
            key, value = item.split(": ", 1)
            product[key] = value

    st.markdown("以下の商品をご提案いたします。")

    # 「商品名」と「価格」
    st.success(f"""
            商品名：{product.get('name', '不明')}（商品ID: {product.get('id', '不明')}）\n
            価格：{product.get('price', '不明')}
    """)

    # 在庫状況の表示
    if 'stock_status' in product:
        stock_status = product['stock_status']
        if stock_status == ct.STOCK_STATUS_LOW:
            st.warning(f"{ct.ICON_WARNING} 在庫状況：{stock_status}")
        elif stock_status == ct.STOCK_STATUS_OUT:
            st.error(f"{ct.ICON_ERROR} 在庫状況：{stock_status}")

    # 「商品カテゴリ」と「メーカー」と「ユーザー評価」
    st.code(f"""
        商品カテゴリ：{product.get('category', '不明')}\n
        メーカー：{product.get('maker', '不明')}\n
        評価：{product.get('score', '不明')}({product.get('review_number', '不明')}件)
    """, language=None, wrap_lines=True)

    # 商品画像
    if 'file_name' in product:
        st.image(f"images/products/{product['file_name']}", width=400)

    # 商品説明
    if 'description' in product:
        st.code(product['description'], language=None, wrap_lines=True)

    # おすすめ対象ユーザー
    if 'recommended_people' in product:
        st.markdown("**こんな方におすすめ！**")
        st.info(product["recommended_people"])

    # 商品ページのリンク
    st.link_button("商品ページを開く", type="primary", use_container_width=True, url="https://google.com")