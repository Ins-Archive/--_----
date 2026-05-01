import streamlit as st

st.set_page_config(page_title="보험분쟁사례", layout="wide")

st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(120deg, #b6ebcd 0%, #a7d7f1 35%, #9dc8f0 100%);
    }
    .block-container {
        max-width: 1220px;
        padding-top: 1.4rem;
        padding-bottom: 2rem;
    }
    .top-menu-container {
        display: flex;
        justify-content: space-between;
        gap: 14px;
        margin-top: 4px;
        margin-bottom: 34px;
    }
    .top-menu-item {
        flex: 1;
        text-align: center;
        border: 2px solid #2e4ca5;
        border-radius: 999px;
        padding: 10px 18px;
        color: #22429a;
        background: rgba(255, 255, 255, 0.2);
        font-size: 1.28rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    .hero-wrap {
        padding-top: 34px;
        padding-left: 8px;
    }
    .hero-title {
        margin: 0;
        color: #2e45b7;
        font-size: 5.1rem;
        font-weight: 900;
        line-height: 1.06;
        letter-spacing: -0.04em;
    }
    .hero-subtitle {
        margin-top: 56px;
        margin-bottom: 32px;
        color: #334bb6;
        font-size: 2.16rem;
        font-weight: 900;
        letter-spacing: -0.02em;
    }
    .search-row {
        display: flex;
        align-items: center;
        gap: 12px;
        background: #ffffff;
        border-radius: 999px;
        box-shadow: 0 8px 28px rgba(68, 95, 170, 0.16);
        padding: 12px 18px 12px 20px;
        max-width: 620px;
    }
    .search-left-icon {
        font-size: 2.25rem;
        color: #7a869a;
        line-height: 1;
    }
    .search-right-dot {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        border: 4px solid #737f90;
        flex-shrink: 0;
    }
    div[data-testid="stTextInput"] {
        width: 100%;
    }
    div[data-testid="stTextInput"] input {
        border: none;
        background: transparent;
        font-size: 1.88rem;
        color: #8a8a8a;
        padding: 0 !important;
        box-shadow: none !important;
    }
    div[data-testid="stTextInput"] input::placeholder {
        color: #9c9c9c;
        opacity: 1;
    }
    div[data-testid="stTextInput"] > label {
        display: none;
    }
    .right-visual {
        margin-top: 16px;
        padding-right: 8px;
    }
    @media (max-width: 1024px) {
        .hero-title { font-size: 4rem; }
        .hero-subtitle { font-size: 1.8rem; margin-top: 36px; }
        .top-menu-item { font-size: 1rem; }
        div[data-testid="stTextInput"] input { font-size: 1.4rem; }
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="top-menu-container">
    <div class="top-menu-item">민원사례 전부보기</div>
    <div class="top-menu-item">분쟁사례 전부보기</div>
    <div class="top-menu-item">보험주요판례 전부보기</div>
</div>
""",
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([1.12, 0.88], gap="small")

with left_col:
    st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
    st.markdown(
        '<h1 class="hero-title">보험분쟁사례<br>전부 모았습니다.</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="hero-subtitle">민원사례 * 분쟁사례 * 보험판례</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
<div class="search-row">
    <div class="search-left-icon">⌕</div>
""",
        unsafe_allow_html=True,
    )
    search_q = st.text_input("검색", placeholder="키워드 검색", label_visibility="collapsed")
    st.markdown(
        """
    <div class="search-right-dot"></div>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

with right_col:
    st.markdown('<div class="right-visual">', unsafe_allow_html=True)
    st.image(
        "https://img.freepik.com/free-vector/3d-insurance-policy-concept-illustration_23-2148927344.jpg",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

if search_q:
    st.info(f"'{search_q}' 관련 자료를 검색하고 있습니다.")