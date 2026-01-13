
# Simple Kospi - 데이터 전처리 리포트
**생성 일시**: 2026-01-13 17:31:26

## 1. 데이터 개요
- **Train 데이터**: 1174행
- **Test 데이터**: 243행
- **특징 개수**: 24개
- **타겟**: 다음날 등락 (0=하락, 1=상승)

## 2. 생성된 특징

### 기본 특징 (7개)
- KOSPI: Open, High, Low, Close, Volume
- KODEX200: Close, Volume

### 파생 특징 (26개)
- **수익률**: kospi_return, kodex_return
- **가격 범위**: kospi_range, kospi_range_pct
- **이동평균**: MA5, MA20, MA60
- **MA 괴리율**: ma5_diff, ma20_diff
- **변동성**: volatility_5, volatility_20
- **거래량**: volume_change, volume_ma5, volume_ratio
- **기술적 지표**: RSI(14)
- **관계 지표**: kospi_kodex_ratio, kospi_kodex_corr

## 3. 타겟 분포

### Train 데이터
- 상승(1): 638일 (54.34%)
- 하락(0): 536일 (45.66%)

### Test 데이터
- 상승(1): 120일 (49.38%)
- 하락(0): 123일 (50.62%)

## 4. 전처리 과정
- ✅ 결측치 처리 완료
- ✅ Feature Engineering 완료 (33개 특징)
- ✅ 타겟 변수 생성 완료
- ✅ Train/Test 분할 완료 (2024년 기준)
- ✅ StandardScaler 정규화 완료

## 5. 다음 단계
- [ ] 모델 선정 (Linear Regression, Logistic Regression, MLP)
- [ ] 모델 학습
- [ ] 성능 평가
- [ ] 결과 분석 및 시각화
