import streamlit as st
import pandas as pd
import os
import urllib.parse

# 1. 페이지 설정 및 이미지 우회
st.set_page_config(page_title="HONGDAE POP-UP HUB", page_icon="🛍️", layout="wide")
st.markdown('<meta name="referrer" content="no-referrer">', unsafe_allow_html=True)

# 2. 커스텀 CSS (세련된 다크 미드나잇 테마 & 고급스러운 UI)
st.markdown("""
    <style>
    /* 전체 배경을 고급스러운 다크 미드나잇 톤으로 설정 */
    .stApp { 
        background-color: #0b0f17; 
        color: #e2e8f0;
    }

    /* 최상단 Hero 영역 */
    .hero-container-v3 {
        background: linear-gradient(135deg, #111827 0%, #1f2937 50%, #e11d48 100%);
        padding: 48px 36px;
        border-radius: 24px;
        color: #ffffff;
        text-align: left;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(225, 29, 72, 0.2);
        color: #fb7185;
        font-size: 12px;
        font-weight: 700;
        padding: 5px 14px;
        border-radius: 30px;
        letter-spacing: 1px;
        margin-bottom: 14px;
        border: 1px solid rgba(251, 113, 133, 0.3);
    }

    .hero-title-v3 { 
        font-size: 36px; 
        font-weight: 900; 
        line-height: 1.25;
        letter-spacing: -1px;
        margin-bottom: 10px;
        background: linear-gradient(to right, #ffffff, #f1f5f9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* 요청하신 문구 수정 반영 */
    .hero-subtitle-v3 { 
        font-size: 15px; 
        color: #94a3b8;
        font-weight: 400;
    }

    /* Streamlit 입력창(검색창) 다크 테마 커스텀 */
    .stTextInput input {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }
    .stTextInput input:focus {
        border-color: #f43f5e !important;
        box-shadow: 0 0 10px rgba(244, 63, 94, 0.3) !important;
    }

    /* 고급 다크 카드 스타일 */
    .card-box {
        background-color: #151d2a;
        border-radius: 16px;
        border: 1px solid #232d3f;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
        margin-bottom: 25px;
        overflow: hidden;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .card-box:hover {
        transform: translateY(-4px);
        border-color: #e11d48;
    }
    .card-content { padding: 18px; }
    
    .card-tag-wrapper { display: flex; gap: 6px; margin-bottom: 10px; }
    .badge-region { background-color: #334155; color: #f8fafc; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 6px; }
    .badge-category { background-color: rgba(225, 29, 72, 0.15); color: #fb7185; font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 6px; }

    .title-map-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 8px 0 10px 0;
    }
    .card-title-text {
        font-size: 17px;
        font-weight: 700;
        color: #f8fafc;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        flex: 1;
        margin-right: 8px;
    }
    .map-btn-a {
        font-size: 11px;
        color: #4ade80 !important;
        background-color: rgba(74, 222, 128, 0.1);
        border: 1px solid rgba(74, 222, 128, 0.3);
        padding: 5px 12px;
        border-radius: 20px;
        text-decoration: none !important;
        font-weight: 700;
        white-space: nowrap;
        transition: all 0.2s ease;
    }
    .map-btn-a:hover {
        background-color: #22c55e;
        color: #ffffff !important;
    }

    .card-info { 
        font-size: 13px; 
        color: #94a3b8; 
        line-height: 1.4; 
        height: 38px; 
        overflow: hidden; 
        text-overflow: ellipsis; 
        display: -webkit-box; 
        -webkit-line-clamp: 2; 
        -webkit-box-orient: vertical; 
    }
    </style>
""", unsafe_allow_html=True)

# 3. 최상단 헤더 (수정된 문구 반영)
st.markdown("""
    <div class="hero-container-v3">
        <div class="hero-badge">HONGDAE TREND & POP-UP</div>
        <div class="hero-title-v3">지금 가장 핫한<br>팝업스토어를 한눈에.</div>
        <div class="hero-subtitle-v3">홍대의 놓치면 안 될 최신 팝업스토어 정보 HUB</div>
    </div>
""", unsafe_allow_html=True)

# 4. 데이터 로드 및 카드 뷰 구성
try:
    df = pd.read_csv("popup_stores_map.csv")
    
    # 지역 선택창 제거 후, 검색창이 전체 넓이를 차지하도록 변경
    search_kw = st.text_input("🔍 팝업스토어 검색", "", placeholder="스토어 이름이나 카테고리를 입력하세요...")

    filtered_df = df.copy()
    if search_kw:
        filtered_df = filtered_df[
            filtered_df['팝업스토어명'].str.contains(search_kw, case=False, na=False) |
            filtered_df['상세정보'].str.contains(search_kw, case=False, na=False)
        ]

    st.write(f"총 <span style='color:#f43f5e; font-weight:bold;'>{len(filtered_df)}개</span>의 팝업스토어", unsafe_allow_html=True)
    st.write("")

    cols_per_row = 3
    cols = st.columns(cols_per_row)
    default_fallback = "https://images.unsplash.com/photo-1555529771-835f59fc5eff?w=600&auto=format&fit=crop"

    for idx, row in filtered_df.reset_index(drop=True).iterrows():
        col = cols[idx % cols_per_row]
        
        with col:
            img_path = str(row['이미지']) if pd.notna(row['이미지']) else ""
            store_name = str(row['팝업스토어명'])
            
            encoded_query = urllib.parse.quote(f"{store_name} 팝업스토어")
            map_url = f"https://map.naver.com/v5/search/{encoded_query}"

            if img_path and os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            elif img_path.startswith("http"):
                st.image(img_path, use_container_width=True)
            else:
                st.image(default_fallback, use_container_width=True)
            
            st.markdown(f"""
                <div class="card-box">
                    <div class="card-content">
                        <div class="card-tag-wrapper">
                            <span class="badge-region">{row['지역']}</span>
                            <span class="badge-category">{row['카테고리']}</span>
                        </div>
                        <div class="title-map-row">
                            <div class="card-title-text" title="{store_name}">{store_name}</div>
                            <a href="{map_url}" target="_blank" class="map-btn-a">📍 지도보기</a>
                        </div>
                        <div class="card-info">📍 {row['상세정보']}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

except FileNotFoundError:
    st.error("⚠️ 'popup_stores_map.csv' 파일이 없습니다.")