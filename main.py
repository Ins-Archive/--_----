import streamlit as st

# 페이지 설정
st.set_page_config(page_title="팩트인스 | FactIns", layout="wide")

# CSS를 활용한 반응형 디자인 구현
st.markdown("""
<style>
    /* 전체 배경 그라데이션 */
    .stApp {
        background: linear_gradient(135deg, #e0f7fa 0%, #e1f5fe 50%, #f3e5f5 100%);
    }

    /* 상단 메뉴 버튼 디자인 */
    .top-menu-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 20px;
    }
    .top-menu-item {
        border: 1px solid #002D62;
        border-radius: 20px;
        padding: 5px 20px;
        font-size: 0.9rem;
        color: #002D62;
        background: rgba(255, 255, 255, 0.5);
    }

    /* 메인 타이틀 영역 */
    .hero-container {
        padding: 60px 0 30px 0;
        text-align: left;
        max-width: 800px;
        margin: 0 auto;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        color: #2c3e50;
        line-height: 1.2;
        margin-bottom: 20px;
    }
    .hero-subtitle {
        font-size: 1.5rem;
        color: #4a69bd;
        font-weight: 700;
        margin-bottom: 40px;
    }

    /* 반응형 검색창 디자인 */
    .search-box {
        background: white;
        border-radius: 50px;
        padding: 10px 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

# 1. 상단 퀵 메뉴 영역
st.markdown("""
<div class="top-menu-container">
    <div class="top-menu-item">민원사례 전부보기</div>
    <div class="top-menu-item">분쟁사례 전부보기</div>
    <div class="top-menu-item">보험주요판례 전부보기</div>
</div>
""", unsafe_allow_html=True)

# 2. 메인 히어로 섹션 (텍스트와 이미지 배치)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">보험분쟁사례<br>전부 모았습니다.</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">민원사례 * 분쟁사례 * 보험판례</p>', unsafe_allow_html=True)
    
    # 실제 검색창 (스트림릿 기능 사용)
    search_q = st.text_input("", placeholder="🔍 키워드 검색", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # 지점장님이 보내주신 이미지와 비슷한 느낌의 3D 일러스트가 들어갈 자리입니다.
    # 우선은 제가 가진 이미지나 아이콘으로 대체할 수 있습니다.
    st.image("https://img.freepik.com/free-vector/shield-with-check-mark-and-document-icon-concept_107791-16543.jpg", use_container_width=True)

st.divider()

# 3. 하단 결과 노출 예시
if search_q:
    st.info(f"'{search_q}'에 대한 팩트를 분석하고 있습니다...")