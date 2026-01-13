#!/usr/bin/env python3
"""
Chapter 2: 선형 회귀 (Linear Regression) 간단한 예제

목표:
- 선형 함수 y = wx + b 학습
- Loss 함수 (MSE) 계산
- Gradient Descent 구현
"""

import numpy as np
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False


def main():
    """메인 함수"""
    print("=" * 60)
    print("📚 Chapter 2: 선형 회귀 예제")
    print("=" * 60)

    # 1. 데이터 준비
    print("\n1️⃣ 데이터 준비")
    x = np.array([1000, 2000, 3000, 4000, 5000])
    y = np.array([10, 18, 32, 41, 48])

    print(f"   입력(조회수): {x}")
    print(f"   출력(수익): {y}")

    # 2. 최소제곱법으로 최적 파라미터 계산
    print("\n2️⃣ 최소제곱법으로 최적해 계산")
    n = len(x)
    w_optimal = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x**2) - np.sum(x)**2)
    b_optimal = (np.sum(y) - w_optimal * np.sum(x)) / n

    print(f"   최적 가중치(w): {w_optimal:.6f}")
    print(f"   최적 바이어스(b): {b_optimal:.6f}")

    y_pred_optimal = w_optimal * x + b_optimal
    mse_optimal = np.mean((y - y_pred_optimal)**2)
    print(f"   최적 MSE: {mse_optimal:.4f}")

    # 3. Gradient Descent로 학습
    print("\n3️⃣ Gradient Descent로 학습")

    # 초기값
    w = 0.0
    b = 0.0
    learning_rate = 0.0000001  # 매우 작은 학습률 (스케일 때문)
    epochs = 10000

    # 기록
    w_history = []
    b_history = []
    loss_history = []

    # 학습
    for epoch in range(epochs):
        # 예측
        y_pred = w * x + b

        # Loss 계산
        loss = np.mean((y - y_pred)**2)

        # Gradient 계산
        dL_dw = -2 * np.mean(x * (y - y_pred))
        dL_db = -2 * np.mean(y - y_pred)

        # 파라미터 업데이트
        w = w - learning_rate * dL_dw
        b = b - learning_rate * dL_db

        # 기록
        w_history.append(w)
        b_history.append(b)
        loss_history.append(loss)

        # 중간 출력
        if (epoch + 1) % 2000 == 0:
            print(f"   Epoch {epoch+1:5d}: Loss = {loss:.4f}, w = {w:.6f}, b = {b:.4f}")

    print(f"\n   최종 결과:")
    print(f"   학습된 가중치(w): {w:.6f}")
    print(f"   학습된 바이어스(b): {b:.4f}")
    print(f"   최종 MSE: {loss_history[-1]:.4f}")

    # 4. 예측 테스트
    print("\n4️⃣ 새로운 데이터로 예측 테스트")
    test_views = [6000, 7000, 8000]

    print("\n   최소제곱법 모델:")
    for views in test_views:
        revenue = w_optimal * views + b_optimal
        print(f"   조회수 {views}회 → 예상 수익: {revenue:.2f}만원")

    print("\n   Gradient Descent 모델:")
    for views in test_views:
        revenue = w * views + b
        print(f"   조회수 {views}회 → 예상 수익: {revenue:.2f}만원")

    # 5. 시각화
    print("\n5️⃣ 결과 시각화")
    visualize_results(x, y, w_optimal, b_optimal, w, b, loss_history)

    print("\n" + "=" * 60)
    print("✅ 학습 완료!")
    print("=" * 60)


def visualize_results(x, y, w_opt, b_opt, w_gd, b_gd, loss_history):
    """결과 시각화"""

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))

    # 1. 선형 회귀 결과
    ax1 = axes[0]
    ax1.scatter(x, y, s=100, color='blue', alpha=0.7, label='실제 데이터', zorder=3)

    # 최소제곱법
    x_line = np.linspace(x.min() - 500, x.max() + 1000, 100)
    y_opt = w_opt * x_line + b_opt
    ax1.plot(x_line, y_opt, 'r-', linewidth=2, label=f'최소제곱법: y={w_opt:.4f}x+{b_opt:.2f}')

    # Gradient Descent
    y_gd = w_gd * x_line + b_gd
    ax1.plot(x_line, y_gd, 'g--', linewidth=2, label=f'GD: y={w_gd:.4f}x+{b_gd:.2f}')

    ax1.set_xlabel('조회수 (views)', fontsize=12)
    ax1.set_ylabel('수익 (만원)', fontsize=12)
    ax1.set_title('선형 회귀 결과 비교', fontsize=14)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # 2. Loss 감소 과정
    ax2 = axes[1]
    ax2.plot(loss_history, linewidth=2, color='blue')
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Loss (MSE)', fontsize=12)
    ax2.set_title('Gradient Descent: Loss 감소', fontsize=14)
    ax2.grid(True, alpha=0.3)

    # 3. 예측 오차
    ax3 = axes[2]
    y_pred_opt = w_opt * x + b_opt
    y_pred_gd = w_gd * x + b_gd

    errors_opt = np.abs(y - y_pred_opt)
    errors_gd = np.abs(y - y_pred_gd)

    width = 0.35
    x_pos = np.arange(len(x))

    ax3.bar(x_pos - width/2, errors_opt, width, label='최소제곱법', alpha=0.8)
    ax3.bar(x_pos + width/2, errors_gd, width, label='Gradient Descent', alpha=0.8)

    ax3.set_xlabel('데이터 인덱스', fontsize=12)
    ax3.set_ylabel('절대 오차', fontsize=12)
    ax3.set_title('예측 오차 비교', fontsize=14)
    ax3.set_xticks(x_pos)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('../assets/linear_regression_result.png', dpi=300, bbox_inches='tight')
    print(f"   ✅ 그래프 저장: ../assets/linear_regression_result.png")
    plt.show()


if __name__ == "__main__":
    main()
