# 프로젝트명: 방한 외래관광객 탐색적 데이터 분석 (koreatravel EDA)

## 📌 1. 프로젝트 개요
본 프로젝트는 방한 외래관광객 데이터(국적별, 교통수단별 통계 데이터베이스)를 바탕으로 심층적인 탐색적 데이터 분석(EDA)을 수행하는 것을 목적으로 합니다. 
데이터 클렌징 및 요약 정보 파악, 기초 기술통계 산출, 피봇테이블 연산과 더불어 총 10가지 이상의 다변량 데이터 시각화를 도출하였으며, 상세한 분석 인사이트를 담은 종합 리포트를 제공합니다.

## 📂 2. 폴더 구조
제출용 `koreatravel` 프로젝트는 아래와 같은 구조로 이루어져 있습니다.

```text
koreatravel/
│
├── README.md               # 프로젝트 개요 및 실행 방법 안내
├── requirements.txt        # 필요 파이썬 패키지 목록
│
├── data/
│   └── raw/                # 원본 데이터 파일 보관
│       ├── visitor_by_nationality.csv
│       └── visitor_by_transport.csv
│
├── src/                    
│   └── eda_analysis.py     # 파이썬 메인 데이터 분석(EDA) 스크립트 코드
│
├── images/                 # 분석 결과로 자동 생성되는 시각화 에셋 (총 10건)
│   ├── 01_gender_total.png
│   ├── ...
│   └── 10_transport_pie.png
│
└── docs/                   
    ├── eda_report.md       # 핵심! 통계표, 교차표, 시각화 해석이 포함된 최종 EDA 리포트
    └── eda_stdout_utf8.txt # 스크립트 실행 과정에서 출력된 로그 원본
```

## 🚀 3. 필수 실행 방법 (Usage)
1. Python 환경에서 필요한 라이브러리를 설치합니다. (`uv` 또는 기본 `pip` 가상환경 활용 권장)
   ```bash
   pip install -r requirements.txt
   ```
2. **[선택 1] 정적 EDA 코드 실행**: 파이썬 분석 스크립트를 실행해 10종의 시각화(.png)를 자동 저장합니다.
   ```bash
   python src/eda_analysis.py
   ```
3. **[선택 2] 반응형 웹 대시보드 실행 (차트 값 확인 목적)**: 마우스 커서를 올려 그래프의 상세 수치(hover values)를 직접 확인할 수 있는 **Interactive Dashboard**를 브라우저에 실행합니다.
   ```bash
   streamlit run src/app.py
   ```

## 💡 4. 프로젝트 기술 특이사항 (사전 정의 규칙)
- **언어 및 환경**: Python 3.10+ 기반
- **주요 라이브러리**: `pandas`, `matplotlib`, `koreanize-matplotlib`, `scikit-learn` 등
- **개발 환경 제약 조건 준수**: 본 분석에서는 디자인 과의존 및 라이브러리 종속성 문제를 방지하기 위해 `seaborn` 관련 스타일 설정을 일절 배제하였습니다. 오직 순수 `matplotlib`과 한글 폰트 적용을 위한 `koreanize-matplotlib`만을 활용하여 모든 시각화를 독자적으로 커스텀 구현한 것이 특징입니다.
