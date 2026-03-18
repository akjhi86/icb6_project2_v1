import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 페이지 설정 ---
st.set_page_config(page_title="방한 외래관광객 데이터 대시보드", layout="wide")
st.title("🇰🇷 방한 외래관광객 탐색적 데이터 분석 (Interactive Dashboard)")
st.markdown("정적인 이미지(PNG)를 넘어, **마우스를 올려 실제 인원수 값을 직접 확인할 수 있도록 살려낸(Interactive)** 동적 대시보드입니다.")

# --- 데이터 로드 ---
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_nat_path = os.path.join(base_dir, "data", "raw", "visitor_by_nationality.csv")
    data_trans_path = os.path.join(base_dir, "data", "raw", "visitor_by_transport.csv")
    
    # 스트림릿 클라우드(리눅스)와 로컬(윈도우) 간 한글 CSV 인코딩 충돌 방지 로직
    try:
        df_nat = pd.read_csv(data_nat_path, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df_nat = pd.read_csv(data_nat_path, encoding='cp949')
        
    try:
        df_trans = pd.read_csv(data_trans_path, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df_trans = pd.read_csv(data_trans_path, encoding='cp949')
    
    df_trans['기준연월'] = pd.to_datetime(df_trans['기준연월'])
    df_trans = df_trans.sort_values('기준연월')
    df_nat['기준연월'] = pd.to_datetime(df_nat['기준연월'])
    return df_nat, df_trans

df_nat, df_trans = load_data()

st.divider()

# --- 도출된 10종의 시각화 (Interactive by Plotly) ---

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. 성별 기준 전체 관광객 인원수 분포")
    ct1 = df_nat.groupby('성별')['인원수'].sum().reset_index()
    fig1 = px.bar(ct1, x='성별', y='인원수', color='성별', text_auto='.2s', title="성별 전체 누적 인원수")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("2. 연령별 관광객 유입 순위 (상위 30)")
    ct2 = df_nat.groupby('연령별')['인원수'].sum().sort_values(ascending=False).reset_index().head(30)
    fig2 = px.bar(ct2, x='연령별', y='인원수', text_auto='.2s', color='연령별', title="연령별 상위 인원수")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
col3, col4 = st.columns(2)

with col3:
    st.subheader("3. 방문 목적별 인원수 차이 비교")
    ct3 = df_nat.groupby('목적별')['인원수'].sum().sort_values(ascending=False).reset_index()
    fig3 = px.bar(ct3, x='목적별', y='인원수', text_auto='.2s', color='목적별', title="방문 목적별 누적 인원")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("4. 공항 및 항구별 누적 이용 방문객 수")
    ports = [col for col in df_trans.columns if col != '기준연월']
    ct4 = df_trans[ports].sum().sort_values(ascending=False).reset_index()
    ct4.columns = ['교통수단', '누적 인원수']
    fig4 = px.bar(ct4, x='교통수단', y='누적 인원수', text_auto='.2s', color='교통수단', title="각 공항/항구별 누적 이용객")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

st.subheader("5. 기준연월별 외래관광객 입국 추세")
ct5 = df_nat.groupby('기준연월')['인원수'].sum().reset_index()
fig5 = px.line(ct5, x='기준연월', y='인원수', markers=True, title="전체 입국자 월별 시계열 추이")
st.plotly_chart(fig5, use_container_width=True)

st.divider()
col5, col6 = st.columns(2)

with col5:
    st.subheader("6. 연령별 및 성별 입국 인원수 비중 (Stacked)")
    ct6 = df_nat.groupby(['연령별', '성별'])['인원수'].sum().reset_index()
    fig6 = px.bar(ct6, x='연령별', y='인원수', color='성별', barmode='stack', title="연령별-성별 교차 인원 비중")
    st.plotly_chart(fig6, use_container_width=True)

with col6:
    st.subheader("7. 방문목적 및 연령대별 방문객 분포 (Heatmap)")
    ct7 = df_nat.pivot_table(index='목적별', columns='연령별', values='인원수', aggfunc='sum').fillna(0)
    fig7 = px.imshow(ct7, text_auto=True, aspect="auto", color_continuous_scale='YlGnBu', title="목적별/연령별 히트맵")
    st.plotly_chart(fig7, use_container_width=True)

st.divider()

st.subheader("8. TOP 3 주요 공항 (인천, 김포, 김해) 연월별 입국 추세")
ct8 = df_trans.melt(id_vars='기준연월', value_vars=['인천공항', '김포공항', '김해공항'], var_name='공항명', value_name='이용객수')
fig8 = px.line(ct8, x='기준연월', y='이용객수', color='공항명', markers=True, title="주요 3대 공항 입국 비교 추이")
st.plotly_chart(fig8, use_container_width=True)

st.divider()

st.subheader("9. 방문 연월에 따른 목적별 외국인 입국 인원 상세 추이")
ct9 = df_nat.groupby(['기준연월', '목적별'])['인원수'].sum().reset_index()
fig9 = px.line(ct9, x='기준연월', y='인원수', color='목적별', markers=True, title="각 목적별 월간 방문객 변화 흐름")
st.plotly_chart(fig9, use_container_width=True)

st.divider()

st.subheader("10. 국내 주요 입국 교통수단 총 이용자 비중")
top_5 = ct4.head(5)
others_val = ct4.iloc[5:]['누적 인원수'].sum()
others_df = pd.DataFrame([{'교통수단': '기타 공항/항구 합산', '누적 인원수': others_val}])
ct10_pie = pd.concat([top_5, others_df], ignore_index=True)
fig10 = px.pie(ct10_pie, values='누적 인원수', names='교통수단', title="전체 입국 관문 점유율 파이 차트")
fig10.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig10, use_container_width=True)

st.success("데이터 표와 반응형 차트를 통해 마우스를 올려 모든 세부 숫자(값)를 상세히 확인하실 수 있습니다!")
