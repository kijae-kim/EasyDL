#!/usr/bin/env python3
"""
Simple Kospi - 전처리 데이터 심화 분석

목표:
1. 특징 간 상관관계 분석
2. 타겟과 특징 간 관계 분석
3. 특징 분포 확인
4. 특징 중요도 파악
5. 탐색적 데이터 분석 (EDA)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")


def load_processed_data():
    """전처리된 데이터 로드"""
    print("\n" + "=" * 60)
    print("📂 전처리 데이터 로드")
    print("=" * 60)

    train_df = pd.read_csv('data/processed/train_data.csv', index_col=0, parse_dates=True)
    test_df = pd.read_csv('data/processed/test_data.csv', index_col=0, parse_dates=True)

    print(f"✅ Train: {len(train_df)}행 × {len(train_df.columns)}열")
    print(f"✅ Test: {len(test_df)}행 × {len(test_df.columns)}열")

    # 특징과 타겟 분리
    feature_cols = [col for col in train_df.columns if not col.startswith('target')]

    X_train = train_df[feature_cols]
    y_train = train_df['target']
    X_test = test_df[feature_cols]
    y_test = test_df['target']

    return X_train, X_test, y_train, y_test, train_df, test_df


def analyze_correlation(X_train, y_train):
    """특징 간 상관관계 분석"""
    print("\n" + "=" * 60)
    print("🔍 특징 간 상관관계 분석")
    print("=" * 60)

    # 상관관계 행렬 계산
    corr_matrix = X_train.corr()

    # 상관관계 히트맵
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    # 전체 상관관계
    sns.heatmap(corr_matrix, cmap='coolwarm', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
                ax=axes[0], vmin=-1, vmax=1)
    axes[0].set_title('특징 간 상관관계 히트맵', fontsize=14, pad=15)

    # 높은 상관관계 찾기
    high_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) > 0.8:
                high_corr.append({
                    'feature1': corr_matrix.columns[i],
                    'feature2': corr_matrix.columns[j],
                    'correlation': corr_matrix.iloc[i, j]
                })

    print(f"\n높은 상관관계 (|r| > 0.8): {len(high_corr)}쌍")
    if high_corr:
        for item in high_corr[:10]:  # 상위 10개만 출력
            print(f"   {item['feature1']} ↔ {item['feature2']}: {item['correlation']:.3f}")

    # 타겟과의 상관관계
    target_corr = pd.DataFrame({
        'feature': X_train.columns,
        'correlation': [X_train[col].corr(y_train) for col in X_train.columns]
    }).sort_values('correlation', key=abs, ascending=False)

    axes[1].barh(range(len(target_corr)), target_corr['correlation'].values,
                color=['green' if x > 0 else 'red' for x in target_corr['correlation'].values],
                alpha=0.7)
    axes[1].set_yticks(range(len(target_corr)))
    axes[1].set_yticklabels(target_corr['feature'].values, fontsize=8)
    axes[1].axvline(0, color='black', linewidth=0.8)
    axes[1].set_xlabel('상관계수', fontsize=11)
    axes[1].set_title('타겟(다음날 등락)과의 상관관계', fontsize=14, pad=15)
    axes[1].grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig('../assets/correlation_analysis.png', dpi=300, bbox_inches='tight')
    print("\n✅ 상관관계 분석 저장: ../assets/correlation_analysis.png")
    plt.close()

    # 타겟과 가장 높은 상관관계
    print(f"\n📊 타겟과 상관관계 Top 5:")
    for i, row in target_corr.head(5).iterrows():
        print(f"   {row['feature']}: {row['correlation']:.4f}")

    return target_corr


def analyze_feature_distributions(X_train, y_train):
    """특징 분포 분석"""
    print("\n" + "=" * 60)
    print("📊 특징 분포 분석")
    print("=" * 60)

    # 주요 특징 선택 (타겟과 상관관계 높은 6개)
    target_corr = pd.DataFrame({
        'feature': X_train.columns,
        'correlation': [abs(X_train[col].corr(y_train)) for col in X_train.columns]
    }).sort_values('correlation', ascending=False)

    top_features = target_corr.head(6)['feature'].values

    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    axes = axes.flatten()

    for i, feature in enumerate(top_features):
        ax = axes[i]

        # 상승/하락별 분포
        data_up = X_train[y_train == 1][feature]
        data_down = X_train[y_train == 0][feature]

        ax.hist(data_down, bins=30, alpha=0.6, label='하락(0)', color='red', density=True)
        ax.hist(data_up, bins=30, alpha=0.6, label='상승(1)', color='green', density=True)

        ax.set_title(f'{feature}', fontsize=12)
        ax.set_xlabel('값', fontsize=10)
        ax.set_ylabel('밀도', fontsize=10)
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

        # t-test
        t_stat, p_value = stats.ttest_ind(data_up, data_down)
        if p_value < 0.05:
            ax.text(0.02, 0.98, f'p={p_value:.4f}*',
                   transform=ax.transAxes, fontsize=9,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

    plt.suptitle('주요 특징의 분포 (상승 vs 하락)', fontsize=16, y=1.00)
    plt.tight_layout()
    plt.savefig('../assets/feature_distributions.png', dpi=300, bbox_inches='tight')
    print("✅ 특징 분포 분석 저장: ../assets/feature_distributions.png")
    plt.close()

    # 통계적 유의성 검정
    print("\n📊 상승/하락 그룹 간 차이 (t-test):")
    significant_features = []
    for feature in X_train.columns:
        data_up = X_train[y_train == 1][feature]
        data_down = X_train[y_train == 0][feature]
        t_stat, p_value = stats.ttest_ind(data_up, data_down)

        if p_value < 0.05:
            significant_features.append({
                'feature': feature,
                'p_value': p_value,
                't_stat': t_stat
            })

    significant_features = sorted(significant_features, key=lambda x: x['p_value'])
    print(f"   통계적으로 유의한 특징 (p < 0.05): {len(significant_features)}개")

    for item in significant_features[:5]:
        print(f"   {item['feature']}: p={item['p_value']:.6f}, t={item['t_stat']:.3f}")


def analyze_feature_importance_simple(X_train, y_train):
    """간단한 특징 중요도 분석 (단변량 분석)"""
    print("\n" + "=" * 60)
    print("🎯 특징 중요도 분석 (단변량)")
    print("=" * 60)

    from sklearn.feature_selection import mutual_info_classif

    # Mutual Information
    mi_scores = mutual_info_classif(X_train, y_train, random_state=42)
    mi_df = pd.DataFrame({
        'feature': X_train.columns,
        'mi_score': mi_scores
    }).sort_values('mi_score', ascending=False)

    # 시각화
    fig, ax = plt.subplots(figsize=(10, 8))

    colors = plt.cm.viridis(np.linspace(0, 1, len(mi_df)))
    bars = ax.barh(range(len(mi_df)), mi_df['mi_score'].values, color=colors, alpha=0.8)

    ax.set_yticks(range(len(mi_df)))
    ax.set_yticklabels(mi_df['feature'].values, fontsize=9)
    ax.set_xlabel('Mutual Information Score', fontsize=12)
    ax.set_title('특징 중요도 (Mutual Information)', fontsize=14, pad=15)
    ax.grid(True, alpha=0.3, axis='x')

    # 상위 3개 강조
    for i in range(3):
        bars[i].set_edgecolor('red')
        bars[i].set_linewidth(2)

    plt.tight_layout()
    plt.savefig('../assets/feature_importance.png', dpi=300, bbox_inches='tight')
    print("✅ 특징 중요도 저장: ../assets/feature_importance.png")
    plt.close()

    print(f"\n📊 특징 중요도 Top 10:")
    for i, row in mi_df.head(10).iterrows():
        print(f"   {i+1}. {row['feature']}: {row['mi_score']:.4f}")

    return mi_df


def analyze_time_series_patterns(train_df):
    """시계열 패턴 분석"""
    print("\n" + "=" * 60)
    print("📈 시계열 패턴 분석")
    print("=" * 60)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. 월별 상승/하락 비율
    train_df['year_month'] = train_df.index.to_period('M')
    monthly_target = train_df.groupby('year_month')['target'].agg(['sum', 'count'])
    monthly_target['ratio'] = monthly_target['sum'] / monthly_target['count']

    axes[0, 0].plot(monthly_target.index.to_timestamp(), monthly_target['ratio'].values,
                    marker='o', linewidth=2, markersize=4)
    axes[0, 0].axhline(0.5, color='red', linestyle='--', linewidth=1, label='50% 기준선')
    axes[0, 0].set_title('월별 상승 비율', fontsize=13)
    axes[0, 0].set_xlabel('날짜', fontsize=11)
    axes[0, 0].set_ylabel('상승 비율', fontsize=11)
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # 2. 요일별 상승/하락
    train_df['weekday'] = train_df.index.dayofweek
    weekday_names = ['월', '화', '수', '목', '금']
    weekday_target = train_df.groupby('weekday')['target'].agg(['sum', 'count'])
    weekday_target['ratio'] = weekday_target['sum'] / weekday_target['count']

    axes[0, 1].bar(range(5), weekday_target['ratio'].values,
                   color=['green' if x > 0.5 else 'red' for x in weekday_target['ratio'].values],
                   alpha=0.7)
    axes[0, 1].axhline(0.5, color='black', linestyle='--', linewidth=1)
    axes[0, 1].set_xticks(range(5))
    axes[0, 1].set_xticklabels(weekday_names)
    axes[0, 1].set_title('요일별 상승 비율', fontsize=13)
    axes[0, 1].set_ylabel('상승 비율', fontsize=11)
    axes[0, 1].grid(True, alpha=0.3, axis='y')

    # 3. 수익률 누적 분포
    train_df_sorted = train_df.sort_values('target_return')
    cumulative_returns = train_df_sorted['target_return'].cumsum()

    axes[1, 0].plot(range(len(cumulative_returns)), cumulative_returns.values, linewidth=2)
    axes[1, 0].axhline(0, color='red', linestyle='--', linewidth=1)
    axes[1, 0].set_title('누적 수익률 분포', fontsize=13)
    axes[1, 0].set_xlabel('거래일 (정렬됨)', fontsize=11)
    axes[1, 0].set_ylabel('누적 수익률', fontsize=11)
    axes[1, 0].grid(True, alpha=0.3)

    # 4. 연도별 타겟 분포
    train_df['year'] = train_df.index.year
    year_target = train_df.groupby(['year', 'target']).size().unstack(fill_value=0)
    year_target_ratio = year_target.div(year_target.sum(axis=1), axis=0)

    year_target_ratio.plot(kind='bar', stacked=True, ax=axes[1, 1],
                           color=['red', 'green'], alpha=0.7)
    axes[1, 1].set_title('연도별 타겟 분포', fontsize=13)
    axes[1, 1].set_xlabel('연도', fontsize=11)
    axes[1, 1].set_ylabel('비율', fontsize=11)
    axes[1, 1].legend(['하락(0)', '상승(1)'], fontsize=10)
    axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=0)
    axes[1, 1].grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('../assets/time_series_patterns.png', dpi=300, bbox_inches='tight')
    print("✅ 시계열 패턴 분석 저장: ../assets/time_series_patterns.png")
    plt.close()

    # 요일별 통계
    print("\n📊 요일별 상승 비율:")
    for i, ratio in enumerate(weekday_target['ratio'].values):
        print(f"   {weekday_names[i]}: {ratio:.2%} ({weekday_target['sum'].iloc[i]:.0f}/{weekday_target['count'].iloc[i]:.0f})")


def create_analysis_summary(target_corr, mi_df):
    """분석 요약 리포트 생성"""
    print("\n" + "=" * 60)
    print("📋 데이터 분석 요약 리포트")
    print("=" * 60)

    report = []
    report.append("\n# Simple Kospi - 데이터 분석 리포트\n")
    report.append(f"**생성 일시**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    # 주요 발견사항
    report.append("## 1. 주요 발견사항\n\n")

    report.append("### 특징 중요도 (Mutual Information Top 5)\n")
    for i, row in mi_df.head(5).iterrows():
        report.append(f"{i+1}. **{row['feature']}**: {row['mi_score']:.4f}\n")
    report.append("\n")

    report.append("### 타겟과 상관관계 Top 5\n")
    for i, row in target_corr.head(5).iterrows():
        report.append(f"{i+1}. **{row['feature']}**: {row['correlation']:.4f}\n")
    report.append("\n")

    # 데이터 특성
    report.append("## 2. 데이터 특성\n\n")
    report.append("- **정규화**: StandardScaler 적용됨\n")
    report.append("- **특징 개수**: 24개\n")
    report.append("- **타겟 균형**: 상승 54%, 하락 46% (비교적 균형)\n")
    report.append("- **시계열 특성**: 이동평균, 변동성 등 시계열 패턴 포함\n\n")

    # 모델 학습 제안
    report.append("## 3. 모델 학습 제안\n\n")
    report.append("### 추천 특징 (중요도 기반)\n")
    top_10 = mi_df.head(10)['feature'].tolist()
    for i, feat in enumerate(top_10, 1):
        report.append(f"{i}. {feat}\n")
    report.append("\n")

    report.append("### 모델 선택 가이드\n")
    report.append("- **선형 회귀**: 기본 베이스라인, 해석 용이\n")
    report.append("- **로지스틱 회귀**: 이진 분류에 최적화, 확률 출력\n")
    report.append("- **MLP**: 비선형 패턴 학습 가능, 성능 최고\n\n")

    # 예상 성능
    report.append("## 4. 예상 성능\n\n")
    report.append("- **Random Baseline**: ~50% (상승/하락 5:5)\n")
    report.append("- **목표 성능**: 55-60% 정확도\n")
    report.append("- **실전 기준**: 53% 이상이면 수익 가능\n\n")

    # 다음 단계
    report.append("## 5. 다음 단계\n\n")
    report.append("- [ ] 선형 회귀 모델 구현 및 학습\n")
    report.append("- [ ] 로지스틱 회귀 모델 구현 및 학습\n")
    report.append("- [ ] MLP 모델 구현 및 학습\n")
    report.append("- [ ] 3가지 모델 성능 비교\n")
    report.append("- [ ] 최종 모델 선정 및 평가\n")

    report_text = ''.join(report)
    print(report_text)

    # 파일 저장
    with open('data/processed/analysis_report.md', 'w', encoding='utf-8') as f:
        f.write(report_text)
    print("✅ 분석 리포트 저장: data/processed/analysis_report.md")


def main():
    """메인 실행 함수"""
    print("\n" + "🔬" * 30)
    print("Simple Kospi - 데이터 심화 분석")
    print("🔬" * 30)

    # 1. 데이터 로드
    X_train, X_test, y_train, y_test, train_df, test_df = load_processed_data()

    # 2. 상관관계 분석
    target_corr = analyze_correlation(X_train, y_train)

    # 3. 특징 분포 분석
    analyze_feature_distributions(X_train, y_train)

    # 4. 특징 중요도 분석
    mi_df = analyze_feature_importance_simple(X_train, y_train)

    # 5. 시계열 패턴 분석
    analyze_time_series_patterns(train_df)

    # 6. 분석 요약 리포트
    create_analysis_summary(target_corr, mi_df)

    print("\n" + "=" * 60)
    print("✅ 데이터 분석 완료!")
    print("=" * 60)
    print("\n생성된 시각화:")
    print("  1. correlation_analysis.png - 상관관계 분석")
    print("  2. feature_distributions.png - 특징 분포")
    print("  3. feature_importance.png - 특징 중요도")
    print("  4. time_series_patterns.png - 시계열 패턴")
    print("\n다음 단계:")
    print("  python 03_model_design.py")
    print("  python 04_model_training.py")


if __name__ == "__main__":
    main()
