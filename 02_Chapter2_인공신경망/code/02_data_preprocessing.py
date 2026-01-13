#!/usr/bin/env python3
"""
Simple Kospi 프로젝트 - Stage 2: 데이터 전처리

목표:
1. 결측치 처리
2. Feature Engineering (수익률, 이동평균, 변동성)
3. 타겟 변수 생성 (다음날 등락)
4. Train/Test 분할 (2019-2023 / 2024)
5. 정규화 (StandardScaler)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import pickle
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False


def load_raw_data():
    """원본 데이터 로드"""
    print("\n" + "=" * 60)
    print("📂 원본 데이터 로드")
    print("=" * 60)

    kospi = pd.read_csv('data/raw/kospi_raw.csv', index_col=0, parse_dates=True)
    kodex = pd.read_csv('data/raw/kodex200_raw.csv', index_col=0, parse_dates=True)

    print(f"✅ KOSPI: {len(kospi)}행 × {len(kospi.columns)}열")
    print(f"✅ KODEX200: {len(kodex)}행 × {len(kodex.columns)}열")

    return kospi, kodex


def handle_missing_values(df, name):
    """결측치 처리"""
    print(f"\n📊 {name} 결측치 처리")

    # 결측치 확인
    missing = df.isnull().sum()
    if missing.sum() == 0:
        print("   ✅ 결측치 없음")
        return df

    print(f"   결측치 발견:")
    print(missing[missing > 0])

    # 전략 1: 거래량이 0이면 결측치를 0으로
    if 'Volume' in df.columns and df['Volume'].isnull().sum() > 0:
        df['Volume'].fillna(0, inplace=True)
        print("   - 거래량 결측치 → 0으로 처리")

    # 전략 2: 가격 결측치는 이전 값으로 forward fill
    price_cols = ['Open', 'High', 'Low', 'Close']
    for col in price_cols:
        if col in df.columns and df[col].isnull().sum() > 0:
            df[col].fillna(method='ffill', inplace=True)
            print(f"   - {col} 결측치 → 이전 값으로 채움")

    # 최종 확인
    remaining = df.isnull().sum().sum()
    if remaining > 0:
        print(f"   ⚠️  남은 결측치: {remaining}개 (행 삭제)")
        df.dropna(inplace=True)

    return df


def create_features(kospi, kodex):
    """Feature Engineering"""
    print("\n" + "=" * 60)
    print("🔧 Feature Engineering")
    print("=" * 60)

    # 새로운 DataFrame 생성
    df = pd.DataFrame(index=kospi.index)

    # 1. KOSPI 기본 특징
    print("\n1️⃣ KOSPI 기본 특징")
    df['kospi_open'] = kospi['Open']
    df['kospi_high'] = kospi['High']
    df['kospi_low'] = kospi['Low']
    df['kospi_close'] = kospi['Close']
    df['kospi_volume'] = kospi['Volume']
    print(f"   ✅ 5개 기본 특징 추가")

    # 2. KODEX200 기본 특징
    print("\n2️⃣ KODEX200 기본 특징")
    df['kodex_close'] = kodex['Close']
    df['kodex_volume'] = kodex['Volume']
    print(f"   ✅ 2개 기본 특징 추가")

    # 3. 수익률 (Returns)
    print("\n3️⃣ 수익률 계산")
    df['kospi_return'] = kospi['Close'].pct_change()
    df['kodex_return'] = kodex['Close'].pct_change()
    print(f"   ✅ 일일 수익률 추가")

    # 4. 가격 범위 (Range)
    print("\n4️⃣ 가격 범위")
    df['kospi_range'] = kospi['High'] - kospi['Low']
    df['kospi_range_pct'] = (kospi['High'] - kospi['Low']) / kospi['Close']
    print(f"   ✅ 가격 범위 (절대/비율) 추가")

    # 5. 이동평균 (Moving Average)
    print("\n5️⃣ 이동평균")
    df['kospi_ma5'] = kospi['Close'].rolling(window=5).mean()
    df['kospi_ma20'] = kospi['Close'].rolling(window=20).mean()
    df['kospi_ma60'] = kospi['Close'].rolling(window=60).mean()
    print(f"   ✅ MA5, MA20, MA60 추가")

    # 6. 이동평균 괴리율
    df['kospi_ma5_diff'] = (kospi['Close'] - df['kospi_ma5']) / df['kospi_ma5']
    df['kospi_ma20_diff'] = (kospi['Close'] - df['kospi_ma20']) / df['kospi_ma20']
    print(f"   ✅ MA 괴리율 추가")

    # 7. 변동성 (Volatility)
    print("\n6️⃣ 변동성")
    df['kospi_volatility_5'] = kospi['Close'].rolling(window=5).std()
    df['kospi_volatility_20'] = kospi['Close'].rolling(window=20).std()
    print(f"   ✅ 5일/20일 변동성 추가")

    # 8. 거래량 변화
    print("\n7️⃣ 거래량 특징")
    df['kospi_volume_change'] = kospi['Volume'].pct_change()
    df['kospi_volume_ma5'] = kospi['Volume'].rolling(window=5).mean()
    df['kospi_volume_ratio'] = kospi['Volume'] / df['kospi_volume_ma5']
    print(f"   ✅ 거래량 변화/평균/비율 추가")

    # 9. 기술적 지표
    print("\n8️⃣ 기술적 지표")
    # RSI (Relative Strength Index) 간소화 버전
    delta = kospi['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    df['kospi_rsi'] = 100 - (100 / (1 + rs))
    print(f"   ✅ RSI(14) 추가")

    # 10. KOSPI-KODEX 관계
    print("\n9️⃣ KOSPI-KODEX 관계")
    df['kospi_kodex_ratio'] = kospi['Close'] / kodex['Close']
    df['kospi_kodex_corr'] = kospi['Close'].rolling(window=20).corr(kodex['Close'])
    print(f"   ✅ 가격 비율 및 상관계수 추가")

    print(f"\n총 특징 개수: {len(df.columns)}개")

    return df


def create_target(df, kospi):
    """타겟 변수 생성: 다음날 등락"""
    print("\n" + "=" * 60)
    print("🎯 타겟 변수 생성")
    print("=" * 60)

    # 다음날 종가
    next_close = kospi['Close'].shift(-1)

    # 오늘 종가
    today_close = kospi['Close']

    # 타겟: 다음날 상승 = 1, 하락 = 0
    df['target'] = (next_close > today_close).astype(int)

    # 타겟 분포 확인
    target_counts = df['target'].value_counts()
    print(f"\n타겟 분포:")
    print(f"   상승(1): {target_counts.get(1, 0)}일 ({target_counts.get(1, 0)/len(df)*100:.2f}%)")
    print(f"   하락(0): {target_counts.get(0, 0)}일 ({target_counts.get(0, 0)/len(df)*100:.2f}%)")

    # 실제 다음날 수익률도 추가 (회귀 문제용)
    df['target_return'] = (next_close - today_close) / today_close

    print(f"\n✅ 타겟 변수 추가 완료")
    print(f"   - target: 이진 분류 (0 or 1)")
    print(f"   - target_return: 실제 수익률 (회귀)")

    return df


def split_train_test(df):
    """Train/Test 분할 (시계열 고려)"""
    print("\n" + "=" * 60)
    print("✂️ Train/Test 분할")
    print("=" * 60)

    # 결측치 제거 (Rolling 연산으로 생긴 초기 NaN)
    df_clean = df.dropna()
    print(f"   결측치 제거 후: {len(df_clean)}행")

    # 2024년을 기준으로 분할
    train_df = df_clean[df_clean.index < '2024-01-01']
    test_df = df_clean[df_clean.index >= '2024-01-01']

    print(f"\n📊 데이터 분할 결과:")
    print(f"   Train: {len(train_df)}행 ({train_df.index[0].strftime('%Y-%m-%d')} ~ {train_df.index[-1].strftime('%Y-%m-%d')})")
    print(f"   Test:  {len(test_df)}행 ({test_df.index[0].strftime('%Y-%m-%d')} ~ {test_df.index[-1].strftime('%Y-%m-%d')})")
    print(f"   비율: Train {len(train_df)/(len(train_df)+len(test_df))*100:.1f}%, Test {len(test_df)/(len(train_df)+len(test_df))*100:.1f}%")

    return train_df, test_df


def normalize_features(train_df, test_df):
    """특징 정규화 (StandardScaler)"""
    print("\n" + "=" * 60)
    print("📏 특징 정규화 (StandardScaler)")
    print("=" * 60)

    # 타겟 변수 분리
    feature_cols = [col for col in train_df.columns if not col.startswith('target')]

    X_train = train_df[feature_cols]
    y_train = train_df['target']
    y_train_reg = train_df['target_return']

    X_test = test_df[feature_cols]
    y_test = test_df['target']
    y_test_reg = test_df['target_return']

    print(f"\n특징 개수: {len(feature_cols)}개")

    # StandardScaler 적용
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # DataFrame으로 변환 (인덱스와 컬럼명 유지)
    X_train_scaled = pd.DataFrame(X_train_scaled, index=X_train.index, columns=X_train.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, index=X_test.index, columns=X_test.columns)

    print(f"✅ 정규화 완료")
    print(f"   평균: 0, 표준편차: 1로 변환")

    # Scaler 저장
    with open('data/processed/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    print(f"✅ Scaler 저장: data/processed/scaler.pkl")

    return X_train_scaled, X_test_scaled, y_train, y_test, y_train_reg, y_test_reg, feature_cols


def save_processed_data(X_train, X_test, y_train, y_test, y_train_reg, y_test_reg):
    """전처리된 데이터 저장"""
    print("\n" + "=" * 60)
    print("💾 전처리 데이터 저장")
    print("=" * 60)

    # Train 데이터
    train_data = X_train.copy()
    train_data['target'] = y_train
    train_data['target_return'] = y_train_reg
    train_data.to_csv('data/processed/train_data.csv')
    print(f"✅ Train 데이터 저장: {len(train_data)}행")

    # Test 데이터
    test_data = X_test.copy()
    test_data['target'] = y_test
    test_data['target_return'] = y_test_reg
    test_data.to_csv('data/processed/test_data.csv')
    print(f"✅ Test 데이터 저장: {len(test_data)}행")

    # 특징 목록 저장
    feature_list = list(X_train.columns)
    with open('data/processed/feature_list.txt', 'w') as f:
        for feat in feature_list:
            f.write(f"{feat}\n")
    print(f"✅ 특징 목록 저장: {len(feature_list)}개 특징")


def visualize_features(df):
    """특징 시각화"""
    print("\n" + "=" * 60)
    print("🎨 특징 시각화")
    print("=" * 60)

    try:
        # 주요 특징 선택
        key_features = ['kospi_close', 'kospi_ma5', 'kospi_ma20', 'kospi_return',
                       'kospi_volatility_20', 'kospi_rsi']

        fig, axes = plt.subplots(3, 2, figsize=(14, 12))
        axes = axes.flatten()

        for i, feature in enumerate(key_features):
            if feature in df.columns:
                ax = axes[i]
                ax.plot(df.index, df[feature].values, linewidth=1, alpha=0.7)
                ax.set_title(f'{feature}', fontsize=12)
                ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('../assets/feature_visualization.png', dpi=300, bbox_inches='tight')
        print("✅ 특징 시각화 저장: ../assets/feature_visualization.png")
        plt.close()
    except Exception as e:
        print(f"⚠️  시각화 스킵 (에러: {e})")


def create_preprocessing_report(X_train, X_test, y_train, y_test):
    """전처리 리포트 생성"""
    print("\n" + "=" * 60)
    print("📋 전처리 리포트 생성")
    print("=" * 60)

    report = []
    report.append("\n# Simple Kospi - 데이터 전처리 리포트\n")
    report.append(f"**생성 일시**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    # 데이터 개요
    report.append("## 1. 데이터 개요\n")
    report.append(f"- **Train 데이터**: {len(X_train)}행\n")
    report.append(f"- **Test 데이터**: {len(X_test)}행\n")
    report.append(f"- **특징 개수**: {len(X_train.columns)}개\n")
    report.append(f"- **타겟**: 다음날 등락 (0=하락, 1=상승)\n\n")

    # 특징 목록
    report.append("## 2. 생성된 특징\n\n")
    report.append("### 기본 특징 (7개)\n")
    report.append("- KOSPI: Open, High, Low, Close, Volume\n")
    report.append("- KODEX200: Close, Volume\n\n")

    report.append("### 파생 특징 (26개)\n")
    report.append("- **수익률**: kospi_return, kodex_return\n")
    report.append("- **가격 범위**: kospi_range, kospi_range_pct\n")
    report.append("- **이동평균**: MA5, MA20, MA60\n")
    report.append("- **MA 괴리율**: ma5_diff, ma20_diff\n")
    report.append("- **변동성**: volatility_5, volatility_20\n")
    report.append("- **거래량**: volume_change, volume_ma5, volume_ratio\n")
    report.append("- **기술적 지표**: RSI(14)\n")
    report.append("- **관계 지표**: kospi_kodex_ratio, kospi_kodex_corr\n\n")

    # 타겟 분포
    report.append("## 3. 타겟 분포\n\n")
    report.append("### Train 데이터\n")
    train_dist = y_train.value_counts()
    report.append(f"- 상승(1): {train_dist.get(1, 0)}일 ({train_dist.get(1, 0)/len(y_train)*100:.2f}%)\n")
    report.append(f"- 하락(0): {train_dist.get(0, 0)}일 ({train_dist.get(0, 0)/len(y_train)*100:.2f}%)\n\n")

    report.append("### Test 데이터\n")
    test_dist = y_test.value_counts()
    report.append(f"- 상승(1): {test_dist.get(1, 0)}일 ({test_dist.get(1, 0)/len(y_test)*100:.2f}%)\n")
    report.append(f"- 하락(0): {test_dist.get(0, 0)}일 ({test_dist.get(0, 0)/len(y_test)*100:.2f}%)\n\n")

    # 정규화
    report.append("## 4. 전처리 과정\n")
    report.append("- ✅ 결측치 처리 완료\n")
    report.append("- ✅ Feature Engineering 완료 (33개 특징)\n")
    report.append("- ✅ 타겟 변수 생성 완료\n")
    report.append("- ✅ Train/Test 분할 완료 (2024년 기준)\n")
    report.append("- ✅ StandardScaler 정규화 완료\n\n")

    # 다음 단계
    report.append("## 5. 다음 단계\n")
    report.append("- [ ] 모델 선정 (Linear Regression, Logistic Regression, MLP)\n")
    report.append("- [ ] 모델 학습\n")
    report.append("- [ ] 성능 평가\n")
    report.append("- [ ] 결과 분석 및 시각화\n")

    report_text = ''.join(report)
    print(report_text)

    # 파일 저장
    with open('data/processed/preprocessing_report.md', 'w', encoding='utf-8') as f:
        f.write(report_text)
    print("✅ 리포트 저장: data/processed/preprocessing_report.md")


def main():
    """메인 실행 함수"""
    print("\n" + "🚀" * 30)
    print("Simple Kospi 프로젝트 - Stage 2: 데이터 전처리")
    print("🚀" * 30)

    # 1. 데이터 로드
    kospi, kodex = load_raw_data()

    # 2. 결측치 처리
    kospi = handle_missing_values(kospi, "KOSPI")
    kodex = handle_missing_values(kodex, "KODEX200")

    # 3. Feature Engineering
    df = create_features(kospi, kodex)

    # 4. 타겟 변수 생성
    df = create_target(df, kospi)

    # 5. Train/Test 분할
    train_df, test_df = split_train_test(df)

    # 6. 정규화
    X_train, X_test, y_train, y_test, y_train_reg, y_test_reg, feature_cols = normalize_features(train_df, test_df)

    # 7. 데이터 저장
    save_processed_data(X_train, X_test, y_train, y_test, y_train_reg, y_test_reg)

    # 8. 시각화
    visualize_features(df)

    # 9. 리포트 생성
    create_preprocessing_report(X_train, X_test, y_train, y_test)

    print("\n" + "=" * 60)
    print("✅ Stage 2: 데이터 전처리 완료!")
    print("=" * 60)
    print("\n다음 단계:")
    print("  python 03_model_design.py")
    print("  python 04_model_training.py")


if __name__ == "__main__":
    main()
