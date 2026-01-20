"""
최적화 알고리즘 비교 시각화 실습
=====================================

SGD, Momentum, RMSProp, Adam의 수렴 과정을 시각화하여 비교합니다.

실행 방법:
    source activate_env.sh
    python 02_Chapter2_인공신경망/code/optimizer_comparison.py
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.animation as animation
from typing import Callable, Tuple, List, Dict
import os

# 한글 폰트 설정 (macOS)
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False


# =============================================================================
# 1. 손실 함수 정의
# =============================================================================

def beale_function(x: float, y: float) -> float:
    """
    Beale 함수: 비대칭적이고 복잡한 지형을 가진 테스트 함수
    전역 최소점: (3, 0.5)에서 f = 0
    """
    term1 = (1.5 - x + x * y) ** 2
    term2 = (2.25 - x + x * y ** 2) ** 2
    term3 = (2.625 - x + x * y ** 3) ** 2
    return term1 + term2 + term3


def beale_gradient(x: float, y: float) -> Tuple[float, float]:
    """Beale 함수의 그래디언트"""
    # df/dx
    dx = (2 * (1.5 - x + x * y) * (-1 + y) +
          2 * (2.25 - x + x * y ** 2) * (-1 + y ** 2) +
          2 * (2.625 - x + x * y ** 3) * (-1 + y ** 3))

    # df/dy
    dy = (2 * (1.5 - x + x * y) * x +
          2 * (2.25 - x + x * y ** 2) * (2 * x * y) +
          2 * (2.625 - x + x * y ** 3) * (3 * x * y ** 2))

    return dx, dy


def quadratic_function(x: float, y: float) -> float:
    """
    타원형 2차 함수: 축별로 곡률이 다른 간단한 함수
    전역 최소점: (0, 0)에서 f = 0
    x축은 완만하고 y축은 가파름 -> 지그재그 현상 발생
    """
    return 0.1 * x ** 2 + 2 * y ** 2


def quadratic_gradient(x: float, y: float) -> Tuple[float, float]:
    """타원형 2차 함수의 그래디언트"""
    return 0.2 * x, 4 * y


# =============================================================================
# 2. 최적화 알고리즘 직접 구현
# =============================================================================

class Optimizer:
    """최적화 알고리즘 기본 클래스"""

    def __init__(self, lr: float = 0.01):
        self.lr = lr
        self.name = "Base"

    def step(self, x: float, y: float, dx: float, dy: float) -> Tuple[float, float]:
        raise NotImplementedError


class SGD(Optimizer):
    """확률적 경사하강법"""

    def __init__(self, lr: float = 0.01):
        super().__init__(lr)
        self.name = "SGD"

    def step(self, x: float, y: float, dx: float, dy: float) -> Tuple[float, float]:
        x_new = x - self.lr * dx
        y_new = y - self.lr * dy
        return x_new, y_new


class MomentumSGD(Optimizer):
    """모멘텀 SGD"""

    def __init__(self, lr: float = 0.01, momentum: float = 0.9):
        super().__init__(lr)
        self.momentum = momentum
        self.vx = 0.0
        self.vy = 0.0
        self.name = f"Momentum (γ={momentum})"

    def step(self, x: float, y: float, dx: float, dy: float) -> Tuple[float, float]:
        self.vx = self.momentum * self.vx + self.lr * dx
        self.vy = self.momentum * self.vy + self.lr * dy
        x_new = x - self.vx
        y_new = y - self.vy
        return x_new, y_new


class RMSProp(Optimizer):
    """RMSProp"""

    def __init__(self, lr: float = 0.01, beta: float = 0.9, eps: float = 1e-8):
        super().__init__(lr)
        self.beta = beta
        self.eps = eps
        self.vx = 0.0
        self.vy = 0.0
        self.name = f"RMSProp (β={beta})"

    def step(self, x: float, y: float, dx: float, dy: float) -> Tuple[float, float]:
        self.vx = self.beta * self.vx + (1 - self.beta) * dx ** 2
        self.vy = self.beta * self.vy + (1 - self.beta) * dy ** 2
        x_new = x - self.lr * dx / (np.sqrt(self.vx) + self.eps)
        y_new = y - self.lr * dy / (np.sqrt(self.vy) + self.eps)
        return x_new, y_new


class Adam(Optimizer):
    """Adam (Adaptive Moment Estimation)"""

    def __init__(self, lr: float = 0.01, beta1: float = 0.9,
                 beta2: float = 0.999, eps: float = 1e-8):
        super().__init__(lr)
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.mx = 0.0  # 1차 모멘트
        self.my = 0.0
        self.vx = 0.0  # 2차 모멘트
        self.vy = 0.0
        self.t = 0     # 타임스텝 (편향 보정용)
        self.name = f"Adam (β1={beta1}, β2={beta2})"

    def step(self, x: float, y: float, dx: float, dy: float) -> Tuple[float, float]:
        self.t += 1

        # 1차 모멘트 업데이트 (Momentum)
        self.mx = self.beta1 * self.mx + (1 - self.beta1) * dx
        self.my = self.beta1 * self.my + (1 - self.beta1) * dy

        # 2차 모멘트 업데이트 (RMSProp)
        self.vx = self.beta2 * self.vx + (1 - self.beta2) * dx ** 2
        self.vy = self.beta2 * self.vy + (1 - self.beta2) * dy ** 2

        # 편향 보정
        mx_hat = self.mx / (1 - self.beta1 ** self.t)
        my_hat = self.my / (1 - self.beta1 ** self.t)
        vx_hat = self.vx / (1 - self.beta2 ** self.t)
        vy_hat = self.vy / (1 - self.beta2 ** self.t)

        # 파라미터 업데이트
        x_new = x - self.lr * mx_hat / (np.sqrt(vx_hat) + self.eps)
        y_new = y - self.lr * my_hat / (np.sqrt(vy_hat) + self.eps)

        return x_new, y_new


# =============================================================================
# 3. 최적화 경로 추적
# =============================================================================

def optimize(optimizer: Optimizer,
             loss_fn: Callable,
             grad_fn: Callable,
             x0: float, y0: float,
             n_steps: int = 100) -> Dict:
    """
    주어진 최적화 알고리즘으로 손실 함수를 최적화하고 경로를 기록
    """
    x, y = x0, y0
    history = {
        'x': [x],
        'y': [y],
        'loss': [loss_fn(x, y)]
    }

    for _ in range(n_steps):
        dx, dy = grad_fn(x, y)
        x, y = optimizer.step(x, y, dx, dy)

        # 발산 방지
        x = np.clip(x, -10, 10)
        y = np.clip(y, -10, 10)

        history['x'].append(x)
        history['y'].append(y)
        history['loss'].append(loss_fn(x, y))

    return history


# =============================================================================
# 4. 시각화 함수
# =============================================================================

def plot_loss_surface(ax, loss_fn: Callable,
                      xlim: Tuple[float, float] = (-5, 5),
                      ylim: Tuple[float, float] = (-5, 5),
                      levels: int = 50):
    """손실 함수의 등고선을 그립니다"""
    x = np.linspace(xlim[0], xlim[1], 200)
    y = np.linspace(ylim[0], ylim[1], 200)
    X, Y = np.meshgrid(x, y)
    Z = np.vectorize(loss_fn)(X, Y)

    # 로그 스케일로 등고선 표시 (값의 범위가 클 때 유용)
    Z = np.clip(Z, 1e-10, 1e10)  # 음수/0 방지

    contour = ax.contour(X, Y, Z, levels=levels, cmap='viridis', alpha=0.6)
    ax.contourf(X, Y, Z, levels=levels, cmap='viridis', alpha=0.3)

    return contour


def plot_optimization_paths(histories: Dict[str, Dict],
                            loss_fn: Callable,
                            title: str = "최적화 알고리즘 비교",
                            xlim: Tuple[float, float] = (-5, 5),
                            ylim: Tuple[float, float] = (-5, 5),
                            save_path: str = None):
    """모든 최적화 알고리즘의 경로를 하나의 그래프에 시각화"""

    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']

    # 왼쪽: 2D Loss Surface + 경로
    ax1 = axes[0]
    plot_loss_surface(ax1, loss_fn, xlim, ylim)

    for (name, history), color in zip(histories.items(), colors):
        ax1.plot(history['x'], history['y'],
                 color=color, linewidth=2, label=name, alpha=0.8)
        ax1.scatter(history['x'][0], history['y'][0],
                    color=color, s=100, marker='o', edgecolors='white', zorder=5)
        ax1.scatter(history['x'][-1], history['y'][-1],
                    color=color, s=100, marker='*', edgecolors='white', zorder=5)

    ax1.set_xlabel('x', fontsize=12)
    ax1.set_ylabel('y', fontsize=12)
    ax1.set_title('2D Loss Surface에서의 최적화 경로', fontsize=14)
    ax1.legend(loc='upper right')
    ax1.set_xlim(xlim)
    ax1.set_ylim(ylim)
    ax1.grid(True, alpha=0.3)

    # 오른쪽: Loss 곡선
    ax2 = axes[1]

    for (name, history), color in zip(histories.items(), colors):
        ax2.plot(history['loss'], color=color, linewidth=2, label=name)

    ax2.set_xlabel('Step', fontsize=12)
    ax2.set_ylabel('Loss', fontsize=12)
    ax2.set_title('학습 곡선 (Loss vs Step)', fontsize=14)
    ax2.legend(loc='upper right')
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3)

    plt.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"그래프 저장: {save_path}")

    plt.show()


def create_animation(histories: Dict[str, Dict],
                     loss_fn: Callable,
                     xlim: Tuple[float, float] = (-5, 5),
                     ylim: Tuple[float, float] = (-5, 5),
                     save_path: str = None):
    """최적화 과정 애니메이션 생성"""

    fig, ax = plt.subplots(figsize=(10, 8))

    colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']

    # 등고선 배경
    plot_loss_surface(ax, loss_fn, xlim, ylim)

    # 경로 라인 초기화
    lines = []
    points = []
    names = list(histories.keys())

    for color in colors[:len(names)]:
        line, = ax.plot([], [], color=color, linewidth=2, alpha=0.8)
        point, = ax.plot([], [], 'o', color=color, markersize=10,
                         markeredgecolor='white', markeredgewidth=2)
        lines.append(line)
        points.append(point)

    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('y', fontsize=12)
    ax.set_title('최적화 알고리즘 수렴 과정', fontsize=14)
    ax.legend(lines, names, loc='upper right')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    # 스텝 카운터
    step_text = ax.text(0.02, 0.98, '', transform=ax.transAxes,
                        fontsize=12, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    def init():
        for line, point in zip(lines, points):
            line.set_data([], [])
            point.set_data([], [])
        step_text.set_text('')
        return lines + points + [step_text]

    def animate(frame):
        for i, (name, history) in enumerate(histories.items()):
            x_data = history['x'][:frame + 1]
            y_data = history['y'][:frame + 1]
            lines[i].set_data(x_data, y_data)
            if frame < len(history['x']):
                points[i].set_data([history['x'][frame]], [history['y'][frame]])

        step_text.set_text(f'Step: {frame}')
        return lines + points + [step_text]

    n_frames = max(len(h['x']) for h in histories.values())
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=n_frames, interval=50, blit=True)

    if save_path:
        anim.save(save_path, writer='pillow', fps=20)
        print(f"애니메이션 저장: {save_path}")

    plt.show()
    return anim


# =============================================================================
# 5. 메인 실행
# =============================================================================

def run_quadratic_experiment():
    """실험 1: 타원형 2차 함수 (지그재그 현상 관찰)"""

    print("=" * 60)
    print("실험 1: 타원형 2차 함수")
    print("=" * 60)
    print("특징: x축은 완만하고 y축은 가파름 → 지그재그 현상 발생")
    print("최소점: (0, 0)")
    print()

    # 시작점
    x0, y0 = -4.0, 3.0
    n_steps = 100

    # 각 최적화 알고리즘 설정
    optimizers = {
        'SGD': SGD(lr=0.1),
        'Momentum': MomentumSGD(lr=0.1, momentum=0.9),
        'RMSProp': RMSProp(lr=0.5, beta=0.9),
        'Adam': Adam(lr=0.5, beta1=0.9, beta2=0.999)
    }

    # 최적화 실행
    histories = {}
    for name, optimizer in optimizers.items():
        history = optimize(optimizer, quadratic_function, quadratic_gradient,
                           x0, y0, n_steps)
        histories[name] = history

        final_loss = history['loss'][-1]
        final_x, final_y = history['x'][-1], history['y'][-1]
        print(f"{name:12s} | 최종 위치: ({final_x:+.4f}, {final_y:+.4f}) | "
              f"최종 Loss: {final_loss:.6f}")

    print()

    # 시각화
    assets_dir = "02_Chapter2_인공신경망/assets"
    os.makedirs(assets_dir, exist_ok=True)

    plot_optimization_paths(
        histories,
        quadratic_function,
        title="타원형 2차 함수에서의 최적화 알고리즘 비교",
        xlim=(-5, 5),
        ylim=(-4, 4),
        save_path=os.path.join(assets_dir, "optimizer_comparison_quadratic.png")
    )

    return histories


def run_beale_experiment():
    """실험 2: Beale 함수 (복잡한 지형)"""

    print("=" * 60)
    print("실험 2: Beale 함수")
    print("=" * 60)
    print("특징: 비대칭적이고 복잡한 지형")
    print("최소점: (3, 0.5)")
    print()

    # 시작점
    x0, y0 = -2.0, 2.0
    n_steps = 200

    # 각 최적화 알고리즘 설정 (Beale 함수는 더 작은 learning rate 필요)
    optimizers = {
        'SGD': SGD(lr=0.0001),
        'Momentum': MomentumSGD(lr=0.0001, momentum=0.9),
        'RMSProp': RMSProp(lr=0.01, beta=0.9),
        'Adam': Adam(lr=0.1, beta1=0.9, beta2=0.999)
    }

    # 최적화 실행
    histories = {}
    for name, optimizer in optimizers.items():
        history = optimize(optimizer, beale_function, beale_gradient,
                           x0, y0, n_steps)
        histories[name] = history

        final_loss = history['loss'][-1]
        final_x, final_y = history['x'][-1], history['y'][-1]
        print(f"{name:12s} | 최종 위치: ({final_x:+.4f}, {final_y:+.4f}) | "
              f"최종 Loss: {final_loss:.6f}")

    print()

    # 시각화
    assets_dir = "02_Chapter2_인공신경망/assets"
    os.makedirs(assets_dir, exist_ok=True)

    plot_optimization_paths(
        histories,
        beale_function,
        title="Beale 함수에서의 최적화 알고리즘 비교",
        xlim=(-4.5, 4.5),
        ylim=(-3, 3),
        save_path=os.path.join(assets_dir, "optimizer_comparison_beale.png")
    )

    return histories


def print_summary():
    """실험 결과 요약"""
    print()
    print("=" * 60)
    print("실험 결과 요약")
    print("=" * 60)
    print("""
1. SGD
   - 가장 단순하지만 느림
   - 타원형 함수에서 심한 지그재그 현상
   - 복잡한 함수에서 쉽게 갇힘

2. Momentum
   - 지그재그 현상 완화
   - 관성으로 인해 최저점 근처에서 진동할 수 있음
   - SGD보다 빠른 수렴

3. RMSProp
   - 축별 적응적 학습률
   - 가파른 축에서 조심스럽게, 완만한 축에서 과감하게 이동
   - 지그재그 현상 크게 감소

4. Adam
   - Momentum + RMSProp + 편향 보정
   - 대부분의 상황에서 가장 안정적
   - 하이퍼파라미터 튜닝이 적게 필요
""")


if __name__ == "__main__":
    # 실험 1: 타원형 2차 함수
    histories1 = run_quadratic_experiment()

    # 실험 2: Beale 함수
    histories2 = run_beale_experiment()

    # 결과 요약
    print_summary()

    print("\n그래프가 02_Chapter2_인공신경망/assets/ 폴더에 저장되었습니다.")
