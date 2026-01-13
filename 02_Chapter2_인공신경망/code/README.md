# Simple Kospi - KOSPI 등락 예측 모델

> Chapter 2 (인공신경망) 학습 내용을 실전 데이터로 직접 구현한 프로젝트

## 프로젝트 소개

KOSPI 지수와 KODEX200 ETF 데이터를 활용하여 다음날 주가 등락을 예측하는 머신러닝 프로젝트입니다.
교재의 YouTube 수익 예측 예제 대신, **금융 데이터에 관심이 있어 자발적으로 데이터를 수집하고 실습**했습니다.

## 기획 배경

Chapter 2에서 학습한 개념들을 실전에 적용하기 위해:
- **선형 회귀**: 기본 회귀 모델로 수익률 예측
- **로지스틱 회귀**: 이진 분류로 등락 방향 예측
- **MLP (다층 퍼셉트론)**: 비선형 패턴 학습으로 성능 개선 시도

교재 예제를 따라하는 대신, 실제 관심 분야(금융)의 데이터로 학습하면서 **데이터 수집부터 모델 평가까지 전 과정을 경험**했습니다.

## 주요 발견

### 1. 주가 예측의 어려움
- 최고 성능: **49.79%** (Logistic Regression)
- Random Baseline: **50.00%**
- **단순 기술적 지표만으로는 주가 예측이 거의 불가능**함을 확인

### 2. 모델별 특징
| 모델 | Test Accuracy | 특징 |
|------|---------------|------|
| 선형 회귀 | R² = -0.057 | 수익률 변동성을 설명하지 못함 |
| 로지스틱 회귀 | 49.79% | 가장 안정적, 해석 용이 |
| MLP | 47.33% | Recall 높지만 False Positive 많음 |

### 3. 인사이트
- 월요일 효과 발견: 월요일 상승 확률 **62.28%** (통계적으로 유의)
- 특징 중요도: `kospi_ma60`, `kospi_range_pct`, `kospi_return`이 가장 중요
- 과적합 없이 안정적으로 학습됨 (Train-Test 격차 10% 미만)

### 4. 교훈
> "이론적으로 완벽한 모델도 실전 데이터에서는 한계가 있다"

금융 시장의 불확실성과 무작위성으로 인해 기술적 지표만으로는 예측이 어려움을 체감했습니다.
더 나은 성능을 위해서는 뉴스 감성 분석, 거시경제 지표 등 추가 데이터가 필요합니다.

## 기술 스택

- **Python 3.12**
- **데이터**: FinanceDataReader (KOSPI, KODEX200)
- **전처리**: Pandas, NumPy, scikit-learn
- **모델링**: scikit-learn, TensorFlow/Keras
- **시각화**: Matplotlib, Seaborn

## 실행 방법

### 1. 환경 설정
```bash
# 가상환경 활성화 (이미 설정된 경우)
source ../../EasyDL/bin/activate

# 필요한 패키지 설치
pip install finance-datareader yfinance scikit-learn tensorflow matplotlib seaborn
```

### 2. 단계별 실행

```bash
cd 02_Chapter2_인공신경망/code

# Stage 1: 데이터 수집 (KOSPI, KODEX200)
python 01_data_collection.py

# Stage 2: 데이터 전처리 (특징 생성, 정규화)
python 02_data_preprocessing.py

# Stage 3: 모델 설계 (3가지 모델 아키텍처)
python 03_model_design.py

# Stage 4: 모델 학습 (학습 및 평가)
python 04_model_training.py
```

### 3. 결과 확인

```bash
# 학습 리포트 확인
cat data/processed/model_training_report.md

# 생성된 시각화
open ../assets/training_curves.png
open ../assets/model_comparison.png
```

## 프로젝트 구조

```
02_Chapter2_인공신경망/
├── code/
│   ├── 01_data_collection.py       # 데이터 수집
│   ├── 02_data_preprocessing.py    # 전처리 및 특징 엔지니어링
│   ├── 03_model_design.py          # 모델 설계
│   ├── 04_model_training.py        # 모델 학습 및 평가
│   ├── analyze_data.py             # 데이터 심화 분석
│   ├── data/
│   │   ├── raw/                    # 원본 데이터
│   │   └── processed/              # 전처리된 데이터, 리포트
│   └── models/                     # 학습된 모델
├── assets/                         # 시각화 이미지
└── notes/                          # 학습 노트
```

## 데이터 정보

- **기간**: 2019-01-02 ~ 2024-12-30 (1,477일)
- **Train**: 2019-2023 (1,174개)
- **Test**: 2024년 (243개)
- **특징**: 24개 (MA, RSI, 변동성, 거래량 등)
- **타겟**: 다음날 등락 방향 (0: 하락, 1: 상승)

## 주요 결과

### 학습 곡선 (MLP)
- 21 epochs에서 Early Stopping
- Validation Loss 기준으로 최적 모델 저장
- 과적합 없이 안정적인 학습 확인

### 성능 비교
- **Logistic Regression**: 49.79% (최고 성능)
- **MLP**: 47.33% (Recall 83%, 상승 예측에 민감)
- **Linear Regression**: R² = -0.057 (회귀 태스크 부적합)

### 실전 적용성
- 실전 수익 기준 (53% 이상) 미달
- 추가 개선 필요:
  - 외부 데이터 (뉴스, 거시경제 지표)
  - 앙상블 모델
  - 시계열 모델 (LSTM, Transformer)

## 배운 점

1. **데이터 수집의 중요성**: 좋은 데이터 없이는 좋은 모델도 무용지물
2. **도메인 지식 필요성**: 금융 데이터는 노이즈가 많아 기술적 지표만으로는 한계
3. **Baseline의 중요성**: Random (50%)과 비교하여 모델 성능 검증
4. **과적합 방지**: Dropout, Early Stopping으로 일반화 성능 확보
5. **평가 지표 이해**: Accuracy만으론 부족, Precision/Recall/F1 종합 고려

## 참고 자료

- [WikiDocs - 딥러닝 파이토치 교과서](https://wikidocs.net/227292)
- FinanceDataReader 라이브러리
- scikit-learn Documentation
- TensorFlow/Keras Documentation

---

**작성자**: 김기재
**작성일**: 2026-01-13
**목적**: Chapter 2 인공신경망 학습 및 실전 적용 연습
