#!/usr/bin/env python3
"""
Chapter 2: 인공신경망 시각화 생성 스크립트

생성할 그래프:
1. 신경망 구조도
2. 선형 회귀 예시
3. Loss 함수 표면 (3D)
4. Gradient Descent 과정
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

# 한글 폰트 설정 (macOS)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

# 스타일 설정
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# 저장 경로
SAVE_DIR = '../assets/'

import os
os.makedirs(SAVE_DIR, exist_ok=True)


def draw_neural_network():
    """
    1. 신경망 구조도 (Input-Hidden-Output)
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    # 레이어 정의
    layers = [3, 4, 2, 1]  # Input(3) -> Hidden(4) -> Hidden(2) -> Output(1)
    layer_names = ['Input Layer', 'Hidden Layer 1', 'Hidden Layer 2', 'Output Layer']

    # 노드 위치 계산
    v_spacing = 1.0
    h_spacing = 2.0

    # 각 레이어의 노드 그리기
    node_positions = []

    for layer_idx, n_nodes in enumerate(layers):
        layer_pos = []
        x = layer_idx * h_spacing

        # 중앙 정렬을 위한 offset
        y_offset = (max(layers) - n_nodes) * v_spacing / 2

        for node_idx in range(n_nodes):
            y = node_idx * v_spacing + y_offset
            layer_pos.append((x, y))

            # 노드 그리기
            circle = plt.Circle((x, y), 0.15, color='skyblue', ec='black', zorder=4)
            ax.add_patch(circle)

            # 레이어 이름 표시 (첫 번째 노드에만)
            if node_idx == 0:
                ax.text(x, y + 0.6, layer_names[layer_idx],
                       ha='center', va='bottom', fontsize=12, fontweight='bold')

        node_positions.append(layer_pos)

    # 엣지 그리기 (Fully Connected)
    for layer_idx in range(len(layers) - 1):
        for i, (x1, y1) in enumerate(node_positions[layer_idx]):
            for j, (x2, y2) in enumerate(node_positions[layer_idx + 1]):
                # 연결선
                ax.plot([x1, x2], [y1, y2], 'gray', alpha=0.3, linewidth=0.5, zorder=1)

                # 가중치 표시 (일부만)
                if i == 0 and j == 0:
                    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                    ax.text(mid_x, mid_y + 0.1, 'w', fontsize=8, color='red', ha='center')

    # 입력/출력 레이블
    for i, (x, y) in enumerate(node_positions[0]):
        ax.text(x - 0.5, y, f'$x_{i+1}$', ha='right', va='center', fontsize=11)

    ax.text(node_positions[-1][0][0] + 0.5, node_positions[-1][0][1],
           '$y$', ha='left', va='center', fontsize=11)

    # 축 설정
    ax.set_xlim(-1, len(layers) * h_spacing)
    ax.set_ylim(-1, max(layers) * v_spacing + 1)
    ax.axis('off')

    plt.title('인공신경망 구조 (Multi-Layer Perceptron)', fontsize=16, pad=20)
    plt.tight_layout()
    plt.savefig(SAVE_DIR + 'neural_network_structure.png', dpi=300, bbox_inches='tight')
    print("✅ 신경망 구조도 생성 완료: neural_network_structure.png")
    plt.close()


def linear_regression_example():
    """
    2. 선형 회귀 예시 (데이터, 회귀선, 오차)
    """
    # 예제 데이터: YouTube 조회수 vs 수익
    x = np.array([1000, 2000, 3000, 4000, 5000])
    y = np.array([10, 18, 32, 41, 48])

    # 선형 회귀 (최소제곱법)
    n = len(x)
    w = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x**2) - np.sum(x)**2)
    b = (np.sum(y) - w * np.sum(x)) / n

    # 예측값
    y_pred = w * x + b

    # 그래프 그리기
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 왼쪽: 선형 회귀
    ax1.scatter(x, y, s=100, color='blue', alpha=0.7, label='실제 데이터', zorder=3)

    # 회귀선
    x_line = np.linspace(x.min() - 500, x.max() + 500, 100)
    y_line = w * x_line + b
    ax1.plot(x_line, y_line, 'r-', linewidth=2, label=f'회귀선: y = {w:.4f}x + {b:.2f}')

    # 오차 표시
    for i in range(len(x)):
        ax1.plot([x[i], x[i]], [y[i], y_pred[i]], 'g--', alpha=0.5, linewidth=1.5)
    ax1.scatter(x, y_pred, s=50, color='red', alpha=0.5, marker='x', label='예측값')

    ax1.set_xlabel('조회수 (views)', fontsize=12)
    ax1.set_ylabel('수익 (만원)', fontsize=12)
    ax1.set_title('선형 회귀 예시: 조회수로 수익 예측', fontsize=14)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    # 오른쪽: Loss (MSE) 계산
    mse = np.mean((y - y_pred)**2)
    errors = y - y_pred

    ax2.bar(range(len(errors)), errors**2, color='orange', alpha=0.7, edgecolor='black')
    ax2.axhline(y=mse, color='red', linestyle='--', linewidth=2, label=f'MSE = {mse:.2f}')
    ax2.set_xlabel('데이터 인덱스', fontsize=12)
    ax2.set_ylabel('제곱 오차 $(y - \hat{y})^2$', fontsize=12)
    ax2.set_title('각 데이터 포인트의 제곱 오차', fontsize=14)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(SAVE_DIR + 'linear_regression_example.png', dpi=300, bbox_inches='tight')
    print(f"✅ 선형 회귀 예시 생성 완료: linear_regression_example.png")
    print(f"   최적 파라미터: w = {w:.4f}, b = {b:.2f}, MSE = {mse:.2f}")
    plt.close()


def loss_surface_3d():
    """
    3. Loss 함수 표면 (3D) - w와 b에 대한 MSE
    """
    # 간단한 데이터셋
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 5, 4, 5])

    # w, b 범위
    w_range = np.linspace(-2, 4, 100)
    b_range = np.linspace(-2, 4, 100)
    W, B = np.meshgrid(w_range, b_range)

    # Loss 계산
    Loss = np.zeros_like(W)
    for i in range(len(w_range)):
        for j in range(len(b_range)):
            y_pred = W[j, i] * x + B[j, i]
            Loss[j, i] = np.mean((y - y_pred)**2)

    # 최적값 찾기
    n = len(x)
    w_opt = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x**2) - np.sum(x)**2)
    b_opt = (np.sum(y) - w_opt * np.sum(x)) / n
    loss_opt = np.mean((y - (w_opt * x + b_opt))**2)

    # 3D 그래프
    fig = plt.figure(figsize=(14, 6))

    # 왼쪽: 3D Surface
    ax1 = fig.add_subplot(121, projection='3d')
    surf = ax1.plot_surface(W, B, Loss, cmap='viridis', alpha=0.8, edgecolor='none')
    ax1.scatter([w_opt], [b_opt], [loss_opt], color='red', s=100, marker='*',
               label='최적점', zorder=10)

    ax1.set_xlabel('Weight (w)', fontsize=11)
    ax1.set_ylabel('Bias (b)', fontsize=11)
    ax1.set_zlabel('Loss (MSE)', fontsize=11)
    ax1.set_title('Loss 함수 표면 (3D)', fontsize=14)
    fig.colorbar(surf, ax=ax1, shrink=0.5)
    ax1.legend()

    # 오른쪽: Contour (등고선)
    ax2 = fig.add_subplot(122)
    contour = ax2.contour(W, B, Loss, levels=20, cmap='viridis')
    ax2.clabel(contour, inline=True, fontsize=8)
    ax2.scatter([w_opt], [b_opt], color='red', s=100, marker='*',
               label=f'최적점 (w={w_opt:.2f}, b={b_opt:.2f})', zorder=10)

    ax2.set_xlabel('Weight (w)', fontsize=12)
    ax2.set_ylabel('Bias (b)', fontsize=12)
    ax2.set_title('Loss 함수 등고선', fontsize=14)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(SAVE_DIR + 'loss_surface.png', dpi=300, bbox_inches='tight')
    print(f"✅ Loss 표면 생성 완료: loss_surface.png")
    print(f"   최적점: w = {w_opt:.2f}, b = {b_opt:.2f}, Loss = {loss_opt:.2f}")
    plt.close()


def gradient_descent_animation():
    """
    4. Gradient Descent 과정 시각화
    """
    # 데이터
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 5, 4, 5])

    # 초기값
    w = 0.0
    b = 0.0
    learning_rate = 0.01
    epochs = 100

    # 기록
    w_history = [w]
    b_history = [b]
    loss_history = []

    # Gradient Descent
    for epoch in range(epochs):
        # 예측
        y_pred = w * x + b

        # Loss
        loss = np.mean((y - y_pred)**2)
        loss_history.append(loss)

        # Gradient 계산
        dL_dw = -2 * np.mean(x * (y - y_pred))
        dL_db = -2 * np.mean(y - y_pred)

        # 업데이트
        w = w - learning_rate * dL_dw
        b = b - learning_rate * dL_db

        w_history.append(w)
        b_history.append(b)

    # 시각화
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 왼쪽: Loss 감소 과정
    ax1.plot(loss_history, linewidth=2, color='blue')
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Loss (MSE)', fontsize=12)
    ax1.set_title('Gradient Descent: Loss 감소 과정', fontsize=14)
    ax1.grid(True, alpha=0.3)

    # 주요 지점 표시
    milestones = [0, 10, 30, 50, 99]
    for ms in milestones:
        ax1.scatter([ms], [loss_history[ms]], s=80, zorder=5)
        ax1.annotate(f'Epoch {ms}',
                    xy=(ms, loss_history[ms]),
                    xytext=(ms+5, loss_history[ms]+0.5),
                    fontsize=9,
                    arrowprops=dict(arrowstyle='->', color='gray', lw=1))

    # 오른쪽: 파라미터 공간에서의 이동 경로
    # Loss contour 생성
    w_range = np.linspace(-1, 2, 50)
    b_range = np.linspace(-1, 4, 50)
    W, B = np.meshgrid(w_range, b_range)
    Loss = np.zeros_like(W)

    for i in range(len(w_range)):
        for j in range(len(b_range)):
            y_pred = W[j, i] * x + B[j, i]
            Loss[j, i] = np.mean((y - y_pred)**2)

    ax2.contour(W, B, Loss, levels=15, cmap='viridis', alpha=0.6)

    # Gradient Descent 경로
    ax2.plot(w_history, b_history, 'ro-', markersize=4, linewidth=1.5,
            label='Gradient Descent 경로', alpha=0.7)
    ax2.scatter([w_history[0]], [b_history[0]], s=150, color='green',
               marker='o', label='시작점', zorder=10)
    ax2.scatter([w_history[-1]], [b_history[-1]], s=150, color='red',
               marker='*', label='최종점', zorder=10)

    ax2.set_xlabel('Weight (w)', fontsize=12)
    ax2.set_ylabel('Bias (b)', fontsize=12)
    ax2.set_title('Gradient Descent 경로 (파라미터 공간)', fontsize=14)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(SAVE_DIR + 'gradient_descent_animation.png', dpi=300, bbox_inches='tight')
    print(f"✅ Gradient Descent 과정 생성 완료: gradient_descent_animation.png")
    print(f"   최종 파라미터: w = {w_history[-1]:.4f}, b = {b_history[-1]:.4f}")
    print(f"   최종 Loss: {loss_history[-1]:.4f}")
    plt.close()


def activation_functions():
    """
    보너스: 활성화 함수 비교
    """
    x = np.linspace(-5, 5, 100)

    # 활성화 함수 정의
    sigmoid = 1 / (1 + np.exp(-x))
    relu = np.maximum(0, x)
    tanh = np.tanh(x)
    step = (x >= 0).astype(float)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Step Function
    axes[0, 0].plot(x, step, linewidth=2, color='blue')
    axes[0, 0].set_title('Unit Step Function', fontsize=14)
    axes[0, 0].set_xlabel('x', fontsize=11)
    axes[0, 0].set_ylabel('f(x)', fontsize=11)
    axes[0, 0].grid(True, alpha=0.3)
    axes[0, 0].axhline(y=0, color='k', linewidth=0.5)
    axes[0, 0].axvline(x=0, color='k', linewidth=0.5)

    # Sigmoid
    axes[0, 1].plot(x, sigmoid, linewidth=2, color='green')
    axes[0, 1].set_title('Sigmoid: $\\sigma(x) = \\frac{1}{1 + e^{-x}}$', fontsize=14)
    axes[0, 1].set_xlabel('x', fontsize=11)
    axes[0, 1].set_ylabel('f(x)', fontsize=11)
    axes[0, 1].grid(True, alpha=0.3)
    axes[0, 1].axhline(y=0, color='k', linewidth=0.5)
    axes[0, 1].axvline(x=0, color='k', linewidth=0.5)

    # ReLU
    axes[1, 0].plot(x, relu, linewidth=2, color='red')
    axes[1, 0].set_title('ReLU: $f(x) = \\max(0, x)$', fontsize=14)
    axes[1, 0].set_xlabel('x', fontsize=11)
    axes[1, 0].set_ylabel('f(x)', fontsize=11)
    axes[1, 0].grid(True, alpha=0.3)
    axes[1, 0].axhline(y=0, color='k', linewidth=0.5)
    axes[1, 0].axvline(x=0, color='k', linewidth=0.5)

    # Tanh
    axes[1, 1].plot(x, tanh, linewidth=2, color='purple')
    axes[1, 1].set_title('Tanh: $f(x) = \\tanh(x)$', fontsize=14)
    axes[1, 1].set_xlabel('x', fontsize=11)
    axes[1, 1].set_ylabel('f(x)', fontsize=11)
    axes[1, 1].grid(True, alpha=0.3)
    axes[1, 1].axhline(y=0, color='k', linewidth=0.5)
    axes[1, 1].axvline(x=0, color='k', linewidth=0.5)

    plt.suptitle('활성화 함수 비교', fontsize=16, y=1.00)
    plt.tight_layout()
    plt.savefig(SAVE_DIR + 'activation_functions.png', dpi=300, bbox_inches='tight')
    print("✅ 활성화 함수 비교 생성 완료: activation_functions.png")
    plt.close()


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("📊 Chapter 2 인공신경망 시각화 생성 시작")
    print("=" * 60)

    # 1. 신경망 구조도
    draw_neural_network()

    # 2. 선형 회귀 예시
    linear_regression_example()

    # 3. Loss 함수 표면
    loss_surface_3d()

    # 4. Gradient Descent 과정
    gradient_descent_animation()

    # 보너스: 활성화 함수
    activation_functions()

    print("\n" + "=" * 60)
    print("✅ 모든 시각화 생성 완료!")
    print(f"📂 저장 위치: {SAVE_DIR}")
    print("=" * 60)

    print("\n생성된 파일:")
    print("  1. neural_network_structure.png - 신경망 구조도")
    print("  2. linear_regression_example.png - 선형 회귀 예시")
    print("  3. loss_surface.png - Loss 함수 표면")
    print("  4. gradient_descent_animation.png - Gradient Descent 과정")
    print("  5. activation_functions.png - 활성화 함수 비교")


if __name__ == "__main__":
    main()
