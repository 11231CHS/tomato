# app.py
import streamlit as st
import pandas as pd
import joblib

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="착과율 예측 시스템",
    page_icon="🍅",
    layout="centered"
)

# -----------------------------
# 모델 로드
# -----------------------------
# 저장한 모델 파일명으로 변경하세요.
# 예: rf_model.pkl
@st.cache_resource
def load_model():
    return joblib.load("tomato_model.pkl")

rf_model = load_model()

# -----------------------------
# 스타일 꾸미기
# -----------------------------
st.markdown("""
    <style>
    .main {
        background-color: #f7f9fc;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: #2E8B57;
    }

    .sub {
        text-align: center;
        color: gray;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 25px;
        border-radius: 15px;
        background-color: #E8FFF1;
        border: 2px solid #2E8B57;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #1B5E20;
    }

    .stButton>button {
        width: 100%;
        height: 50px;
        border-radius: 12px;
        background-color: #2E8B57;
        color: white;
        font-size: 20px;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: #256d46;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# 제목
# -----------------------------
st.markdown('<div class="title">🍅 착과율 예측 시스템</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub">온도 · 습도 · CO₂ 데이터를 기반으로 착과율을 예측합니다.</div>',
    unsafe_allow_html=True
)

# -----------------------------
# 입력 UI
# -----------------------------
st.subheader("📥 환경 데이터 입력")

col1, col2 = st.columns(2)

with col1:
    temp = st.number_input(
        "🌡 내부온도 (°C)",
        min_value=0.0,
        max_value=50.0,
        value=25.0,
        step=0.1
    )

with col2:
    humidity = st.number_input(
        "💧 내부습도 (%)",
        min_value=0.0,
        max_value=100.0,
        value=60.0,
        step=0.1
    )

soil_temp = st.number_input(
    "🌿 내부 CO₂ (ppm)",
    min_value=0.0,
    max_value=5000.0,
    value=400.0,
    step=10.0
)

st.markdown("---")

# -----------------------------
# 예측 버튼
# -----------------------------
if st.button("📊 착과율 예측하기"):

    # 입력 데이터를 DataFrame으로 변환
    input_data = pd.DataFrame(
        [[temp, humidity, soil_temp]],
        columns=['내부온도', '내부습도', '내부CO2']
    )

    # 예측
    predicted = rf_model.predict(input_data)

    result = predicted[0]

    # 결과 출력
    st.markdown(
        f"""
        <div class="result-box">
            🍅 예측 착과율<br><br>
            {result:.1f} %
        </div>
        """,
        unsafe_allow_html=True
    )

    # 추가 코멘트
    st.markdown("### 📌 분석 결과")

    if result >= 80:
        st.success("매우 좋은 환경입니다. 착과율이 높게 예상됩니다.")
    elif result >= 60:
        st.info("양호한 상태입니다. 일부 환경 조정으로 개선 가능성이 있습니다.")
    else:
        st.warning("착과율이 낮게 예상됩니다. 온도·습도·CO₂ 조건을 점검해보세요.")
