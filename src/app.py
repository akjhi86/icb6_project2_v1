import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import os

st.set_page_config(page_title="방한 외래관광객 대시보드 (20종 차트)", page_icon="✈️", layout="wide")

st.title("✈️ 방한 외래관광객 실시간 분석 대시보드 (버전 2.0)")
st.markdown("데이터 결측치 점검 기능과 고도화된 10종을 추가하여, **총 20가지 테마의 동적 통계 시각화** 에셋을 지원합니다.")

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_nat_path = os.path.join(base_dir, "data", "raw", "visitor_by_nationality.csv")
data_trans_path = os.path.join(base_dir, "data", "raw", "visitor_by_transport.csv")

@st.cache_data
def load_data():
    df_nat = pd.read_csv(data_nat_path)
    df_trans = pd.read_csv(data_trans_path)
    
    # 🌟 결측치 탐색 및 덮어쓰기 로직 🌟
    nat_null = df_nat.isnull().sum().sum()
    trans_null = df_trans.isnull().sum().sum()
    
    if nat_null > 0 or trans_null > 0:
        df_nat.fillna(0, inplace=True)
        df_trans.fillna(0, inplace=True)
        imputed = True
    else:
        imputed = False
        
    df_nat['기준연월'] = pd.to_datetime(df_nat['기준연월'])
    df_trans['기준연월'] = pd.to_datetime(df_trans['기준연월'])
    df_trans = df_trans.sort_values('기준연월')
    
    return df_nat, df_trans, nat_null, trans_null, imputed

try:
    df_nat, df_trans, nat_null, trans_null, imputed = load_data()
except Exception as e:
    st.error(f"데이터 파일 에러: {e}")
    st.stop()

# 🌟 결측치 현황 리포트 아코디언 컴포넌트 추가 🌟
with st.expander("🛠️ 데이터 무결성 및 결측치(Missing Values) 점검 보고서", expanded=True):
    if imputed:
        st.warning(f"데이터 결손 감지: 국적 파일에서 {nat_null}건, 교통수단 파일에서 {trans_null}건의 결측치가 발견되었습니다. 정상적인 20종 차트 연산을 위해 해당 구간을 0으로 안전하게 치환(Impute) 적용했습니다.")
    else:
        st.success("데이터 검증 완료: 두 데이터셋 모두 단 하나의 결측치 빈칸도 발견되지 않은 완벽한 무결점 데이터 상태를 유지 중입니다!")
    st.markdown("본 대시보드의 실시간 시각화 파이프라인은 완전하게 클린 처리된 위 데이터들을 기반으로 수행되어 안전하고 정확한 지표를 반환합니다.")

# 좌측 사이드바 구조
st.sidebar.header("🔍 실시간 데이터 정밀 필터")
months = sorted(df_nat['기준연월'].dt.strftime('%Y-%m').unique().tolist())
selected_months = st.sidebar.multiselect("연월 필터", months, default=months)
selected_purposes = st.sidebar.multiselect(
    "조회 목적군 선택", 
    options=df_nat['목적별'].unique().tolist(), 
    default=df_nat['목적별'].unique().tolist()
)

filtered_nat = df_nat.copy()
if selected_months:
    mask = filtered_nat['기준연월'].dt.strftime('%Y-%m').isin(selected_months)
    filtered_nat = filtered_nat[mask]
if selected_purposes:
    filtered_nat = filtered_nat[filtered_nat['목적별'].isin(selected_purposes)]


st.sidebar.markdown("---")

c1, c2, c3 = st.columns(3)
total_visitors = filtered_nat['인원수'].sum()
top_purpose = filtered_nat.groupby('목적별')['인원수'].sum().idxmax() if not filtered_nat.empty else "N/A"
top_age = filtered_nat.groupby('연령별')['인원수'].sum().idxmax() if not filtered_nat.empty else "N/A"
c1.metric("📊 설정 조건 총 외래관광객 인원", f"{total_visitors:,} 명")
c2.metric("🏆 가장 두드러진 주 방문 목적", top_purpose)
c3.metric("🎯 메가 소비 타겟 거점 연령대", top_age)
st.divider()

# 메인 뷰어 탭 포지션 
tab1, tab2, tab3, tab4 = st.tabs(["👤 인구특성 (1~3, 6 차트)", "📅 시계열 추이 (5, 9, 17, 20 차트)", "🛬 교통 인프라 규모 (4, 8, 10, 11, 14, 18 차트)", "💎 타겟별 심층 교차분석 (7, 12, 13, 15, 16, 19 차트)"])

with tab1:
    st.subheader("인구통계학적 기초 점유 비중")
    if not filtered_nat.empty:
        r1_1, r1_2 = st.columns(2)
        with r1_1:
            ct1 = filtered_nat.groupby('성별')['인원수'].sum()
            fig1, ax1 = plt.subplots(figsize=(6,5))
            ct1.plot(kind='bar', color=['#87CEFA', '#FA8072', '#98FB98'], ax=ax1)
            ax1.set_title("01. 성별 방문 규모 종합판")
            plt.xticks(rotation=0)
            st.pyplot(fig1)
        with r1_2:
            ct2 = filtered_nat.groupby('연령별')['인원수'].sum().sort_values(ascending=False)
            fig2, ax2 = plt.subplots(figsize=(6,5))
            ct2.plot(kind='bar', color='#FFA07A', ax=ax2)
            ax2.set_title("02. 유치 규모 최고액을 보유한 연령그룹 순서도")
            plt.xticks(rotation=45)
            st.pyplot(fig2)
            
        r2_1, r2_2 = st.columns(2)
        with r2_1:
            ct3 = filtered_nat.groupby('목적별')['인원수'].sum().sort_values(ascending=False)
            fig3, ax3 = plt.subplots(figsize=(6,5))
            ct3.plot(kind='bar', color='#DDA0DD', ax=ax3)
            ax3.set_title("03. 관광 vs 비관광 방문 목적의 차등 궤도막대")
            plt.xticks(rotation=0)
            st.pyplot(fig3)
        with r2_2:
            ct6 = filtered_nat.pivot_table(index='연령별', columns='성별', values='인원수', aggfunc='sum').fillna(0)
            fig6, ax6 = plt.subplots(figsize=(6,5))
            ct6.plot(kind='bar', stacked=True, ax=ax6, cmap='Pastel1')
            ax6.set_title("06. 층이 나뉜 연령별/성분 분담 점유비율 탑 (Stacked)")
            plt.xticks(rotation=45)
            st.pyplot(fig6)
            
with tab2:
    st.subheader("계절성과 시간 궤도 추세 모니터링 보드")
    if not filtered_nat.empty:
        r3_1, r3_2 = st.columns(2)
        with r3_1:
            ct5 = filtered_nat.groupby('기준연월')['인원수'].sum()
            fig5, ax5 = plt.subplots(figsize=(6,5))
            ct5.plot(kind='line', marker='o', color='#DC143C', ax=ax5)
            ax5.set_title("05. 기본 연월별 전체 객수 외래입국 추이 차트")
            ax5.grid(True, linestyle='--')
            st.pyplot(fig5)
        with r3_2:
            ct9 = filtered_nat.pivot_table(index='기준연월', columns='목적별', values='인원수', aggfunc='sum').fillna(0)
            fig9, ax9 = plt.subplots(figsize=(6,5))
            ct9.plot(kind='line', marker='s', ax=ax9)
            ax9.set_title("09. 시간의 결대로 펼친 목적 유형 세선 분석 (Multi-line)")
            ax9.grid(True)
            st.pyplot(fig9)
            
        r4_1, r4_2 = st.columns(2)
        with r4_1:
            df_q = filtered_nat.copy()
            df_q['분기'] = df_q['기준연월'].dt.to_period('Q').astype(str)
            ct17 = df_q.groupby('분기')['인원수'].sum()
            fig17, ax17 = plt.subplots(figsize=(6,5))
            ct17.plot(kind='bar', color='#4682B4', ax=ax17)
            ax17.set_title("17. 필터조건을 응집한 거간 분기(Quarterly) 총합 지형")
            plt.xticks(rotation=0)
            st.pyplot(fig17)
        with r4_2:
            ct20_young = filtered_nat[filtered_nat['연령별'] == '20세 이하'].groupby('기준연월')['인원수'].sum()
            ct20_old = filtered_nat[filtered_nat['연령별'] == '61세이상'].groupby('기준연월')['인원수'].sum()
            fig20, ax20 = plt.subplots(figsize=(6,5))
            ax20.plot(ct20_young.index, ct20_young.values, marker='^', label='청년/미성년 집단군')
            ax20.plot(ct20_old.index, ct20_old.values, marker='v', label='시니어 파워 집단군')
            ax20.set_title("20. 시대 교차점(청년vs노년) 흐름이 만나고 벗어나는 양극성 변동")
            ax20.legend()
            ax20.grid(True, linestyle=':')
            plt.xticks(rotation=45)
            st.pyplot(fig20)

with tab3:
    st.subheader("국가 공항/항만 핵심 교통 인프라 통계 (전체 기간 상수)")
    ports = [col for col in df_trans.columns if col != '기준연월']
    r5_1, r5_2 = st.columns(2)
    with r5_1:
        ct4 = df_trans[ports].sum().sort_values(ascending=False)
        fig4, ax4 = plt.subplots(figsize=(6,5))
        ct4.plot(kind='bar', color='#20B2AA', ax=ax4)
        ax4.set_title("04. 국가 관문 기준 단일 전체 누적 수송 인원")
        plt.xticks(rotation=45)
        st.pyplot(fig4)
        
    with r5_2:
        top_5 = ct4.head(5)
        others = pd.Series({'그 외 항구 등 종합': ct4.iloc[5:].sum()})
        fig10, ax10 = plt.subplots(figsize=(6,5))
        pd.concat([top_5, others]).plot(kind='pie', autopct='%1.1f%%', cmap='Set2', ax=ax10)
        ax10.set_title("10. 메이저 파이프라인(교통) 채널별 실질 지분율 파악용")
        ax10.set_ylabel('')
        st.pyplot(fig10)

    r6_1, r6_2 = st.columns(2)
    with r6_1:
        fig8, ax8 = plt.subplots(figsize=(6,5))
        df_trans.set_index('기준연월')[['인천공항', '김포공항', '김해공항']].plot(kind='line', marker='x', ax=ax8)
        ax8.set_title("08. 핵심 하늘길 3대장 꺾은선 (인천/김포/김해)")
        st.pyplot(fig8)
        
    with r6_2:
        port_cols = ['부산항구', '인천항구', '제주항구', '기타항구']
        ct11 = df_trans[port_cols].sum()
        fig11, ax11 = plt.subplots(figsize=(6,5))
        ct11.plot(kind='bar', color='#8FBC8F', ax=ax11)
        ax11.set_title("11. 비행기를 제외한 '배편, 해양 항구' 전용 누적 비교 단위")
        st.pyplot(fig11)

    r7_1, r7_2 = st.columns(2)
    with r7_1:
        ct14_inland = df_trans.set_index('기준연월')[['김포공항', '김해공항']].sum(axis=1)
        ct14_jeju = df_trans.set_index('기준연월')['제주공항']
        fig14, ax14 = plt.subplots(figsize=(6,5))
        ax14.plot(ct14_inland.index, ct14_inland.values, marker='o', label='내륙 특화 공용망')
        ax14.plot(ct14_jeju.index, ct14_jeju.values, marker='s', label='도서 지역 관광 혜택망')
        ax14.set_title("14. 목적 특화형 공항 간 경쟁력 엎치락뒤치락 확인법")
        ax14.legend()
        st.pyplot(fig14)
        
    with r7_2:
        df_area = df_trans.set_index('기준연월')
        ct18_icn = df_area['인천공항']
        ct18_others = df_area[ports].sum(axis=1) - df_area['인천공항']
        fig18, ax18 = plt.subplots(figsize=(6,5))
        ax18.stackplot(df_area.index, ct18_icn, ct18_others, labels=['초거대 인프라(인천)', '타 인프라의 잔여 합계 면적'])
        ax18.set_title("18. 인천공항 절대 독점력 대항 지표 누적 Area")
        ax18.legend(loc='upper left')
        st.pyplot(fig18)

with tab4:
    st.subheader("타겟 심층 그룹 기반의 교차/정밀 뷰어망 (고급 모드)")
    if not filtered_nat.empty:
        r8_1, r8_2 = st.columns(2)
        with r8_1:
            ct7 = filtered_nat.pivot_table(index='목적별', columns='연령별', values='인원수', aggfunc='sum').fillna(0)
            fig7, ax7 = plt.subplots(figsize=(6,5))
            img = ax7.imshow(ct7.values, cmap='YlGnBu', aspect='auto')
            plt.colorbar(img, ax=ax7)
            ax7.set_xticks(range(len(ct7.columns)))
            ax7.set_xticklabels(ct7.columns, rotation=45)
            ax7.set_yticks(range(len(ct7.index)))
            ax7.set_yticklabels(ct7.index)
            ax7.set_title("07. 방한 목적-연령 변수의 충돌 계측을 위한 히트맵")
            st.pyplot(fig7)
            
        with r8_2:
            df_2024 = filtered_nat[filtered_nat['기준연월'].dt.year == 2024]
            fig12, ax12 = plt.subplots(figsize=(6,5))
            if not df_2024.empty:
                ct12 = df_2024.groupby('연령별')['인원수'].sum().sort_values(ascending=False)
                ct12.plot(kind='bar', color='#FF69B4', ax=ax12)
                ax12.set_title("12. 당해(24년) 트렌드로 스코프를 축소한 연령별 막대")
                plt.xticks(rotation=45)
                st.pyplot(fig12)
            else:
                st.info("2024년도 필터 조건 구간이 설정되지 않았습니다.")

        r9_1, r9_2 = st.columns(2)
        with r9_1:
            ct13 = filtered_nat.pivot_table(index='목적별', columns='성별', values='인원수', aggfunc='sum').fillna(0)
            fig13, ax13 = plt.subplots(figsize=(6,5))
            ct13.plot(kind='bar', ax=ax13, cmap='autumn')
            ax13.set_title("13. 그룹단위 분할! 방문목적+성비 병렬 교착")
            plt.xticks(rotation=0)
            st.pyplot(fig13)
            
        with r9_2:
            crew_df = filtered_nat[filtered_nat['성별'] == '승무원']
            if not crew_df.empty:
                ct15 = crew_df.groupby('목적별')['인원수'].sum()
                fig15, ax15 = plt.subplots(figsize=(6,5))
                ct15.plot(kind='pie', autopct='%1.1f%%', cmap='coolwarm', ax=ax15)
                ax15.set_title("15. 운수노동 근로자('승무원')의 입국 사유율 분석")
                ax15.set_ylabel('')
                st.pyplot(fig15)
            else:
                st.info("승무원 그룹 전용 지표 데이터 없음")

        r10_1, r10_2 = st.columns(2)
        with r10_1:
            target_w = filtered_nat[(filtered_nat['성별'] == '여성') & (filtered_nat['연령별'].isin(['21~30세', '31~40세']))]
            fig16, ax16 = plt.subplots(figsize=(6,5))
            if not target_w.empty:
                target_w.groupby('기준연월')['인원수'].sum().plot(kind='line', color='#C71585', marker='d', ax=ax16)
                ax16.set_title("16. 주력 소비군 (K-컬쳐 타겟, 매력 21~40세 여성) 동향형 선 그래프")
                st.pyplot(fig16)
            else:
                st.info("조건 내 해당 타겟 (2030 여성)이 없습니다.")
                
        with r10_2:
            non_tourist = filtered_nat[filtered_nat['목적별'] != '관광']
            if not non_tourist.empty and non_tourist['인원수'].sum() > 0:
                ct19 = non_tourist.groupby('목적별')['인원수'].sum()
                fig19, ax19 = plt.subplots(figsize=(6,5))
                ct19.plot(kind='pie', autopct='%1.1f%%', cmap='Wistia', pctdistance=0.85, ax=ax19)
                centre_circle = plt.Circle((0,0),0.70,fc='white')
                ax19.add_artist(centre_circle)
                ax19.set_title("19. '관광객이 아닌 그 외 유입자'의 비중 추적용 링(Donut) 디자인")
                ax19.set_ylabel('')
                st.pyplot(fig19)
            else:
                st.info("순수 관광을 제외한 데이터 수집 불가.")

st.markdown("---")
st.caption("koreatravel Explorer App Powered By Python Streamlit / Analysis Limit: 20 Chart Edition (v2.0) | Imputation Integrity Checked.")
