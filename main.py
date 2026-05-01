import streamlit as st

st.set_page_config(page_title="보험분쟁사례", layout="wide")

st.markdown(
    """
<style>
    html, body, [class*="css"] {
        font-family: "Pretendard", "Noto Sans KR", "Segoe UI", sans-serif;
    }
    .stApp {
        background: linear-gradient(120deg, #E0F7FA 0%, #B3E5FC 100%);
    }
    .main .block-container {
        max-width: 1260px;
        padding-top: 1.4rem;
        padding-bottom: 2.2rem;
        padding-left: 2.6rem;
        padding-right: 2.6rem;
    }

    .top-nav {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin-top: 0.35rem;
        margin-bottom: 2.4rem;
        flex-wrap: wrap;
    }
    .top-nav-btn {
        border: 1.8px solid #2D5CB7;
        color: #2D5CB7;
        border-radius: 999px;
        background: transparent;
        padding: 0.65rem 1.5rem;
        font-size: 1.02rem;
        font-weight: 600;
        line-height: 1;
        white-space: nowrap;
    }

    .hero-left {
        padding-top: 4.8rem;
        padding-left: 0.2rem;
        padding-right: 1rem;
    }
    .hero-title {
        margin: 0;
        color: #111111;
        font-size: clamp(2.4rem, 4.7vw, 4.8rem);
        font-weight: 800;
        line-height: 1.12;
        letter-spacing: -0.03em;
    }
    .hero-subtitle {
        margin-top: 2.5rem;
        margin-bottom: 1.7rem;
        color: #164A9E;
        font-size: clamp(1.05rem, 1.9vw, 2rem);
        font-weight: 700;
        letter-spacing: -0.01em;
    }

    .hero-search {
        max-width: 560px;
    }
    .hero-search div[data-testid="stTextInput"] {
        margin: 0;
    }
    .hero-search div[data-testid="stTextInput"] > label {
        display: none;
    }
    .hero-search div[data-baseweb="input"] {
        border: none !important;
        border-radius: 999px !important;
        background-color: #ffffff !important;
        box-shadow: 0 8px 20px rgba(20, 53, 118, 0.13) !important;
        padding-left: 3rem !important;
        padding-right: 2.1rem !important;
        background-image: url("https://api.iconify.design/material-symbols/search-rounded.svg?color=%23808A98"), url("https://api.iconify.design/mdi/circle-outline.svg?color=%23808A98");
        background-repeat: no-repeat, no-repeat;
        background-size: 1.35rem 1.35rem, 1.1rem 1.1rem;
        background-position: left 1rem center, right 0.95rem center;
    }
    .hero-search input {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
        font-size: 1.25rem !important;
        color: #5F6B7A !important;
        padding: 0.7rem 0 !important;
    }
    .hero-search input::placeholder {
        color: #96A0AE !important;
        opacity: 1;
    }

    .hero-right {
        padding-top: 1.2rem;
        padding-left: 1.2rem;
        padding-right: 0.4rem;
    }

    @media (max-width: 1024px) {
        .main .block-container {
            padding-left: 1.2rem;
            padding-right: 1.2rem;
        }
        .hero-left {
            padding-top: 1.2rem;
            padding-right: 0;
        }
        .hero-subtitle {
            margin-top: 1.4rem;
        }
        .hero-search div[data-baseweb="input"] {
            padding-left: 2.6rem !important;
        }
        .hero-search input {
            font-size: 1.05rem !important;
        }
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="top-nav">
    <div class="top-nav-btn">민원사례 전부보기</div>
    <div class="top-nav-btn">분쟁사례 전부보기</div>
    <div class="top-nav-btn">보험주요판례 전부보기</div>
</div>
""",
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([6, 4], gap="medium")

with left_col:
    st.markdown('<div class="hero-left">', unsafe_allow_html=True)
    st.markdown(
        '<h1 class="hero-title">보험분쟁사례<br>전부 모았습니다.</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="hero-subtitle">민원사례 * 분쟁사례 * 보험판례</p>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="hero-search">', unsafe_allow_html=True)
    search_q = st.text_input("키워드 검색", placeholder="키워드 검색", label_visibility="collapsed")
    st.markdown("</div></div>", unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="hero-right">', unsafe_allow_html=True)
    st.image(
        r"C:\Users\yunch\.cursor\projects\c-Users-yunch-OneDrive-Desktop\assets\c__Users_yunch_AppData_Roaming_Cursor_User_workspaceStorage_7d881214a54a2549035ecc0fc989534a_images__________-737218a9-d87d-46c1-8ca2-949d9bd5a2b0.png",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

if search_q:
    st.info(f"'{search_q}' 키워드로 사례를 검색하고 있습니다.")