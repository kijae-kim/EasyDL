
# Simple Kospi - 데이터 분석 리포트
**생성 일시**: 2026-01-13 17:34:59

## 1. 주요 발견사항

### 특징 중요도 (Mutual Information Top 5)
14. **kospi_ma60**: 0.0269
11. **kospi_range_pct**: 0.0220
8. **kospi_return**: 0.0198
12. **kospi_ma5**: 0.0171
20. **kospi_volume_ma5**: 0.0126

### 타겟과 상관관계 Top 5
22. **kospi_rsi**: 0.0758
13. **kospi_ma20**: -0.0725
14. **kospi_ma60**: -0.0715
12. **kospi_ma5**: -0.0643
3. **kospi_low**: -0.0629

## 2. 데이터 특성

- **정규화**: StandardScaler 적용됨
- **특징 개수**: 24개
- **타겟 균형**: 상승 54%, 하락 46% (비교적 균형)
- **시계열 특성**: 이동평균, 변동성 등 시계열 패턴 포함

## 3. 모델 학습 제안

### 추천 특징 (중요도 기반)
1. kospi_ma60
2. kospi_range_pct
3. kospi_return
4. kospi_ma5
5. kospi_volume_ma5
6. kospi_kodex_ratio
7. kodex_return
8. kospi_high
9. kospi_volume_ratio
10. kospi_range

### 모델 선택 가이드
- **선형 회귀**: 기본 베이스라인, 해석 용이
- **로지스틱 회귀**: 이진 분류에 최적화, 확률 출력
- **MLP**: 비선형 패턴 학습 가능, 성능 최고

## 4. 예상 성능

- **Random Baseline**: ~50% (상승/하락 5:5)
- **목표 성능**: 55-60% 정확도
- **실전 기준**: 53% 이상이면 수익 가능

## 5. 다음 단계

- [ ] 선형 회귀 모델 구현 및 학습
- [ ] 로지스틱 회귀 모델 구현 및 학습
- [ ] MLP 모델 구현 및 학습
- [ ] 3가지 모델 성능 비교
- [ ] 최종 모델 선정 및 평가
