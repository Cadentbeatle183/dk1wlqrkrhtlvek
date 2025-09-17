# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import requests
from io import StringIO
from datetime import datetime

# 폰트 적용 (Pretendard, 없으면 무시)
plt.rcParams['font.family'] = 'Pretendard'

st.set_page_config(page_title="해수온 상승 대시보드", layout="wide")

st.title("🌊 바다의 온도 경고음: 해수온 상승과 지속 가능한 해결책")

# =========================
# 공개 데이터 대시보드
# =========================
st.header("📈 공개 데이터 기반 해수온 상승 분석")

@st.cache_data
def load_public_data():
    try:
        # NOAA 해수온 데이터 예시 (SST: Sea Surface Temperature)
        # 출처: NOAA OISST v2, https://www.ncei.noaa.gov/products/optimum-interpolation-sst
        url = "https://www.ncei.noaa.gov/data/sea-surface-temperature-optimum-interpolation/v2.1/access/avhrr/2023/AVHRR_OI_v2.1_20230101.csv"
        r = requests.get(url)
        r.raise_for_status()
        df = pd.read_csv(StringIO(r.text))
        # date, value 형식으로 변환 (예시: 전체 평균 해수온)
        df['date'] = pd.to_datetime(df['date'])
        df = df[df['date'] <= pd.Timestamp(datetime.now().date())]  # 미래 데이터 제거
        df = df[['date', 'value']].drop_duplicates()
        return df
    except:
        st.warning("공개 데이터 로드 실패, 예시 데이터로 대체합니다.")
        dates = pd.date_range(start="2023-01-01", periods=12, freq='M')
        values = np.linspace(26, 28, 12)  # 예시 해수온
        return pd.DataFrame({'date': dates, 'value': values})

public_df = load_public_data()

# 시각화
fig, ax = plt.subplots(figsize=(10,4))
sns.lineplot(data=public_df, x='date', y='value', marker='o', ax=ax)
ax.set_title("공개 데이터 기반 월별 해수온 변화", fontsize=14)
ax.set_xlabel("날짜")
ax.set_ylabel("해수온 (℃)")
st.pyplot(fig)

# CSV 다운로드
st.download_button(
    label="📥 공개 데이터 다운로드",
    data=public_df.to_csv(index=False),
    file_name='public_sea_temp.csv',
    mime='text/csv'
)

# =========================
# 사용자 입력 데이터 대시보드
# =========================
st.header("📝 사용자 입력 데이터 기반 해수온 분석")

# 예시 사용자 데이터 (프롬프트 기반)
@st.cache_data
def load_user_data():
    # 날짜, 해수온, 그룹(옵션) 표준화
    dates = pd.date_range(start="2024-01-01", periods=12, freq='M')
    values = [26.1,26.5,27.0,27.2,27.8,28.0,28.3,28.5,28.6,28.9,29.0,29.2]
    groups = ["서해"]*6 + ["남해"]*6
    df = pd.DataFrame({'date': dates, 'value': values, '지역': groups})
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'] <= pd.Timestamp(datetime.now().date())]  # 미래 데이터 제거
    return df

user_df = load_user_data()

# 사이드바 옵션
st.sidebar.header("사용자 데이터 필터")
selected_region = st.sidebar.multiselect("지역 선택", options=user_df['지역'].unique(), default=user_df['지역'].unique())
df_filtered = user_df[user_df['지역'].isin(selected_region)]

# 시각화
fig2 = px.line(df_filtered, x='date', y='value', color='지역',
               labels={'date':'날짜','value':'해수온 (℃)','지역':'지역'},
               title="사용자 입력 데이터 기반 월별 해수온 변화")
st.plotly_chart(fig2, use_container_width=True)

# CSV 다운로드
st.download_button(
    label="📥 사용자 데이터 다운로드",
    data=df_filtered.to_csv(index=False),
    file_name='user_sea_temp.csv',
    mime='text/csv'
)

# =========================
# 결론/설명
# =========================
st.header("💡 결론 및 제언")
st.markdown("""
- 해수온 상승은 산호초 백화, 어류 이동 경로 변화, 해안 도시 침수 등 다양한 문제를 발생시킵니다.
- 원인은 주로 인간 활동으로 인한 온실가스 배출이며, 국제적 정책 대응과 개인의 실천이 동시에 필요합니다.
- 학생 개개인의 작은 행동(일회용품 줄이기, 에너지 절약 등)도 장기적으로 큰 효과를 발휘할 수 있습니다.
""")
