"""
성능 개선 로드맵 시각화

현재 성능과 예상 개선 효과를 시각화합니다.
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 1. 난이도별 개선 전략 비교
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1-1. 개선 방법별 예상 성능
strategies = [
    '현재\n(Baseline)',
    'Level 1\n특징선택+앙상블',
    'Level 2\n특징엔지니어링',
    'Level 3\n외부데이터',
    'Level 4\nLSTM/Attention',
    'Level 5\n강화학습'
]

min_acc = [49.79, 50, 51, 52, 52, 53]
max_acc = [49.79, 54, 55, 58, 60, 65]
avg_acc = [(mi + ma) / 2 for mi, ma in zip(min_acc, max_acc)]

difficulty = [1, 2, 3, 4, 5, 6]
colors = ['red', 'orange', 'yellow', 'lightgreen', 'green', 'blue']

# 에러바 준비 (2xN 형식)
xerr_lower = [a - mi for a, mi in zip(avg_acc, min_acc)]
xerr_upper = [ma - a for ma, a in zip(max_acc, avg_acc)]

axes[0, 0].barh(strategies, avg_acc, xerr=[xerr_lower, xerr_upper],
                color=colors, alpha=0.7, capsize=5)
axes[0, 0].axvline(x=50, color='black', linestyle='--', linewidth=2, label='Random Baseline (50%)')
axes[0, 0].axvline(x=53, color='green', linestyle='--', linewidth=2, label='실전 기준 (53%)')
axes[0, 0].set_xlabel('예상 정확도 (%)', fontsize=12)
axes[0, 0].set_title('개선 전략별 예상 성능', fontsize=14, fontweight='bold')
axes[0, 0].legend(fontsize=10)
axes[0, 0].grid(True, alpha=0.3, axis='x')
axes[0, 0].set_xlim([45, 70])

# 숫자 표시
for i, (s, avg, mi, ma) in enumerate(zip(strategies, avg_acc, min_acc, max_acc)):
    axes[0, 0].text(avg + 1, i, f'{avg:.1f}%\n({mi:.0f}-{ma:.0f}%)',
                    va='center', fontsize=9, fontweight='bold')

# 1-2. 난이도 vs 효과 산점도
effort_hours = [0, 10, 40, 80, 120, 200]  # 예상 작업 시간 (시간)
improvement = [0, 2.5, 3.5, 5.5, 7.5, 12.5]  # 평균 개선폭 (%)

axes[0, 1].scatter(effort_hours, improvement, s=[100*d for d in difficulty],
                   c=colors, alpha=0.6, edgecolors='black', linewidth=2)

for i, (x, y, s) in enumerate(zip(effort_hours, improvement, strategies)):
    axes[0, 1].annotate(s.replace('\n', ' '), (x, y),
                       xytext=(10, 10), textcoords='offset points',
                       fontsize=9, bbox=dict(boxstyle='round,pad=0.5', facecolor=colors[i], alpha=0.3))

axes[0, 1].set_xlabel('예상 작업 시간 (시간)', fontsize=12)
axes[0, 1].set_ylabel('평균 개선폭 (%p)', fontsize=12)
axes[0, 1].set_title('노력 대비 효과', fontsize=14, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3)

# ROI 라인 (Return on Investment)
axes[0, 1].plot([0, 200], [0, 200/20], 'r--', alpha=0.5, label='ROI 1.0')
axes[0, 1].legend(fontsize=10)

# 1-3. 단계별 구현 우선순위
phases = {
    'Phase 1\n(1주)': ['앙상블', '특징선택', '임계값조정', '요일특징'],
    'Phase 2\n(2주)': ['기술지표', '시차특징', 'XGBoost'],
    'Phase 3\n(3-4주)': ['글로벌시장', '환율/금리', '뉴스감성'],
    'Phase 4\n(4-6주)': ['LSTM', 'Attention']
}

phase_colors = ['#FFE5E5', '#FFFFE5', '#E5FFE5', '#E5E5FF']
y_pos = 0

for phase, items in phases.items():
    height = len(items) * 0.2
    axes[1, 0].barh(y_pos, 1, height=height, color=phase_colors[y_pos % 4], alpha=0.7, edgecolor='black')
    axes[1, 0].text(0.5, y_pos, phase, ha='center', va='center',
                    fontsize=11, fontweight='bold')

    for i, item in enumerate(items):
        axes[1, 0].text(1.05, y_pos - height/2 + (i+0.5) * height/len(items),
                       f'• {item}', va='center', fontsize=9)

    y_pos += 1

axes[1, 0].set_xlim([0, 2.5])
axes[1, 0].set_ylim([-0.5, y_pos - 0.5])
axes[1, 0].axis('off')
axes[1, 0].set_title('실전 구현 로드맵', fontsize=14, fontweight='bold')

# 1-4. 현재 문제 진단
problems = {
    '특징 중요도 낮음': 0.85,
    '다중공선성': 0.70,
    '데이터 부족': 0.60,
    '외부 요인 미반영': 0.90,
    '시계열 패턴 미학습': 0.75
}

solutions = {
    '특징 중요도 낮음': '외부 데이터 추가',
    '다중공선성': '특징 선택/PCA',
    '데이터 부족': 'GAN/증강',
    '외부 요인 미반영': '글로벌 시장 데이터',
    '시계열 패턴 미학습': 'LSTM/Attention'
}

problem_names = list(problems.keys())
severity = list(problems.values())

bars = axes[1, 1].barh(problem_names, severity, color=['red', 'orange', 'yellow', 'red', 'orange'], alpha=0.7)

# 해결책 표시
for i, (prob, sol) in enumerate(solutions.items()):
    axes[1, 1].text(severity[i] + 0.05, i, f'→ {sol}',
                   va='center', fontsize=9, style='italic')

axes[1, 1].set_xlabel('심각도', fontsize=12)
axes[1, 1].set_title('현재 문제 진단 및 해결책', fontsize=14, fontweight='bold')
axes[1, 1].set_xlim([0, 1.2])
axes[1, 1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('../assets/improvement_roadmap.png', dpi=150, bbox_inches='tight')
print("✅ 개선 로드맵 시각화 저장: ../assets/improvement_roadmap.png")
plt.close()


# 2. 특징 중요도 vs 상관관계 산점도
fig, ax = plt.subplots(figsize=(12, 8))

# 실제 데이터 (analysis_report.md 기반)
features = [
    'kospi_ma60', 'kospi_range_pct', 'kospi_return', 'kospi_ma5', 'kospi_volume_ma5',
    'kospi_kodex_ratio', 'kodex_return', 'kospi_high', 'kospi_volume_ratio', 'kospi_range',
    'kospi_rsi', 'kospi_ma20', 'kospi_low'
]

mutual_info = [0.0269, 0.0220, 0.0198, 0.0171, 0.0126, 0.012, 0.011, 0.010, 0.009, 0.008, 0.007, 0.006, 0.005]
correlation = [0.0715, 0.03, 0.05, 0.0643, 0.02, 0.04, 0.03, 0.0629, 0.01, 0.02, 0.0758, 0.0725, 0.0629]

colors_scatter = plt.cm.viridis(np.linspace(0, 1, len(features)))

ax.scatter(mutual_info, correlation, s=200, c=colors_scatter, alpha=0.6, edgecolors='black', linewidth=2)

for i, feature in enumerate(features):
    ax.annotate(feature.replace('kospi_', '').replace('kodex_', 'kdx_'),
               (mutual_info[i], correlation[i]),
               xytext=(5, 5), textcoords='offset points',
               fontsize=8, alpha=0.8)

ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)

ax.set_xlabel('Mutual Information (특징 중요도)', fontsize=12)
ax.set_ylabel('Correlation with Target (상관관계)', fontsize=12)
ax.set_title('특징 분석: 중요도 vs 상관관계\n(낮은 값 = 예측 어려움)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)

# 기준선 표시
ax.axhline(y=0.3, color='green', linestyle='--', alpha=0.3, label='강한 상관관계 (0.3)')
ax.axvline(x=0.1, color='green', linestyle='--', alpha=0.3, label='높은 중요도 (0.1)')
ax.legend(fontsize=10)

# 문제 영역 표시
ax.fill_between([0, 0.1], 0, 0.3, color='red', alpha=0.1, label='문제 영역 (낮음)')

plt.tight_layout()
plt.savefig('../assets/feature_analysis_scatter.png', dpi=150, bbox_inches='tight')
print("✅ 특징 분석 산점도 저장: ../assets/feature_analysis_scatter.png")
plt.close()


# 3. 개선 시나리오별 예상 누적 성과
fig, ax = plt.subplots(figsize=(14, 8))

weeks = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])

# 시나리오별 성능 추이
baseline = np.array([49.79] * len(weeks))

scenario_conservative = np.array([49.79, 50.5, 51.2, 51.8, 52.3, 52.7, 53.0, 53.2, 53.5])
scenario_moderate = np.array([49.79, 51.0, 52.5, 53.5, 54.2, 55.0, 55.5, 56.0, 56.5])
scenario_optimistic = np.array([49.79, 52.0, 54.0, 55.5, 57.0, 58.5, 60.0, 61.0, 62.0])

ax.plot(weeks, baseline, 'k--', linewidth=2, label='현재 성능 (49.79%)', alpha=0.5)
ax.plot(weeks, scenario_conservative, 'o-', linewidth=3, label='보수적 (앙상블만)', color='orange', markersize=8)
ax.plot(weeks, scenario_moderate, 's-', linewidth=3, label='중간 (특징+모델)', color='green', markersize=8)
ax.plot(weeks, scenario_optimistic, '^-', linewidth=3, label='공격적 (외부데이터+LSTM)', color='blue', markersize=8)

# 기준선
ax.axhline(y=50, color='red', linestyle='--', linewidth=2, alpha=0.3, label='Random Baseline (50%)')
ax.axhline(y=53, color='green', linestyle='--', linewidth=2, alpha=0.3, label='실전 기준 (53%)')

# 영역 표시
ax.fill_between(weeks, 50, 53, color='yellow', alpha=0.1, label='개선 필요 영역')
ax.fill_between(weeks, 53, 70, color='green', alpha=0.1, label='실전 가능 영역')

ax.set_xlabel('기간 (주)', fontsize=12)
ax.set_ylabel('예상 정확도 (%)', fontsize=12)
ax.set_title('개선 시나리오별 예상 성과 추이', fontsize=14, fontweight='bold')
ax.legend(fontsize=11, loc='lower right')
ax.grid(True, alpha=0.3)
ax.set_ylim([48, 65])

# 주요 마일스톤 표시
milestones = [
    (1, 'Phase 1\n앙상블'),
    (3, 'Phase 2\n특징 강화'),
    (5, 'Phase 3\n외부 데이터'),
    (7, 'Phase 4\nLSTM')
]

for week, text in milestones:
    ax.annotate(text, xy=(week, 48.5), xytext=(week, 47),
               arrowprops=dict(arrowstyle='->', color='gray', alpha=0.5),
               fontsize=9, ha='center', bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

plt.tight_layout()
plt.savefig('../assets/improvement_scenarios.png', dpi=150, bbox_inches='tight')
print("✅ 개선 시나리오 추이 저장: ../assets/improvement_scenarios.png")
plt.close()

print("\n" + "="*60)
print("✅ 성능 개선 로드맵 시각화 완료!")
print("="*60)
print("\n생성된 파일:")
print("  1. improvement_roadmap.png - 전체 개선 전략 개요")
print("  2. feature_analysis_scatter.png - 특징 중요도 분석")
print("  3. improvement_scenarios.png - 시나리오별 예상 성과")
print("\n다음 단계:")
print("  - 성능_개선_방안.md 문서 읽기")
print("  - Phase 1 (앙상블 + 특징선택) 구현 권장")
