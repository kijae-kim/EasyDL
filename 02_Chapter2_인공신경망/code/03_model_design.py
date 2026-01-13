#!/usr/bin/env python3
"""
Simple Kospi 프로젝트 - Stage 3: 모델 설계

목표:
1. 선형 회귀 (Linear Regression) - Chapter 2 기본 개념
2. 로지스틱 회귀 (Logistic Regression) - 이진 분류
3. MLP (Multi-Layer Perceptron) - 신경망

각 모델의 구조 정의 및 하이퍼파라미터 설정
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import tensorflow as tf
from tensorflow import keras
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False


def load_data():
    """전처리된 데이터 로드"""
    print("\n" + "=" * 60)
    print("📂 데이터 로드")
    print("=" * 60)

    train_df = pd.read_csv('data/processed/train_data.csv', index_col=0, parse_dates=True)
    test_df = pd.read_csv('data/processed/test_data.csv', index_col=0, parse_dates=True)

    # 특징과 타겟 분리
    feature_cols = [col for col in train_df.columns if not col.startswith('target')]

    X_train = train_df[feature_cols].values
    y_train = train_df['target'].values
    y_train_reg = train_df['target_return'].values

    X_test = test_df[feature_cols].values
    y_test = test_df['target'].values
    y_test_reg = test_df['target_return'].values

    print(f"✅ Train: X={X_train.shape}, y={y_train.shape}")
    print(f"✅ Test:  X={X_test.shape}, y={y_test.shape}")
    print(f"   특징 개수: {X_train.shape[1]}개")

    return X_train, X_test, y_train, y_test, y_train_reg, y_test_reg, feature_cols


def design_linear_regression():
    """
    모델 1: 선형 회귀 (Linear Regression)

    Chapter 2 기본 개념:
    - y = wx + b (다변량: y = w1*x1 + w2*x2 + ... + b)
    - Loss: MSE (Mean Squared Error)
    - 목표: 다음날 수익률(target_return) 예측
    """
    print("\n" + "=" * 60)
    print("📐 모델 1: 선형 회귀 (Linear Regression)")
    print("=" * 60)

    print("\n🎯 목표:")
    print("   - Chapter 2의 기본 개념 적용")
    print("   - y = w·x + b 형태의 선형 함수 학습")
    print("   - 다음날 수익률(연속값) 예측")

    print("\n📊 모델 구조:")
    print("   입력: 24개 특징")
    print("   출력: 1개 (다음날 수익률)")
    print("   파라미터: 가중치(w) 24개 + 바이어스(b) 1개 = 25개")

    print("\n🔧 하이퍼파라미터:")
    print("   - fit_intercept: True (바이어스 사용)")
    print("   - normalize: False (이미 정규화됨)")

    print("\n📉 손실 함수:")
    print("   - MSE = (1/n) * Σ(y_true - y_pred)²")

    print("\n💡 예상:")
    print("   - 장점: 간단, 해석 용이, 빠른 학습")
    print("   - 단점: 선형 관계만 학습, 복잡한 패턴 못 잡음")
    print("   - 용도: 베이스라인, 선형 관계 파악")

    # 모델 생성
    model = LinearRegression(fit_intercept=True)

    print("\n✅ 선형 회귀 모델 설계 완료")

    return model


def design_logistic_regression():
    """
    모델 2: 로지스틱 회귀 (Logistic Regression)

    이진 분류:
    - Sigmoid 함수: σ(z) = 1 / (1 + e^(-z))
    - z = w·x + b
    - Loss: Binary Cross-Entropy
    - 목표: 다음날 등락(0 or 1) 예측
    """
    print("\n" + "=" * 60)
    print("📐 모델 2: 로지스틱 회귀 (Logistic Regression)")
    print("=" * 60)

    print("\n🎯 목표:")
    print("   - 이진 분류 문제에 최적화")
    print("   - 다음날 상승(1) or 하락(0) 예측")
    print("   - 확률로 해석 가능 (0~1 사이 값)")

    print("\n📊 모델 구조:")
    print("   입력: 24개 특징")
    print("   선형 변환: z = w·x + b")
    print("   활성화 함수: σ(z) = 1/(1+e^(-z))")
    print("   출력: 1개 (상승 확률)")
    print("   파라미터: 25개 (선형회귀와 동일)")

    print("\n🔧 하이퍼파라미터:")
    print("   - penalty: 'l2' (L2 정규화)")
    print("   - C: 1.0 (정규화 강도)")
    print("   - solver: 'lbfgs' (최적화 알고리즘)")
    print("   - max_iter: 1000 (최대 반복 횟수)")
    print("   - random_state: 42")

    print("\n📉 손실 함수:")
    print("   - Binary Cross-Entropy")
    print("   - BCE = -[y*log(p) + (1-y)*log(1-p)]")

    print("\n💡 예상:")
    print("   - 장점: 확률 출력, 분류에 최적화")
    print("   - 단점: 여전히 선형 결정 경계")
    print("   - 용도: 기본 분류 모델, 확률 해석")

    # 모델 생성
    model = LogisticRegression(
        penalty='l2',
        C=1.0,
        solver='lbfgs',
        max_iter=1000,
        random_state=42
    )

    print("\n✅ 로지스틱 회귀 모델 설계 완료")

    return model


def design_mlp_model(input_dim):
    """
    모델 3: MLP (Multi-Layer Perceptron)

    신경망:
    - Input Layer → Hidden Layer 1 → Hidden Layer 2 → Output Layer
    - 활성화 함수: ReLU (은닉층), Sigmoid (출력층)
    - Loss: Binary Cross-Entropy
    - Optimizer: Adam
    """
    print("\n" + "=" * 60)
    print("📐 모델 3: MLP (Multi-Layer Perceptron)")
    print("=" * 60)

    print("\n🎯 목표:")
    print("   - 비선형 패턴 학습")
    print("   - 복잡한 특징 조합 학습")
    print("   - 최고 성능 추구")

    print("\n📊 모델 구조:")
    print(f"   Input Layer:    {input_dim}개 노드 (특징)")
    print(f"   Hidden Layer 1: 32개 노드 (ReLU)")
    print(f"   Dropout:        0.3 (과적합 방지)")
    print(f"   Hidden Layer 2: 16개 노드 (ReLU)")
    print(f"   Dropout:        0.3")
    print(f"   Output Layer:   1개 노드 (Sigmoid)")

    total_params = (input_dim * 32 + 32) + (32 * 16 + 16) + (16 * 1 + 1)
    print(f"\n   총 파라미터: {total_params:,}개")

    print("\n🔧 하이퍼파라미터:")
    print("   - 활성화 함수 (은닉층): ReLU")
    print("   - 활성화 함수 (출력층): Sigmoid")
    print("   - Dropout 비율: 0.3")
    print("   - Optimizer: Adam (lr=0.001)")
    print("   - Loss: Binary Cross-Entropy")
    print("   - Batch Size: 32")
    print("   - Epochs: 100")
    print("   - Validation Split: 0.2")

    print("\n📉 손실 함수:")
    print("   - Binary Cross-Entropy")
    print("   - Optimizer: Adam (adaptive learning rate)")

    print("\n💡 예상:")
    print("   - 장점: 비선형 학습, 높은 성능, 복잡한 패턴")
    print("   - 단점: 과적합 위험, 학습 시간, 해석 어려움")
    print("   - 용도: 최종 모델, 성능 최적화")

    # 모델 생성
    model = keras.Sequential([
        # Input Layer
        keras.layers.Input(shape=(input_dim,)),

        # Hidden Layer 1
        keras.layers.Dense(32, activation='relu', name='hidden1'),
        keras.layers.Dropout(0.3, name='dropout1'),

        # Hidden Layer 2
        keras.layers.Dense(16, activation='relu', name='hidden2'),
        keras.layers.Dropout(0.3, name='dropout2'),

        # Output Layer
        keras.layers.Dense(1, activation='sigmoid', name='output')
    ])

    # 컴파일
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
    )

    print("\n✅ MLP 모델 설계 완료")

    # 모델 요약
    print("\n📋 모델 요약:")
    model.summary()

    return model


def visualize_model_architectures(input_dim):
    """모델 아키텍처 시각화"""
    print("\n" + "=" * 60)
    print("🎨 모델 아키텍처 시각화")
    print("=" * 60)

    fig, axes = plt.subplots(1, 3, figsize=(16, 6))

    # 1. 선형 회귀
    ax1 = axes[0]
    ax1.text(0.5, 0.7, 'Input\n(24 features)', ha='center', va='center',
            fontsize=12, bbox=dict(boxstyle='round', facecolor='lightblue'))
    ax1.arrow(0.5, 0.6, 0, -0.15, head_width=0.05, head_length=0.05, fc='black')
    ax1.text(0.5, 0.35, 'Linear\nTransform\ny = wx + b', ha='center', va='center',
            fontsize=11, bbox=dict(boxstyle='round', facecolor='lightgreen'))
    ax1.arrow(0.5, 0.25, 0, -0.15, head_width=0.05, head_length=0.05, fc='black')
    ax1.text(0.5, 0.0, 'Output\n(수익률)', ha='center', va='center',
            fontsize=12, bbox=dict(boxstyle='round', facecolor='lightcoral'))
    ax1.set_xlim(0, 1)
    ax1.set_ylim(-0.1, 0.9)
    ax1.axis('off')
    ax1.set_title('선형 회귀\n(25개 파라미터)', fontsize=14, pad=20)

    # 2. 로지스틱 회귀
    ax2 = axes[1]
    ax2.text(0.5, 0.7, 'Input\n(24 features)', ha='center', va='center',
            fontsize=12, bbox=dict(boxstyle='round', facecolor='lightblue'))
    ax2.arrow(0.5, 0.6, 0, -0.08, head_width=0.05, head_length=0.05, fc='black')
    ax2.text(0.5, 0.45, 'z = wx + b', ha='center', va='center',
            fontsize=11, bbox=dict(boxstyle='round', facecolor='lightgreen'))
    ax2.arrow(0.5, 0.38, 0, -0.08, head_width=0.05, head_length=0.05, fc='black')
    ax2.text(0.5, 0.23, 'Sigmoid\nσ(z)', ha='center', va='center',
            fontsize=11, bbox=dict(boxstyle='round', facecolor='lightyellow'))
    ax2.arrow(0.5, 0.15, 0, -0.08, head_width=0.05, head_length=0.05, fc='black')
    ax2.text(0.5, 0.0, 'Output\n(확률 0~1)', ha='center', va='center',
            fontsize=12, bbox=dict(boxstyle='round', facecolor='lightcoral'))
    ax2.set_xlim(0, 1)
    ax2.set_ylim(-0.1, 0.9)
    ax2.axis('off')
    ax2.set_title('로지스틱 회귀\n(25개 파라미터)', fontsize=14, pad=20)

    # 3. MLP
    ax3 = axes[2]
    y_positions = [0.75, 0.55, 0.35, 0.15, -0.05]
    labels = ['Input\n(24)', 'Hidden 1\n(32)\nReLU', 'Dropout\n(0.3)',
             'Hidden 2\n(16)\nReLU', 'Output\n(1)\nSigmoid']
    colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightgreen', 'lightcoral']

    for i, (y, label, color) in enumerate(zip(y_positions, labels, colors)):
        ax3.text(0.5, y, label, ha='center', va='center',
                fontsize=10, bbox=dict(boxstyle='round', facecolor=color))
        if i < len(y_positions) - 1:
            ax3.arrow(0.5, y-0.05, 0, -0.10, head_width=0.05, head_length=0.03, fc='black')

    ax3.set_xlim(0, 1)
    ax3.set_ylim(-0.15, 0.9)
    ax3.axis('off')
    total_params = (input_dim * 32 + 32) + (32 * 16 + 16) + (16 * 1 + 1)
    ax3.set_title(f'MLP\n({total_params:,}개 파라미터)', fontsize=14, pad=20)

    plt.suptitle('Simple Kospi 모델 아키텍처 비교', fontsize=16, y=0.98)
    plt.tight_layout()
    plt.savefig('../assets/model_architectures.png', dpi=300, bbox_inches='tight')
    print("✅ 모델 아키텍처 시각화 저장: ../assets/model_architectures.png")
    plt.close()


def create_model_design_report(input_dim):
    """모델 설계 리포트 생성"""
    print("\n" + "=" * 60)
    print("📋 모델 설계 리포트")
    print("=" * 60)

    report = []
    report.append("\n# Simple Kospi - 모델 설계 리포트\n")
    report.append(f"**생성 일시**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    # 모델 개요
    report.append("## 1. 모델 개요\n\n")
    report.append("### 설계된 3가지 모델\n\n")

    report.append("#### 1) 선형 회귀 (Linear Regression)\n")
    report.append("- **목적**: Chapter 2 기본 개념 적용, 베이스라인\n")
    report.append("- **구조**: y = wx + b\n")
    report.append("- **파라미터**: 25개 (24 weights + 1 bias)\n")
    report.append("- **손실 함수**: MSE\n")
    report.append("- **예측 대상**: 다음날 수익률 (연속값)\n\n")

    report.append("#### 2) 로지스틱 회귀 (Logistic Regression)\n")
    report.append("- **목적**: 이진 분류 최적화\n")
    report.append("- **구조**: σ(wx + b), σ는 Sigmoid 함수\n")
    report.append("- **파라미터**: 25개\n")
    report.append("- **손실 함수**: Binary Cross-Entropy\n")
    report.append("- **예측 대상**: 다음날 등락 (0 or 1)\n\n")

    report.append("#### 3) MLP (Multi-Layer Perceptron)\n")
    report.append("- **목적**: 비선형 패턴 학습, 최고 성능\n")
    report.append(f"- **구조**: {input_dim} → 32(ReLU) → 16(ReLU) → 1(Sigmoid)\n")
    total_params = (input_dim * 32 + 32) + (32 * 16 + 16) + (16 * 1 + 1)
    report.append(f"- **파라미터**: {total_params:,}개\n")
    report.append("- **정규화**: Dropout (0.3)\n")
    report.append("- **손실 함수**: Binary Cross-Entropy\n")
    report.append("- **Optimizer**: Adam (lr=0.001)\n")
    report.append("- **예측 대상**: 다음날 등락 (0 or 1)\n\n")

    # 비교표
    report.append("## 2. 모델 비교\n\n")
    report.append("| 항목 | 선형 회귀 | 로지스틱 회귀 | MLP |\n")
    report.append("|------|-----------|---------------|-----|\n")
    report.append("| 파라미터 수 | 25 | 25 | " + f"{total_params:,}" + " |\n")
    report.append("| 복잡도 | 낮음 | 낮음 | 높음 |\n")
    report.append("| 학습 속도 | 빠름 | 빠름 | 느림 |\n")
    report.append("| 비선형 학습 | ❌ | ❌ | ✅ |\n")
    report.append("| 확률 출력 | ❌ | ✅ | ✅ |\n")
    report.append("| 해석 가능성 | 높음 | 높음 | 낮음 |\n")
    report.append("| 과적합 위험 | 낮음 | 낮음 | 높음 |\n\n")

    # 학습 계획
    report.append("## 3. 학습 계획\n\n")
    report.append("### 학습 데이터\n")
    report.append("- Train: 1,174행 (2019-2023)\n")
    report.append("- Validation: Train의 20% (약 235행)\n")
    report.append("- Test: 243행 (2024)\n\n")

    report.append("### 평가 지표\n")
    report.append("**회귀 모델 (선형 회귀)**:\n")
    report.append("- MSE (Mean Squared Error)\n")
    report.append("- RMSE (Root Mean Squared Error)\n")
    report.append("- R² Score\n\n")

    report.append("**분류 모델 (로지스틱 회귀, MLP)**:\n")
    report.append("- Accuracy (정확도)\n")
    report.append("- Precision (정밀도)\n")
    report.append("- Recall (재현율)\n")
    report.append("- F1-Score\n")
    report.append("- Confusion Matrix\n\n")

    # 다음 단계
    report.append("## 4. 다음 단계 (Stage 4: 학습)\n\n")
    report.append("- [ ] 선형 회귀 모델 학습 및 평가\n")
    report.append("- [ ] 로지스틱 회귀 모델 학습 및 평가\n")
    report.append("- [ ] MLP 모델 학습 및 평가\n")
    report.append("- [ ] 3가지 모델 성능 비교\n")
    report.append("- [ ] 학습 곡선 시각화\n")
    report.append("- [ ] 최종 모델 선정\n")

    report_text = ''.join(report)
    print(report_text)

    # 파일 저장
    with open('data/processed/model_design_report.md', 'w', encoding='utf-8') as f:
        f.write(report_text)
    print("✅ 모델 설계 리포트 저장: data/processed/model_design_report.md")


def save_model_configs():
    """모델 설정 저장"""
    print("\n" + "=" * 60)
    print("💾 모델 설정 저장")
    print("=" * 60)

    configs = {
        'linear_regression': {
            'model_type': 'LinearRegression',
            'params': {
                'fit_intercept': True
            },
            'task': 'regression',
            'target': 'target_return'
        },
        'logistic_regression': {
            'model_type': 'LogisticRegression',
            'params': {
                'penalty': 'l2',
                'C': 1.0,
                'solver': 'lbfgs',
                'max_iter': 1000,
                'random_state': 42
            },
            'task': 'classification',
            'target': 'target'
        },
        'mlp': {
            'model_type': 'MLP',
            'architecture': {
                'input_dim': 24,
                'hidden_layers': [32, 16],
                'output_dim': 1,
                'activation': 'relu',
                'output_activation': 'sigmoid',
                'dropout': 0.3
            },
            'training': {
                'optimizer': 'adam',
                'learning_rate': 0.001,
                'loss': 'binary_crossentropy',
                'batch_size': 32,
                'epochs': 100,
                'validation_split': 0.2
            },
            'task': 'classification',
            'target': 'target'
        }
    }

    # JSON 저장
    import json
    with open('data/processed/model_configs.json', 'w', encoding='utf-8') as f:
        json.dump(configs, f, indent=2, ensure_ascii=False)

    print("✅ 모델 설정 저장: data/processed/model_configs.json")


def main():
    """메인 실행 함수"""
    print("\n" + "🎨" * 30)
    print("Simple Kospi 프로젝트 - Stage 3: 모델 설계")
    print("🎨" * 30)

    # 1. 데이터 로드
    X_train, X_test, y_train, y_test, y_train_reg, y_test_reg, feature_cols = load_data()

    input_dim = X_train.shape[1]

    # 2. 모델 설계
    model_lr = design_linear_regression()
    model_logistic = design_logistic_regression()
    model_mlp = design_mlp_model(input_dim)

    # 3. 아키텍처 시각화
    visualize_model_architectures(input_dim)

    # 4. 설계 리포트 생성
    create_model_design_report(input_dim)

    # 5. 모델 설정 저장
    save_model_configs()

    print("\n" + "=" * 60)
    print("✅ Stage 3: 모델 설계 완료!")
    print("=" * 60)

    print("\n📊 설계된 모델:")
    print("   1. 선형 회귀: 25개 파라미터")
    print("   2. 로지스틱 회귀: 25개 파라미터")
    total_params = (input_dim * 32 + 32) + (32 * 16 + 16) + (16 * 1 + 1)
    print(f"   3. MLP: {total_params:,}개 파라미터")

    print("\n다음 단계:")
    print("  python 04_model_training.py")


if __name__ == "__main__":
    main()
