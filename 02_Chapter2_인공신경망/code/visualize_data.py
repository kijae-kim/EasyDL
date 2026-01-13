#!/usr/bin/env python3
"""
Simple Kospi - 수집한 데이터 시각화

목표:
- KOSPI와 KODEX200 가격 추이 시각화
- 거래량 비교
- 기본 통계 분석
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")


def load_data():
    """데이터 로드"""
    print("📂 데이터 로딩...")
    kospi = pd.read_csv('data/raw/kospi_raw.csv', index_col=0, parse_dates=True)
    kodex = pd.read_csv('data/raw/kodex200_raw.csv', index_col=0, parse_dates=True)
    print(f"✅ KOSPI: {len(kospi)}행, KODEX200: {len(kodex)}행")
    return kospi, kodex


def visualize_price_trends(kospi, kodex):
    """가격 추이 시각화"""
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))

    # KOSPI 종가
    ax1 = axes[0]
    ax1.plot(kospi.index, kospi['Close'], linewidth=1.5, color='blue', alpha=0.8)
    ax1.fill_between(kospi.index, kospi['Close'], alpha=0.2, color='blue')
    ax1.set_title('KOSPI 지수 추이 (2019-2024)', fontsize=16, pad=15)
    ax1.set_xlabel('날짜', fontsize=12)
    ax1.set_ylabel('KOSPI 지수', fontsize=12)
    ax1.grid(True, alpha=0.3)

    # 주요 이벤트 표시
    ax1.axvline(pd.Timestamp('2020-03-19'), color='red', linestyle='--', alpha=0.5, label='COVID-19 저점')
    ax1.axvline(pd.Timestamp('2021-06-30'), color='green', linestyle='--', alpha=0.5, label='역대 최고점')
    ax1.legend(fontsize=10)

    # KODEX200 종가
    ax2 = axes[1]
    ax2.plot(kodex.index, kodex['Close'], linewidth=1.5, color='green', alpha=0.8)
    ax2.fill_between(kodex.index, kodex['Close'], alpha=0.2, color='green')
    ax2.set_title('KODEX200 ETF 추이 (2019-2024)', fontsize=16, pad=15)
    ax2.set_xlabel('날짜', fontsize=12)
    ax2.set_ylabel('KODEX200 가격', fontsize=12)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('../assets/kospi_price_trends.png', dpi=300, bbox_inches='tight')
    print("✅ 가격 추이 그래프 저장: ../assets/kospi_price_trends.png")
    plt.close()


def visualize_returns(kospi, kodex):
    """수익률 분포 시각화"""
    # 일일 수익률 계산
    kospi_returns = kospi['Close'].pct_change().dropna()
    kodex_returns = kodex['Close'].pct_change().dropna()

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # KOSPI 수익률 히스토그램
    axes[0, 0].hist(kospi_returns * 100, bins=50, alpha=0.7, color='blue', edgecolor='black')
    axes[0, 0].axvline(0, color='red', linestyle='--', linewidth=2)
    axes[0, 0].set_title('KOSPI 일일 수익률 분포', fontsize=14)
    axes[0, 0].set_xlabel('수익률 (%)', fontsize=11)
    axes[0, 0].set_ylabel('빈도', fontsize=11)
    axes[0, 0].grid(True, alpha=0.3)

    # KODEX200 수익률 히스토그램
    axes[0, 1].hist(kodex_returns * 100, bins=50, alpha=0.7, color='green', edgecolor='black')
    axes[0, 1].axvline(0, color='red', linestyle='--', linewidth=2)
    axes[0, 1].set_title('KODEX200 일일 수익률 분포', fontsize=14)
    axes[0, 1].set_xlabel('수익률 (%)', fontsize=11)
    axes[0, 1].set_ylabel('빈도', fontsize=11)
    axes[0, 1].grid(True, alpha=0.3)

    # 수익률 시계열
    axes[1, 0].plot(kospi_returns.index, kospi_returns * 100, linewidth=0.8, color='blue', alpha=0.6)
    axes[1, 0].axhline(0, color='red', linestyle='--', linewidth=1)
    axes[1, 0].set_title('KOSPI 일일 수익률 시계열', fontsize=14)
    axes[1, 0].set_xlabel('날짜', fontsize=11)
    axes[1, 0].set_ylabel('수익률 (%)', fontsize=11)
    axes[1, 0].grid(True, alpha=0.3)

    # 변동성 (20일 rolling std)
    kospi_volatility = kospi_returns.rolling(20).std() * np.sqrt(252) * 100
    axes[1, 1].plot(kospi_volatility.index, kospi_volatility, linewidth=1.5, color='purple')
    axes[1, 1].fill_between(kospi_volatility.index, kospi_volatility, alpha=0.3, color='purple')
    axes[1, 1].set_title('KOSPI 변동성 (연율화, 20일 이동평균)', fontsize=14)
    axes[1, 1].set_xlabel('날짜', fontsize=11)
    axes[1, 1].set_ylabel('변동성 (%)', fontsize=11)
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('../assets/kospi_returns_analysis.png', dpi=300, bbox_inches='tight')
    print("✅ 수익률 분석 그래프 저장: ../assets/kospi_returns_analysis.png")
    plt.close()

    # 통계 출력
    print("\n📊 수익률 통계:")
    print(f"   KOSPI 평균 수익률: {kospi_returns.mean()*100:.4f}%")
    print(f"   KOSPI 표준편차: {kospi_returns.std()*100:.4f}%")
    print(f"   KOSPI 최대 상승: {kospi_returns.max()*100:.2f}%")
    print(f"   KOSPI 최대 하락: {kospi_returns.min()*100:.2f}%")


def visualize_correlation(kospi, kodex):
    """KOSPI와 KODEX200 상관관계"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 정규화 (2019-01-02 = 100)
    kospi_norm = (kospi['Close'] / kospi['Close'].iloc[0]) * 100
    kodex_norm = (kodex['Close'] / kodex['Close'].iloc[0]) * 100

    # 정규화된 가격 비교
    axes[0].plot(kospi_norm.index, kospi_norm, label='KOSPI', linewidth=1.5, alpha=0.8)
    axes[0].plot(kodex_norm.index, kodex_norm, label='KODEX200', linewidth=1.5, alpha=0.8)
    axes[0].set_title('정규화된 가격 비교 (2019-01-02 = 100)', fontsize=14)
    axes[0].set_xlabel('날짜', fontsize=11)
    axes[0].set_ylabel('지수 (base=100)', fontsize=11)
    axes[0].legend(fontsize=11)
    axes[0].grid(True, alpha=0.3)

    # 산점도
    axes[1].scatter(kospi['Close'], kodex['Close'], alpha=0.3, s=10)
    axes[1].set_title('KOSPI vs KODEX200 산점도', fontsize=14)
    axes[1].set_xlabel('KOSPI 종가', fontsize=11)
    axes[1].set_ylabel('KODEX200 종가', fontsize=11)
    axes[1].grid(True, alpha=0.3)

    # 상관계수 계산
    corr = kospi['Close'].corr(kodex['Close'])
    axes[1].text(0.05, 0.95, f'상관계수: {corr:.4f}',
                transform=axes[1].transAxes,
                fontsize=12,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    plt.savefig('../assets/kospi_correlation.png', dpi=300, bbox_inches='tight')
    print(f"✅ 상관관계 그래프 저장: ../assets/kospi_correlation.png")
    print(f"   KOSPI-KODEX200 상관계수: {corr:.4f}")
    plt.close()


def main():
    """메인 함수"""
    print("\n" + "=" * 60)
    print("📊 Simple Kospi - 데이터 시각화")
    print("=" * 60 + "\n")

    # 데이터 로드
    kospi, kodex = load_data()

    # 시각화
    print("\n🎨 시각화 생성 중...")
    visualize_price_trends(kospi, kodex)
    visualize_returns(kospi, kodex)
    visualize_correlation(kospi, kodex)

    print("\n" + "=" * 60)
    print("✅ 시각화 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()
