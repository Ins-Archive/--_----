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

    .search-shell {
        max-width: 560px;
        width: 100%;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        border-radius: 999px;
        background: #ffffff;
        padding: 0.72rem 1.05rem 0.72rem 1.1rem;
        box-shadow: 0 8px 20px rgba(20, 53, 118, 0.13);
    }
    .search-icon {
        color: #808A98;
        font-size: 1.6rem;
        line-height: 1;
        flex-shrink: 0;
    }
    .search-shell div[data-testid="stTextInput"] {
        width: 100%;
        margin: 0;
    }
    .search-shell div[data-testid="stTextInput"] label {
        display: none;
    }
    .search-shell div[data-testid="stTextInput"] > div {
        margin: 0;
    }
    .search-shell div[data-baseweb="input"] {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
        min-height: auto !important;
        padding: 0 !important;
    }
    .search-shell input {
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
        font-size: 1.25rem !important;
        color: #5F6B7A !important;
        padding: 0 !important;
    }
    .search-shell input::placeholder {
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
        .search-shell input {
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
    st.markdown('<div class="search-shell"><span class="search-icon">🔍</span>', unsafe_allow_html=True)
    search_q = st.text_input("키워드 검색", placeholder="키워드 검색", label_visibility="collapsed")
    st.markdown("</div></div>", unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="hero-right">', unsafe_allow_html=True)
    st.image(
        "https://cdn3d.iconscout.com/3d/premium/thumb/insurance-policy-3d-icon-download-in-png-blend-fbx-gltf-file-formats--secure-protection-document-safety-business-pack-icons-9292352.png",
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

if search_q:
    st.info(f"'{search_q}' 키워드로 사례를 검색하고 있습니다.")