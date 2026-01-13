#!/usr/bin/env python3
"""
Simple Kospi 프로젝트 - Stage 1: 데이터 수집

목표:
- KOSPI 지수 데이터 다운로드 (2019-2024)
- KODEX200 ETF 데이터 다운로드 (2019-2024)
- CSV 파일로 저장
- 데이터 확인 및 기본 통계
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

try:
    import FinanceDataReader as fdr
    USE_FDR = True
    print("✅ FinanceDataReader 사용")
except ImportError:
    import yfinance as yf
    USE_FDR = False
    print("⚠️  FinanceDataReader 없음, yfinance 사용")


def download_kospi_data(start_date='2019-01-01', end_date='2024-12-31'):
    """
    KOSPI 지수 데이터 다운로드

    Args:
        start_date: 시작 날짜 (YYYY-MM-DD)
        end_date: 종료 날짜 (YYYY-MM-DD)

    Returns:
        DataFrame: KOSPI 데이터
    """
    print("\n" + "=" * 60)
    print("📊 KOSPI 지수 데이터 다운로드")
    print("=" * 60)

    try:
        if USE_FDR:
            # FinanceDataReader 사용
            df = fdr.DataReader('KS11', start_date, end_date)
            print(f"✅ FinanceDataReader로 KOSPI 데이터 다운로드 완료")
        else:
            # yfinance 사용
            df = yf.download('^KS11', start=start_date, end=end_date, progress=False)
            print(f"✅ yfinance로 KOSPI 데이터 다운로드 완료")

        # 데이터 확인
        print(f"   기간: {df.index[0].strftime('%Y-%m-%d')} ~ {df.index[-1].strftime('%Y-%m-%d')}")
        print(f"   데이터 개수: {len(df)}행")
        print(f"   컬럼: {list(df.columns)}")

        return df

    except Exception as e:
        print(f"❌ KOSPI 데이터 다운로드 실패: {e}")
        return None


def download_kodex200_data(start_date='2019-01-01', end_date='2024-12-31'):
    """
    KODEX200 ETF 데이터 다운로드

    Args:
        start_date: 시작 날짜 (YYYY-MM-DD)
        end_date: 종료 날짜 (YYYY-MM-DD)

    Returns:
        DataFrame: KODEX200 데이터
    """
    print("\n" + "=" * 60)
    print("📊 KODEX200 ETF 데이터 다운로드")
    print("=" * 60)

    try:
        if USE_FDR:
            # FinanceDataReader 사용 (한국 주식 코드)
            df = fdr.DataReader('069500', start_date, end_date)
            print(f"✅ FinanceDataReader로 KODEX200 데이터 다운로드 완료")
        else:
            # yfinance 사용 (KRX 코드)
            df = yf.download('069500.KS', start=start_date, end=end_date, progress=False)
            print(f"✅ yfinance로 KODEX200 데이터 다운로드 완료")

        # 데이터 확인
        print(f"   기간: {df.index[0].strftime('%Y-%m-%d')} ~ {df.index[-1].strftime('%Y-%m-%d')}")
        print(f"   데이터 개수: {len(df)}행")
        print(f"   컬럼: {list(df.columns)}")

        return df

    except Exception as e:
        print(f"❌ KODEX200 데이터 다운로드 실패: {e}")
        return None


def inspect_data(df, name):
    """
    데이터 기본 정보 출력

    Args:
        df: DataFrame
        name: 데이터 이름
    """
    print("\n" + "=" * 60)
    print(f"🔍 {name} 데이터 확인")
    print("=" * 60)

    # 기본 정보
    print("\n1️⃣ 기본 정보:")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    print(f"   Index: {df.index.name if df.index.name else 'Date (index)'}")

    # 결측치
    print("\n2️⃣ 결측치:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("   ✅ 결측치 없음")

    # 기본 통계
    print("\n3️⃣ 기본 통계:")
    print(df.describe())

    # 최근 5일 데이터
    print("\n4️⃣ 최근 5일 데이터:")
    print(df.tail())


def save_data(df, filename):
    """
    데이터를 CSV 파일로 저장

    Args:
        df: DataFrame
        filename: 파일명
    """
    try:
        filepath = f'data/raw/{filename}'
        df.to_csv(filepath)
        print(f"✅ 데이터 저장 완료: {filepath}")

        # 파일 크기 확인
        import os
        size = os.path.getsize(filepath) / 1024  # KB
        print(f"   파일 크기: {size:.2f} KB")

        return True

    except Exception as e:
        print(f"❌ 데이터 저장 실패: {e}")
        return False


def create_summary_report(kospi_df, kodex_df):
    """
    데이터 요약 리포트 생성

    Args:
        kospi_df: KOSPI DataFrame
        kodex_df: KODEX200 DataFrame
    """
    print("\n" + "=" * 60)
    print("📋 데이터 수집 요약 리포트")
    print("=" * 60)

    report = []
    report.append("\n# Simple Kospi - 데이터 수집 리포트\n")
    report.append(f"**생성 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    # KOSPI 요약
    report.append("## 1. KOSPI 지수 데이터\n")
    report.append(f"- **기간**: {kospi_df.index[0].strftime('%Y-%m-%d')} ~ {kospi_df.index[-1].strftime('%Y-%m-%d')}\n")
    report.append(f"- **데이터 개수**: {len(kospi_df)}행\n")
    report.append(f"- **결측치**: {kospi_df.isnull().sum().sum()}개\n")
    report.append(f"- **종가 범위**: {kospi_df['Close'].min():.2f} ~ {kospi_df['Close'].max():.2f}\n")
    report.append(f"- **평균 거래량**: {kospi_df['Volume'].mean():,.0f}\n\n")

    # KODEX200 요약
    report.append("## 2. KODEX200 ETF 데이터\n")
    report.append(f"- **기간**: {kodex_df.index[0].strftime('%Y-%m-%d')} ~ {kodex_df.index[-1].strftime('%Y-%m-%d')}\n")
    report.append(f"- **데이터 개수**: {len(kodex_df)}행\n")
    report.append(f"- **결측치**: {kodex_df.isnull().sum().sum()}개\n")
    report.append(f"- **종가 범위**: {kodex_df['Close'].min():.2f} ~ {kodex_df['Close'].max():.2f}\n")
    report.append(f"- **평균 거래량**: {kodex_df['Volume'].mean():,.0f}\n\n")

    # 데이터 품질
    report.append("## 3. 데이터 품질 체크\n")

    # 날짜 일치 확인
    common_dates = len(set(kospi_df.index) & set(kodex_df.index))
    report.append(f"- **공통 거래일**: {common_dates}일\n")

    # 기간 일치 확인
    kospi_days = len(kospi_df)
    kodex_days = len(kodex_df)
    if kospi_days == kodex_days:
        report.append(f"- **기간 일치**: ✅ 두 데이터 모두 {kospi_days}일\n")
    else:
        report.append(f"- **기간 불일치**: ⚠️ KOSPI {kospi_days}일, KODEX {kodex_days}일\n")

    report.append("\n## 4. 다음 단계\n")
    report.append("- [ ] 데이터 전처리 (결측치 처리, Feature Engineering)\n")
    report.append("- [ ] Train/Test 분할\n")
    report.append("- [ ] 모델 학습\n")
    report.append("- [ ] 결과 평가\n")

    # 콘솔 출력
    report_text = ''.join(report)
    print(report_text)

    # 파일 저장
    try:
        with open('data/raw/data_collection_report.md', 'w', encoding='utf-8') as f:
            f.write(report_text)
        print("✅ 리포트 저장: data/raw/data_collection_report.md")
    except Exception as e:
        print(f"⚠️  리포트 저장 실패: {e}")


def main():
    """메인 실행 함수"""
    print("\n" + "🚀" * 30)
    print("Simple Kospi 프로젝트 - Stage 1: 데이터 수집")
    print("🚀" * 30)

    # 1. KOSPI 데이터 다운로드
    kospi_df = download_kospi_data()
    if kospi_df is None:
        print("❌ KOSPI 데이터 다운로드 실패. 프로그램 종료.")
        return

    # 2. KODEX200 데이터 다운로드
    kodex_df = download_kodex200_data()
    if kodex_df is None:
        print("❌ KODEX200 데이터 다운로드 실패. 프로그램 종료.")
        return

    # 3. 데이터 확인
    inspect_data(kospi_df, "KOSPI")
    inspect_data(kodex_df, "KODEX200")

    # 4. 데이터 저장
    print("\n" + "=" * 60)
    print("💾 데이터 저장")
    print("=" * 60)

    save_data(kospi_df, 'kospi_raw.csv')
    save_data(kodex_df, 'kodex200_raw.csv')

    # 5. 요약 리포트
    create_summary_report(kospi_df, kodex_df)

    print("\n" + "=" * 60)
    print("✅ Stage 1: 데이터 수집 완료!")
    print("=" * 60)
    print("\n다음 단계:")
    print("  python 02_data_preprocessing.py")


if __name__ == "__main__":
    main()
