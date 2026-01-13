# 🎯 Simple Kospi 프로젝트 기획서

> Chapter 2 인공신경망 실전 프로젝트: KOSPI 등락 예측 모델

---

## 📌 프로젝트 개요

### 목표
- Chapter 2에서 학습한 **선형 회귀(Linear Regression)** 개념을 실제 주식 데이터에 적용
- KOSPI 지수와 ETF 데이터를 활용한 **등락 예측 모델** 구현
- 데이터 수집부터 모델 평가까지 전체 ML 파이프라인 경험

### 예측 대상
**다음날 KOSPI 지수의 등락 (이진 분류)**
- 상승(1): 내일 종가 > 오늘 종가
- 하락(0): 내일 종가 ≤ 오늘 종가

### 데이터 소스
1. **KOSPI 지수 데이터**
   - 종가(Close)
   - 시가(Open)
   - 고가(High)
   - 저가(Low)
   - 거래량(Volume)

2. **KOSPI ETF 데이터** (KODEX200 등)
   - 종가
   - 거래량
   - 수익률

### 기간
- **학습 데이터**: 2019-01-01 ~ 2023-12-31 (5년)
- **테스트 데이터**: 2024-01-01 ~ 2024-12-31 (1년)

---

## 🗓️ 프로젝트 단계

### Stage 1: 데이터 수집 (Data Collection)

**목표**: KOSPI 지수 및 ETF 데이터 수집

**사용 라이브러리**:
- `yfinance`: 야후 파이낸스에서 주식 데이터 다운로드
- `pandas-datareader`: 대체 데이터 소스
- `FinanceDataReader`: 한국 주식 데이터 전용

**구현 파일**: `code/01_data_collection.py`

**수집할 데이터**:
```python
# KOSPI 지수
ticker_kospi = "^KS11"  # Yahoo Finance KOSPI 코드
# 또는 FinanceDataReader 사용
import FinanceDataReader as fdr
kospi = fdr.DataReader('KS11', '2019-01-01', '2024-12-31')

# KODEX200 ETF
kodex200 = fdr.DataReader('069500', '2019-01-01', '2024-12-31')
```

**저장 위치**: `code/data/raw/`
- `kospi_raw.csv`
- `kodex200_raw.csv`

**체크리스트**:
- [ ] `yfinance` 또는 `FinanceDataReader` 설치
- [ ] KOSPI 지수 데이터 다운로드 (2019-2024)
- [ ] KODEX200 데이터 다운로드
- [ ] 데이터 확인 (shape, columns, missing values)
- [ ] CSV 파일로 저장

---

### Stage 2: 데이터 전처리 (Data Preprocessing)

**목표**: 모델 학습에 적합한 형태로 데이터 변환

**구현 파일**: `code/02_data_preprocessing.py`

**전처리 단계**:

#### 2.1 결측치 처리
```python
# 결측치 확인
df.isnull().sum()

# 전략:
# - 거래량 결측 → 0으로 채우기 (거래 없었음)
# - 가격 결측 → 이전 값으로 채우기 (forward fill)
```

#### 2.2 Feature Engineering (특징 추출)
```python
# 기본 특징
df['return'] = df['Close'].pct_change()  # 수익률
df['range'] = df['High'] - df['Low']     # 가격 범위
df['volatility'] = df['Close'].rolling(5).std()  # 변동성

# 이동 평균
df['MA5'] = df['Close'].rolling(5).mean()   # 5일 이동평균
df['MA20'] = df['Close'].rolling(20).mean() # 20일 이동평균

# 타겟 변수 생성
df['target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
# 1: 다음날 상승, 0: 다음날 하락
```

#### 2.3 데이터 분할
```python
# 시계열 데이터는 섞지 않고 순차적으로 분할
train_data = df['2019':'2023']  # 학습 데이터
test_data = df['2024']           # 테스트 데이터
```

#### 2.4 정규화 (Normalization)
```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
train_scaled = scaler.fit_transform(train_data)
test_scaled = scaler.transform(test_data)
```

**저장 위치**: `code/data/processed/`
- `train_data.csv`
- `test_data.csv`
- `scaler.pkl` (정규화 파라미터)

**체크리스트**:
- [ ] 결측치 처리 완료
- [ ] Feature Engineering 구현
- [ ] 타겟 변수 생성 (다음날 등락)
- [ ] Train/Test 분할
- [ ] 정규화 적용
- [ ] 처리된 데이터 저장

---

### Stage 3: 모델 선정 및 설계 (Model Selection)

**목표**: Chapter 2의 개념을 적용한 모델 선택

**구현 파일**: `code/03_model_design.py`

#### 3.1 모델 후보

**Option 1: 선형 회귀 (Linear Regression)** ✅ **Chapter 2 개념**
```python
from sklearn.linear_model import LinearRegression

# y = ax + b 형태
# 입력: KOSPI 특징들 (종가, 거래량, 이동평균 등)
# 출력: 다음날 가격 (연속값)
```

**Option 2: 로지스틱 회귀 (Logistic Regression)** ✅ **분류 문제에 적합**
```python
from sklearn.linear_model import LogisticRegression

# 입력: KOSPI 특징들
# 출력: 등락 확률 (0 or 1)
```

**Option 3: 간단한 신경망 (MLP)** ✅ **Chapter 2 인공신경망**
```python
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Dense(8, activation='relu', input_shape=(n_features,)),
    keras.layers.Dense(4, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')  # 이진 분류
])
```

#### 3.2 최종 선정 모델

**Phase 1**: 선형 회귀 (Baseline)
- Chapter 2 내용 직접 적용
- 간단하고 해석 가능
- Loss: MSE (Mean Squared Error)

**Phase 2**: 로지스틱 회귀
- 이진 분류에 최적화
- Loss: Binary Cross-Entropy

**Phase 3**: 간단한 MLP
- 비선형 패턴 학습 가능
- Hidden Layer 2개

**비교 평가**:
- 3가지 모델 모두 구현하여 성능 비교
- Chapter 2 → Chapter 4 개념으로 확장

**체크리스트**:
- [ ] 선형 회귀 모델 정의
- [ ] 로지스틱 회귀 모델 정의
- [ ] MLP 모델 설계 (TensorFlow/PyTorch)
- [ ] Loss 함수 정의 (MSE, BCE)
- [ ] 평가 지표 선정 (Accuracy, Precision, Recall)

---

### Stage 4: 모델 학습 (Training)

**목표**: 선정한 모델을 학습 데이터로 훈련

**구현 파일**: `code/04_model_training.py`

#### 4.1 선형 회귀 학습
```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# 모델 초기화
model_lr = LinearRegression()

# 학습
model_lr.fit(X_train, y_train)

# 평가
y_pred = model_lr.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

print(f"MSE: {mse}")
print(f"가중치(a): {model_lr.coef_}")
print(f"바이어스(b): {model_lr.intercept_}")
```

#### 4.2 로지스틱 회귀 학습
```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

model_logistic = LogisticRegression()
model_logistic.fit(X_train, y_train)

y_pred = model_logistic.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"정확도: {accuracy}")
print(classification_report(y_test, y_pred))
```

#### 4.3 MLP 학습
```python
import tensorflow as tf

# 모델 정의
model_mlp = tf.keras.Sequential([
    tf.keras.layers.Dense(8, activation='relu', input_shape=(n_features,)),
    tf.keras.layers.Dense(4, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# 컴파일
model_mlp.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# 학습
history = model_mlp.fit(
    X_train, y_train,
    epochs=50,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)
```

#### 4.4 학습 과정 시각화
```python
import matplotlib.pyplot as plt

# Loss 그래프
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.savefig('../assets/training_loss.png')
```

**저장 위치**:
- 모델: `code/models/`
  - `linear_regression.pkl`
  - `logistic_regression.pkl`
  - `mlp_model.h5`
- 학습 그래프: `assets/`

**체크리스트**:
- [ ] 선형 회귀 학습 및 평가
- [ ] 로지스틱 회귀 학습 및 평가
- [ ] MLP 학습 및 평가
- [ ] 학습 과정 시각화 (Loss 그래프)
- [ ] 모델 저장

---

### Stage 5: 결과 평가 및 분석 (Evaluation)

**목표**: 모델 성능 평가 및 결과 분석

**구현 파일**: `code/05_evaluation.py`

#### 5.1 평가 지표

**분류 문제 지표**:
```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_auc_score
)

# 정확도 (Accuracy)
accuracy = accuracy_score(y_test, y_pred)

# 정밀도 (Precision): 상승 예측 중 실제 상승 비율
precision = precision_score(y_test, y_pred)

# 재현율 (Recall): 실제 상승 중 예측 성공 비율
recall = recall_score(y_test, y_pred)

# F1-Score
f1 = f1_score(y_test, y_pred)

# ROC-AUC
roc_auc = roc_auc_score(y_test, y_pred_proba)
```

**회귀 문제 지표** (선형 회귀):
```python
from sklearn.metrics import mean_squared_error, r2_score

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)
```

#### 5.2 결과 시각화

**Confusion Matrix**:
```python
import seaborn as sns

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.savefig('../assets/confusion_matrix.png')
```

**예측 vs 실제 비교**:
```python
plt.figure(figsize=(12, 6))
plt.plot(y_test.values, label='Actual', alpha=0.7)
plt.plot(y_pred, label='Predicted', alpha=0.7)
plt.xlabel('Time')
plt.ylabel('KOSPI Direction (0=하락, 1=상승)')
plt.legend()
plt.savefig('../assets/prediction_comparison.png')
```

**수익률 시뮬레이션**:
```python
# 예측에 따라 매수/매도 전략 시뮬레이션
initial_capital = 10000000  # 1천만원
portfolio = initial_capital

for i in range(len(y_test)):
    if y_pred[i] == 1:  # 상승 예측 → 매수
        portfolio *= (1 + returns[i])
    # 하락 예측 → 보유 (또는 공매도)

print(f"최종 자산: {portfolio:,.0f}원")
print(f"수익률: {(portfolio/initial_capital - 1)*100:.2f}%")
```

#### 5.3 모델 비교

**성능 비교 테이블**:
```python
results = pd.DataFrame({
    'Model': ['Linear Regression', 'Logistic Regression', 'MLP'],
    'Accuracy': [acc_lr, acc_log, acc_mlp],
    'Precision': [prec_lr, prec_log, prec_mlp],
    'Recall': [rec_lr, rec_log, rec_mlp],
    'F1-Score': [f1_lr, f1_log, f1_mlp]
})

print(results)
results.to_csv('../assets/model_comparison.csv')
```

**시각화**:
```python
results.plot(x='Model', kind='bar', figsize=(10, 6))
plt.ylabel('Score')
plt.title('Model Performance Comparison')
plt.savefig('../assets/model_comparison.png')
```

**체크리스트**:
- [ ] 평가 지표 계산 (Accuracy, Precision, Recall, F1)
- [ ] Confusion Matrix 생성
- [ ] 예측 vs 실제 그래프 생성
- [ ] 수익률 시뮬레이션 실행
- [ ] 3가지 모델 성능 비교
- [ ] 결과 분석 리포트 작성

---

## 📊 예상 산출물

### 코드 파일 (`02_Chapter2_인공신경망/code/`)
```
code/
├── data/
│   ├── raw/
│   │   ├── kospi_raw.csv
│   │   └── kodex200_raw.csv
│   └── processed/
│       ├── train_data.csv
│       └── test_data.csv
├── models/
│   ├── linear_regression.pkl
│   ├── logistic_regression.pkl
│   └── mlp_model.h5
├── 01_data_collection.py
├── 02_data_preprocessing.py
├── 03_model_design.py
├── 04_model_training.py
└── 05_evaluation.py
```

### 시각화 자료 (`02_Chapter2_인공신경망/assets/`)
```
assets/
├── kospi_price_history.png        # KOSPI 가격 추이
├── feature_distribution.png       # 특징 분포 히스토그램
├── correlation_matrix.png         # 특징 간 상관관계
├── training_loss.png              # 학습 Loss 그래프
├── confusion_matrix.png           # 혼동 행렬
├── prediction_comparison.png      # 예측 vs 실제
├── portfolio_performance.png      # 수익률 시뮬레이션
└── model_comparison.png           # 모델 성능 비교
```

### 노트 (`02_Chapter2_인공신경망/notes/`)
```
notes/
├── 인공신경망.md                  # 기존 노트 (보강)
├── Simple_Kospi_학습노트.md       # 프로젝트 학습 기록
└── Simple_Kospi_결과분석.md       # 최종 결과 분석
```

---

## 🔧 필요한 라이브러리

### 설치 명령어
```bash
pip install yfinance
pip install FinanceDataReader
pip install scikit-learn
pip install tensorflow  # 또는 pytorch
pip install matplotlib seaborn
pip install pandas numpy
```

### requirements.txt 추가
```txt
# Simple Kospi 프로젝트
yfinance>=0.2.0
FinanceDataReader>=0.9.0
scikit-learn>=1.3.0
```

---

## 📅 예상 소요 시간

| 단계 | 예상 시간 | 난이도 |
|------|----------|--------|
| Stage 1: 데이터 수집 | 1-2시간 | ⭐⭐☆☆☆ |
| Stage 2: 전처리 | 2-3시간 | ⭐⭐⭐☆☆ |
| Stage 3: 모델 설계 | 1-2시간 | ⭐⭐☆☆☆ |
| Stage 4: 학습 | 2-3시간 | ⭐⭐⭐☆☆ |
| Stage 5: 평가 | 2-3시간 | ⭐⭐⭐⭐☆ |
| **총 소요 시간** | **8-13시간** | **⭐⭐⭐☆☆** |

---

## 🎯 학습 목표 달성

### Chapter 2 개념 적용
- ✅ 선형 회귀 (Linear Regression) 실습
- ✅ Loss 함수 (MSE, BCE) 이해
- ✅ 가중치(Weight)와 바이어스(Bias) 학습 과정 확인
- ✅ 인공신경망(MLP) 구조 이해

### 추가 학습 효과
- ✅ 실전 데이터 전처리 경험
- ✅ 시계열 데이터 특성 이해
- ✅ 모델 평가 지표 활용
- ✅ 금융 데이터 분석 입문

---

## 🚀 다음 단계

프로젝트 완료 후:
1. **Chapter 3**: Gradient Descent 최적화 기법 적용
2. **Chapter 4**: Sigmoid/Softmax를 활용한 분류 개선
3. **Chapter 7**: CNN을 활용한 차트 이미지 분석
4. **Chapter 8**: LSTM/Transformer를 활용한 시계열 예측

---

## 📝 참고 자료

- **강의**: [Chapter 2 인공신경망 이해하기](https://youtu.be/jBGKm7tUZiI)
- **데이터**: Yahoo Finance, FinanceDataReader
- **모델**: scikit-learn, TensorFlow
- **시각화**: Matplotlib, Seaborn

---

**작성일**: 2026-01-13
**프로젝트 상태**: 📋 기획 완료 → 🚀 구현 대기
**예상 완료일**: 2026-01-15
