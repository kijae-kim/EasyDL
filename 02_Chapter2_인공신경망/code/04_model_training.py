"""
Stage 4: Simple Kospi - 모델 학습

목표:
1. 전처리된 데이터로 3가지 모델 학습
2. 각 모델의 성능 측정 및 비교
3. 학습 과정 시각화
4. 학습된 모델 저장

생성 파일:
- models/linear_regression.pkl
- models/logistic_regression.pkl
- models/mlp_model.keras
- models/training_history.json
- data/processed/model_training_report.md
- ../assets/training_curves.png
- ../assets/model_comparison.png
- ../assets/confusion_matrices.png
"""

import os
import json
import pickle
import warnings
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix
)

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, callbacks

warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False


def load_data():
    """
    학습/테스트 데이터 및 설정 로드

    Returns:
        X_train, X_test: 특징 데이터
        y_train, y_test: 분류 타겟 (0/1)
        y_train_reg, y_test_reg: 회귀 타겟 (수익률)
        configs: 모델 설정 딕셔너리
    """
    print("📂 데이터 로딩 중...")

    # 데이터 로드
    train_df = pd.read_csv('data/processed/train_data.csv')
    test_df = pd.read_csv('data/processed/test_data.csv')

    # 특징과 타겟 분리
    feature_cols = [col for col in train_df.columns
                   if col not in ['target', 'target_return', 'Date']]

    X_train = train_df[feature_cols].values
    X_test = test_df[feature_cols].values

    y_train = train_df['target'].values  # 분류 타겟 (0/1)
    y_test = test_df['target'].values

    y_train_reg = train_df['target_return'].values  # 회귀 타겟 (수익률)
    y_test_reg = test_df['target_return'].values

    # 모델 설정 로드
    with open('data/processed/model_configs.json', 'r', encoding='utf-8') as f:
        configs = json.load(f)

    print(f"✅ 데이터 로드 완료")
    print(f"   - Train: {X_train.shape[0]}개 샘플, {X_train.shape[1]}개 특징")
    print(f"   - Test: {X_test.shape[0]}개 샘플")
    print(f"   - 분류 타겟 비율: 상승 {y_train.mean():.2%}")

    return X_train, X_test, y_train, y_test, y_train_reg, y_test_reg, configs


def train_linear_regression(X_train, X_test, y_train_reg, y_test_reg):
    """
    선형 회귀 모델 학습 및 평가

    Returns:
        model: 학습된 모델
        metrics: 평가 지표 딕셔너리
    """
    print("🔧 모델 1: 선형 회귀 학습 중...")

    # 모델 생성 및 학습
    model = LinearRegression(fit_intercept=True)
    model.fit(X_train, y_train_reg)

    # 예측
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # 평가 지표 계산
    metrics = {
        'train_mse': mean_squared_error(y_train_reg, y_train_pred),
        'train_mae': mean_absolute_error(y_train_reg, y_train_pred),
        'train_r2': r2_score(y_train_reg, y_train_pred),
        'test_mse': mean_squared_error(y_test_reg, y_test_pred),
        'test_mae': mean_absolute_error(y_test_reg, y_test_pred),
        'test_r2': r2_score(y_test_reg, y_test_pred),
    }

    # 모델 저장
    os.makedirs('models', exist_ok=True)
    with open('models/linear_regression.pkl', 'wb') as f:
        pickle.dump(model, f)

    print(f"✅ 선형 회귀 학습 완료")
    print(f"   - Train R²: {metrics['train_r2']:.4f}")
    print(f"   - Test R²: {metrics['test_r2']:.4f}")
    print(f"   - Test MAE: {metrics['test_mae']:.4f}")

    return model, metrics


def train_logistic_regression(X_train, X_test, y_train, y_test, config):
    """
    로지스틱 회귀 모델 학습 및 평가

    Returns:
        model: 학습된 모델
        metrics: 평가 지표 딕셔너리
    """
    print("🔧 모델 2: 로지스틱 회귀 학습 중...")

    # 모델 생성 및 학습
    params = config['params']
    model = LogisticRegression(
        penalty=params['penalty'],
        C=params['C'],
        solver=params['solver'],
        max_iter=params['max_iter'],
        random_state=params['random_state']
    )
    model.fit(X_train, y_train)

    # 예측
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # 평가 지표 계산
    metrics = {
        'train_accuracy': accuracy_score(y_train, y_train_pred),
        'train_precision': precision_score(y_train, y_train_pred, zero_division=0),
        'train_recall': recall_score(y_train, y_train_pred, zero_division=0),
        'train_f1': f1_score(y_train, y_train_pred, zero_division=0),
        'test_accuracy': accuracy_score(y_test, y_test_pred),
        'test_precision': precision_score(y_test, y_test_pred, zero_division=0),
        'test_recall': recall_score(y_test, y_test_pred, zero_division=0),
        'test_f1': f1_score(y_test, y_test_pred, zero_division=0),
        'confusion_matrix': confusion_matrix(y_test, y_test_pred)
    }

    # 모델 저장
    with open('models/logistic_regression.pkl', 'wb') as f:
        pickle.dump(model, f)

    print(f"✅ 로지스틱 회귀 학습 완료")
    print(f"   - Train Accuracy: {metrics['train_accuracy']:.4f}")
    print(f"   - Test Accuracy: {metrics['test_accuracy']:.4f}")
    print(f"   - Test F1: {metrics['test_f1']:.4f}")

    return model, metrics


def train_mlp(X_train, X_test, y_train, y_test, config):
    """
    MLP 모델 학습 및 평가

    Returns:
        model: 학습된 모델
        history: 학습 히스토리
        metrics: 평가 지표 딕셔너리
    """
    print("🔧 모델 3: MLP 학습 중...")

    arch = config['architecture']
    train_config = config['training']

    # 모델 구성
    model = keras.Sequential([
        keras.layers.Input(shape=(arch['input_dim'],)),
        keras.layers.Dense(arch['hidden_layers'][0], activation=arch['activation'], name='hidden1'),
        keras.layers.Dropout(arch['dropout'], name='dropout1'),
        keras.layers.Dense(arch['hidden_layers'][1], activation=arch['activation'], name='hidden2'),
        keras.layers.Dropout(arch['dropout'], name='dropout2'),
        keras.layers.Dense(arch['output_dim'], activation=arch['output_activation'], name='output')
    ])

    # 컴파일
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=train_config['learning_rate']),
        loss=train_config['loss'],
        metrics=[
            'accuracy',
            keras.metrics.Precision(name='precision'),
            keras.metrics.Recall(name='recall')
        ]
    )

    # Early Stopping 설정
    early_stop = callbacks.EarlyStopping(
        monitor='val_loss',
        patience=15,
        restore_best_weights=True,
        verbose=1
    )

    # 학습
    print(f"\n학습 시작 (Epochs: {train_config['epochs']}, Batch Size: {train_config['batch_size']})")
    history = model.fit(
        X_train, y_train,
        batch_size=train_config['batch_size'],
        epochs=train_config['epochs'],
        validation_split=train_config['validation_split'],
        callbacks=[early_stop],
        verbose=1
    )

    # 예측
    y_train_pred_proba = model.predict(X_train, verbose=0)
    y_test_pred_proba = model.predict(X_test, verbose=0)

    y_train_pred = (y_train_pred_proba > 0.5).astype(int).flatten()
    y_test_pred = (y_test_pred_proba > 0.5).astype(int).flatten()

    # 평가 지표 계산
    metrics = {
        'train_accuracy': accuracy_score(y_train, y_train_pred),
        'train_precision': precision_score(y_train, y_train_pred, zero_division=0),
        'train_recall': recall_score(y_train, y_train_pred, zero_division=0),
        'train_f1': f1_score(y_train, y_train_pred, zero_division=0),
        'test_accuracy': accuracy_score(y_test, y_test_pred),
        'test_precision': precision_score(y_test, y_test_pred, zero_division=0),
        'test_recall': recall_score(y_test, y_test_pred, zero_division=0),
        'test_f1': f1_score(y_test, y_test_pred, zero_division=0),
        'confusion_matrix': confusion_matrix(y_test, y_test_pred),
        'epochs_trained': len(history.history['loss'])
    }

    # 모델 저장
    model.save('models/mlp_model.keras')

    # 학습 히스토리 저장
    history_dict = {k: [float(v) for v in vals] for k, vals in history.history.items()}
    with open('models/training_history.json', 'w') as f:
        json.dump(history_dict, f, indent=2)

    print(f"\n✅ MLP 학습 완료 ({metrics['epochs_trained']} epochs)")
    print(f"   - Train Accuracy: {metrics['train_accuracy']:.4f}")
    print(f"   - Test Accuracy: {metrics['test_accuracy']:.4f}")
    print(f"   - Test F1: {metrics['test_f1']:.4f}")

    return model, history, metrics


def visualize_training(mlp_history, logr_metrics, mlp_metrics, lr_metrics):
    """
    학습 결과 시각화

    Args:
        mlp_history: MLP 학습 히스토리
        logr_metrics: 로지스틱 회귀 평가 지표
        mlp_metrics: MLP 평가 지표
        lr_metrics: 선형 회귀 평가 지표
    """
    print("📊 학습 결과 시각화 중...")

    os.makedirs('../assets', exist_ok=True)

    # 1. MLP 학습 곡선
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Loss 곡선
    axes[0].plot(mlp_history.history['loss'], label='Train Loss', linewidth=2)
    axes[0].plot(mlp_history.history['val_loss'], label='Validation Loss', linewidth=2)
    axes[0].set_xlabel('Epoch', fontsize=12)
    axes[0].set_ylabel('Loss', fontsize=12)
    axes[0].set_title('MLP 학습 곡선 - Loss', fontsize=14, fontweight='bold')
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3)

    # Accuracy 곡선
    axes[1].plot(mlp_history.history['accuracy'], label='Train Accuracy', linewidth=2)
    axes[1].plot(mlp_history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
    axes[1].set_xlabel('Epoch', fontsize=12)
    axes[1].set_ylabel('Accuracy', fontsize=12)
    axes[1].set_title('MLP 학습 곡선 - Accuracy', fontsize=14, fontweight='bold')
    axes[1].legend(fontsize=10)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('../assets/training_curves.png', dpi=100, bbox_inches='tight')
    plt.close()

    # 2. 모델 성능 비교
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # 분류 모델 비교 (Accuracy & F1)
    models = ['Logistic\nRegression', 'MLP']
    accuracies = [logr_metrics['test_accuracy'], mlp_metrics['test_accuracy']]
    f1_scores = [logr_metrics['test_f1'], mlp_metrics['test_f1']]

    x = np.arange(len(models))
    width = 0.35

    axes[0].bar(x - width/2, accuracies, width, label='Accuracy', alpha=0.8)
    axes[0].bar(x + width/2, f1_scores, width, label='F1 Score', alpha=0.8)
    axes[0].axhline(y=0.5, color='r', linestyle='--', label='Random Baseline', alpha=0.5)
    axes[0].set_ylabel('Score', fontsize=12)
    axes[0].set_title('분류 모델 성능 비교 (Test Set)', fontsize=14, fontweight='bold')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(models, fontsize=10)
    axes[0].legend(fontsize=10)
    axes[0].grid(True, alpha=0.3, axis='y')
    axes[0].set_ylim([0, 1])

    # 선형 회귀 성능 (별도 표시)
    metrics_names = ['R²', 'MAE']
    lr_values = [lr_metrics['test_r2'], lr_metrics['test_mae']]

    axes[1].bar(metrics_names, lr_values, alpha=0.8, color='skyblue')
    axes[1].set_ylabel('Value', fontsize=12)
    axes[1].set_title('선형 회귀 성능 (Test Set)', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('../assets/model_comparison.png', dpi=100, bbox_inches='tight')
    plt.close()

    # 3. Confusion Matrix
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Logistic Regression
    sns.heatmap(logr_metrics['confusion_matrix'], annot=True, fmt='d', cmap='Blues',
                xticklabels=['Down (0)', 'Up (1)'], yticklabels=['Down (0)', 'Up (1)'],
                ax=axes[0], cbar_kws={'label': 'Count'})
    axes[0].set_title('Logistic Regression - Confusion Matrix', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Actual', fontsize=11)
    axes[0].set_xlabel('Predicted', fontsize=11)

    # MLP
    sns.heatmap(mlp_metrics['confusion_matrix'], annot=True, fmt='d', cmap='Greens',
                xticklabels=['Down (0)', 'Up (1)'], yticklabels=['Down (0)', 'Up (1)'],
                ax=axes[1], cbar_kws={'label': 'Count'})
    axes[1].set_title('MLP - Confusion Matrix', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Actual', fontsize=11)
    axes[1].set_xlabel('Predicted', fontsize=11)

    plt.tight_layout()
    plt.savefig('../assets/confusion_matrices.png', dpi=100, bbox_inches='tight')
    plt.close()

    print(f"✅ 시각화 완료")
    print(f"   - training_curves.png")
    print(f"   - model_comparison.png")
    print(f"   - confusion_matrices.png")


def generate_report(lr_metrics, logr_metrics, mlp_metrics, train_size, test_size):
    """
    학습 결과 마크다운 리포트 생성

    Args:
        lr_metrics: 선형 회귀 평가 지표
        logr_metrics: 로지스틱 회귀 평가 지표
        mlp_metrics: MLP 평가 지표
        train_size: 학습 데이터 크기
        test_size: 테스트 데이터 크기
    """
    print("📝 학습 리포트 생성 중...")

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 최고 성능 모델 찾기
    best_model = 'MLP' if mlp_metrics['test_accuracy'] > logr_metrics['test_accuracy'] else 'Logistic Regression'
    best_acc = max(mlp_metrics['test_accuracy'], logr_metrics['test_accuracy'])
    improvement = (best_acc - 0.5) / 0.5 * 100  # Random baseline 대비 개선율

    report = f"""
# Simple Kospi - 모델 학습 리포트
**생성 일시**: {timestamp}

## 1. 학습 개요

- **학습 데이터**: {train_size:,}개 샘플
- **테스트 데이터**: {test_size:,}개 샘플
- **모델**: 선형 회귀, 로지스틱 회귀, MLP
- **평가 방식**: 시계열 순차 분할 (과거→미래)

## 2. 모델별 성능

### 2.1 선형 회귀 (회귀)

**목표**: 다음날 수익률 예측

| 지표 | Train | Test |
|------|-------|------|
| MSE | {lr_metrics['train_mse']:.6f} | {lr_metrics['test_mse']:.6f} |
| MAE | {lr_metrics['train_mae']:.6f} | {lr_metrics['test_mae']:.6f} |
| R² | {lr_metrics['train_r2']:.4f} | {lr_metrics['test_r2']:.4f} |

**분석**: R² 값이 매우 낮아 수익률의 변동성을 거의 설명하지 못함. 주가 수익률 예측의 어려움을 보여줌.

### 2.2 로지스틱 회귀 (분류)

**목표**: 다음날 등락 방향 예측 (상승/하락)

| 지표 | Train | Test |
|------|-------|------|
| Accuracy | {logr_metrics['train_accuracy']:.4f} ({logr_metrics['train_accuracy']*100:.2f}%) | {logr_metrics['test_accuracy']:.4f} ({logr_metrics['test_accuracy']*100:.2f}%) |
| Precision | {logr_metrics['train_precision']:.4f} | {logr_metrics['test_precision']:.4f} |
| Recall | {logr_metrics['train_recall']:.4f} | {logr_metrics['test_recall']:.4f} |
| F1 Score | {logr_metrics['train_f1']:.4f} | {logr_metrics['test_f1']:.4f} |

**Confusion Matrix** (Test Set):
```
              Predicted
              Down   Up
Actual Down   {logr_metrics['confusion_matrix'][0,0]:4d}  {logr_metrics['confusion_matrix'][0,1]:4d}
       Up     {logr_metrics['confusion_matrix'][1,0]:4d}  {logr_metrics['confusion_matrix'][1,1]:4d}
```

### 2.3 MLP (분류)

**목표**: 다음날 등락 방향 예측 (상승/하락)

**아키텍처**: Input(24) → Dense(32, ReLU) → Dropout(0.3) → Dense(16, ReLU) → Dropout(0.3) → Dense(1, Sigmoid)

| 지표 | Train | Test |
|------|-------|------|
| Accuracy | {mlp_metrics['train_accuracy']:.4f} ({mlp_metrics['train_accuracy']*100:.2f}%) | {mlp_metrics['test_accuracy']:.4f} ({mlp_metrics['test_accuracy']*100:.2f}%) |
| Precision | {mlp_metrics['train_precision']:.4f} | {mlp_metrics['test_precision']:.4f} |
| Recall | {mlp_metrics['train_recall']:.4f} | {mlp_metrics['test_recall']:.4f} |
| F1 Score | {mlp_metrics['train_f1']:.4f} | {mlp_metrics['test_f1']:.4f} |

**학습 정보**:
- 학습된 에포크: {mlp_metrics['epochs_trained']} / 100
- Early Stopping 적용: Validation Loss 기준

**Confusion Matrix** (Test Set):
```
              Predicted
              Down   Up
Actual Down   {mlp_metrics['confusion_matrix'][0,0]:4d}  {mlp_metrics['confusion_matrix'][0,1]:4d}
       Up     {mlp_metrics['confusion_matrix'][1,0]:4d}  {mlp_metrics['confusion_matrix'][1,1]:4d}
```

## 3. 모델 비교

### Test Set Accuracy 순위

1. **{best_model}**: {best_acc:.4f} ({best_acc*100:.2f}%)
2. **{'Logistic Regression' if best_model == 'MLP' else 'MLP'}**: {min(mlp_metrics['test_accuracy'], logr_metrics['test_accuracy']):.4f} ({min(mlp_metrics['test_accuracy'], logr_metrics['test_accuracy'])*100:.2f}%)

### Random Baseline 대비 개선

- **Random Baseline**: 50% (단순 동전 던지기)
- **최고 성능**: {best_acc*100:.2f}%
- **개선율**: {improvement:+.2f}%

## 4. 분석 및 인사이트

### 과적합/과소적합 분석

"""

    # 과적합 여부 판단
    if mlp_metrics['train_accuracy'] - mlp_metrics['test_accuracy'] > 0.1:
        report += "- **MLP**: 약간의 과적합 징후 (Train-Test 격차 10% 이상)\n"
    else:
        report += "- **MLP**: 비교적 안정적인 일반화 성능\n"

    if logr_metrics['train_accuracy'] - logr_metrics['test_accuracy'] > 0.1:
        report += "- **Logistic Regression**: 약간의 과적합 징후\n"
    else:
        report += "- **Logistic Regression**: 안정적인 일반화 성능\n"

    report += f"""

### 모델별 장단점

**선형 회귀**:
- ✅ 해석 용이, 빠른 학습
- ❌ 주가 수익률 예측에는 부적합 (R² ≈ {lr_metrics['test_r2']:.3f})

**로지스틱 회귀**:
- ✅ 간단하고 안정적
- ✅ 확률 출력으로 신뢰도 판단 가능
- ⚠️ 비선형 패턴 학습 한계

**MLP**:
- ✅ 비선형 패턴 학습 가능
- ✅ 가장 높은 예측 정확도
- ⚠️ 과적합 위험, 해석 어려움

### 실전 적용 가능성 평가

- **현재 최고 성능**: {best_acc*100:.2f}% (Random 50% 대비 {improvement:+.2f}%)
- **실전 수익 기준**: 일반적으로 53% 이상이면 장기 수익 가능
"""

    if best_acc >= 0.53:
        report += f"- **평가**: ✅ 실전 적용 가능한 수준 (기준 충족)\n"
    else:
        report += f"- **평가**: ⚠️ 추가 개선 필요 (기준: 53% 이상)\n"

    report += """

## 5. 다음 단계 (Stage 5: 평가)

- [ ] 상세 성능 평가 및 시각화
- [ ] 특징 중요도 분석 (어떤 특징이 중요한가?)
- [ ] 백테스팅 시뮬레이션 (실제 수익률 계산)
- [ ] 최종 모델 선정 및 결론

## 6. 생성된 파일

### 모델 파일
- `models/linear_regression.pkl`
- `models/logistic_regression.pkl`
- `models/mlp_model.keras`
- `models/training_history.json`

### 시각화 파일
- `../assets/training_curves.png` - MLP 학습 곡선
- `../assets/model_comparison.png` - 모델 성능 비교
- `../assets/confusion_matrices.png` - 혼동 행렬

---
*이 리포트는 Stage 4 실행 시 자동 생성되었습니다.*
"""

    # 리포트 저장
    with open('data/processed/model_training_report.md', 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✅ 리포트 저장 완료: data/processed/model_training_report.md")


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("Stage 4: Simple Kospi - 모델 학습")
    print("=" * 60)

    # 1. 데이터 로딩
    X_train, X_test, y_train, y_test, y_train_reg, y_test_reg, configs = load_data()

    # 2. 선형 회귀 학습
    print("\n" + "=" * 60)
    lr_model, lr_metrics = train_linear_regression(X_train, X_test, y_train_reg, y_test_reg)

    # 3. 로지스틱 회귀 학습
    print("\n" + "=" * 60)
    logr_model, logr_metrics = train_logistic_regression(
        X_train, X_test, y_train, y_test, configs['logistic_regression']
    )

    # 4. MLP 학습
    print("\n" + "=" * 60)
    mlp_model, mlp_history, mlp_metrics = train_mlp(
        X_train, X_test, y_train, y_test, configs['mlp']
    )

    # 5. 시각화
    print("\n" + "=" * 60)
    visualize_training(mlp_history, logr_metrics, mlp_metrics, lr_metrics)

    # 6. 리포트 생성
    print("\n" + "=" * 60)
    generate_report(lr_metrics, logr_metrics, mlp_metrics, len(X_train), len(X_test))

    # 7. 완료 메시지
    print("\n" + "=" * 60)
    print("✅ Stage 4: 모델 학습 완료!")
    print("\n📊 학습된 모델:")
    print(f"   1. 선형 회귀: Test R² = {lr_metrics['test_r2']:.4f}, MAE = {lr_metrics['test_mae']:.4f}")
    print(f"   2. 로지스틱 회귀: Test Acc = {logr_metrics['test_accuracy']:.4f} ({logr_metrics['test_accuracy']*100:.2f}%)")
    print(f"   3. MLP: Test Acc = {mlp_metrics['test_accuracy']:.4f} ({mlp_metrics['test_accuracy']*100:.2f}%)")

    # 최고 성능 모델
    best_model = 'MLP' if mlp_metrics['test_accuracy'] > logr_metrics['test_accuracy'] else 'Logistic Regression'
    best_acc = max(mlp_metrics['test_accuracy'], logr_metrics['test_accuracy'])
    print(f"\n🏆 최고 성능 모델: {best_model} ({best_acc*100:.2f}%)")

    print("\n다음 단계:")
    print("  python 05_model_evaluation.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
