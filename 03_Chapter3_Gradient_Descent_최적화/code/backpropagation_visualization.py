"""
역전파 시각화: 계산 그래프 애니메이션
=====================================
순전파와 역전파 과정을 단계별로 시각화합니다.

실행 방법:
    python 03_Chapter3_Gradient_Descent_최적화/code/backpropagation_visualization.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from matplotlib import rcParams

# 한글 폰트 설정 (macOS)
plt.rcParams['font.family'] = ['Apple SD Gothic Neo', 'AppleGothic', 'Malgun Gothic', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


class SimpleNetwork:
    """간단한 2층 신경망 (입력 → 히든 → 출력)"""

    def __init__(self):
        # 고정된 가중치와 편향 (시각화를 위해 간단한 값 사용)
        np.random.seed(42)
        self.W1 = np.array([[0.5], [0.3]])  # (2, 1) - 입력 2개 → 히든 1개
        self.b1 = np.array([0.1])
        self.W2 = np.array([[0.7]])          # (1, 1) - 히든 1개 → 출력 1개
        self.b2 = np.array([0.2])

        # 중간값 저장
        self.cache = {}

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        s = self.sigmoid(x)
        return s * (1 - s)

    def forward(self, x):
        """순전파: 각 단계의 값을 저장"""
        self.cache['x'] = x

        # 입력층 → 히든층
        self.cache['z1'] = np.dot(x, self.W1) + self.b1
        self.cache['h'] = self.sigmoid(self.cache['z1'])

        # 히든층 → 출력층
        self.cache['z2'] = np.dot(self.cache['h'], self.W2) + self.b2
        self.cache['y_hat'] = self.cache['z2']  # 회귀이므로 선형 출력

        return self.cache['y_hat']

    def compute_loss(self, y_true):
        """MSE 손실 계산"""
        self.cache['y_true'] = y_true
        self.cache['loss'] = 0.5 * (self.cache['y_hat'] - y_true) ** 2
        return self.cache['loss']

    def backward(self):
        """역전파: 각 단계의 그라디언트 계산"""
        grads = {}

        # 손실 → 출력
        grads['dL_dy_hat'] = self.cache['y_hat'] - self.cache['y_true']

        # 출력층 가중치
        grads['dL_dW2'] = self.cache['h'] * grads['dL_dy_hat']
        grads['dL_db2'] = grads['dL_dy_hat']

        # 히든층으로 전파
        grads['dL_dh'] = self.W2 * grads['dL_dy_hat']
        grads['dL_dz1'] = grads['dL_dh'] * self.sigmoid_derivative(self.cache['z1'])

        # 히든층 가중치
        grads['dL_dW1'] = np.outer(self.cache['x'], grads['dL_dz1'])
        grads['dL_db1'] = grads['dL_dz1']

        self.cache['grads'] = grads
        return grads


class ComputationGraphVisualizer:
    """계산 그래프 시각화 클래스"""

    def __init__(self, network):
        self.net = network
        self.fig, self.ax = plt.subplots(1, 1, figsize=(14, 8))

        # 노드 위치 정의
        self.node_positions = {
            'x1': (1, 6), 'x2': (1, 4),
            'W1': (2.5, 5), 'b1': (3.5, 6.5),
            'z1': (4, 5), 'sigmoid': (5.5, 5), 'h': (7, 5),
            'W2': (8.5, 5), 'b2': (9.5, 6.5),
            'z2': (10, 5), 'y_hat': (11.5, 5),
            'y_true': (11.5, 3), 'Loss': (13, 5)
        }

        # 엣지 정의 (from, to)
        self.edges = [
            ('x1', 'W1'), ('x2', 'W1'), ('W1', 'z1'), ('b1', 'z1'),
            ('z1', 'sigmoid'), ('sigmoid', 'h'),
            ('h', 'W2'), ('W2', 'z2'), ('b2', 'z2'),
            ('z2', 'y_hat'), ('y_hat', 'Loss'), ('y_true', 'Loss')
        ]

        # 애니메이션 단계 정의
        self.forward_steps = [
            {'active': ['x1', 'x2'], 'desc': '입력값 설정'},
            {'active': ['x1', 'x2', 'W1'], 'desc': '가중치 곱셈: x * W1'},
            {'active': ['z1', 'b1'], 'desc': '편향 덧셈: x*W1 + b1 = z1'},
            {'active': ['sigmoid'], 'desc': '활성화 함수: sigmoid(z1)'},
            {'active': ['h'], 'desc': '히든층 출력: h = sigmoid(z1)'},
            {'active': ['h', 'W2'], 'desc': '가중치 곱셈: h * W2'},
            {'active': ['z2', 'b2'], 'desc': '편향 덧셈: h*W2 + b2 = z2'},
            {'active': ['y_hat'], 'desc': '예측값: y_hat = z2'},
            {'active': ['y_hat', 'y_true', 'Loss'], 'desc': '손실 계산: L = 0.5*(y_hat - y)^2'},
        ]

        self.backward_steps = [
            {'active': ['Loss'], 'desc': '역전파 시작: dL/dy_hat = (y_hat - y)', 'grad': 'dL_dy_hat'},
            {'active': ['y_hat', 'W2'], 'desc': 'dL/dW2 = h * dL/dy_hat', 'grad': 'dL_dW2'},
            {'active': ['h'], 'desc': 'dL/dh = W2 * dL/dy_hat', 'grad': 'dL_dh'},
            {'active': ['sigmoid', 'z1'], 'desc': "dL/dz1 = dL/dh * sigmoid'(z1)", 'grad': 'dL_dz1'},
            {'active': ['W1'], 'desc': 'dL/dW1 = x * dL/dz1', 'grad': 'dL_dW1'},
        ]

        self.current_step = 0
        self.total_steps = len(self.forward_steps) + len(self.backward_steps) + 2  # +2 for pauses
        self.phase = 'forward'

    def draw_node(self, name, pos, active=False, value=None, is_backward=False):
        """노드 그리기"""
        x, y = pos

        # 색상 결정
        if active and is_backward:
            color = '#ff6b6b'  # 역전파: 빨간색
            edge_color = '#c0392b'
        elif active:
            color = '#4ecdc4'  # 순전파: 청록색
            edge_color = '#16a085'
        else:
            color = '#ecf0f1'  # 비활성: 회색
            edge_color = '#bdc3c7'

        # 노드 모양 결정
        if name in ['sigmoid']:
            # 활성화 함수는 다이아몬드
            diamond = patches.RegularPolygon((x, y), numVertices=4, radius=0.4,
                                            facecolor=color, edgecolor=edge_color, linewidth=2)
            self.ax.add_patch(diamond)
        elif name in ['Loss']:
            # 손실은 원
            circle = patches.Circle((x, y), 0.4, facecolor=color, edgecolor=edge_color, linewidth=2)
            self.ax.add_patch(circle)
        else:
            # 나머지는 사각형
            rect = patches.FancyBboxPatch((x-0.4, y-0.3), 0.8, 0.6,
                                          boxstyle="round,pad=0.05",
                                          facecolor=color, edgecolor=edge_color, linewidth=2)
            self.ax.add_patch(rect)

        # 노드 이름
        display_names = {
            'x1': '$x_1$', 'x2': '$x_2$', 'W1': '$\\times W_1$', 'b1': '$+b_1$',
            'z1': '$z_1$', 'sigmoid': '$\\sigma$', 'h': '$h$',
            'W2': '$\\times W_2$', 'b2': '$+b_2$', 'z2': '$z_2$',
            'y_hat': '$\\hat{y}$', 'y_true': '$y$', 'Loss': '$L$'
        }
        self.ax.text(x, y, display_names.get(name, name), ha='center', va='center',
                    fontsize=11, fontweight='bold')

        # 값 표시
        if value is not None:
            self.ax.text(x, y-0.55, f'{value:.3f}', ha='center', va='top',
                        fontsize=9, color='#2c3e50')

    def draw_edge(self, from_node, to_node, active=False, is_backward=False):
        """엣지 그리기"""
        x1, y1 = self.node_positions[from_node]
        x2, y2 = self.node_positions[to_node]

        # 노드 크기만큼 오프셋
        dx = x2 - x1
        dy = y2 - y1
        dist = np.sqrt(dx**2 + dy**2)
        offset = 0.45

        x1_adj = x1 + offset * dx / dist
        y1_adj = y1 + offset * dy / dist
        x2_adj = x2 - offset * dx / dist
        y2_adj = y2 - offset * dy / dist

        # 색상 결정
        if active and is_backward:
            color = '#e74c3c'
            width = 2.5
        elif active:
            color = '#3498db'
            width = 2.5
        else:
            color = '#bdc3c7'
            width = 1

        self.ax.annotate('', xy=(x2_adj, y2_adj), xytext=(x1_adj, y1_adj),
                        arrowprops=dict(arrowstyle='->', color=color, lw=width))

    def get_node_value(self, name):
        """노드의 현재 값 반환"""
        cache = self.net.cache
        values = {
            'x1': cache.get('x', [0, 0])[0] if 'x' in cache else None,
            'x2': cache.get('x', [0, 0])[1] if 'x' in cache else None,
            'z1': cache.get('z1', [None])[0],
            'h': cache.get('h', [None])[0],
            'z2': cache.get('z2', [None])[0],
            'y_hat': cache.get('y_hat', [None])[0],
            'y_true': cache.get('y_true', None),
            'Loss': cache.get('loss', [None])[0] if 'loss' in cache else None,
        }
        return values.get(name)

    def get_grad_value(self, grad_name):
        """그라디언트 값 반환"""
        if 'grads' not in self.net.cache:
            return None
        grads = self.net.cache['grads']
        val = grads.get(grad_name)
        if val is not None:
            if hasattr(val, '__len__'):
                return val.flatten()[0]
            return val
        return None

    def draw_frame(self, step):
        """프레임 그리기"""
        self.ax.clear()
        self.ax.set_xlim(0, 14)
        self.ax.set_ylim(2, 8)
        self.ax.set_aspect('equal')
        self.ax.axis('off')

        # 단계 결정
        if step < len(self.forward_steps):
            self.phase = 'forward'
            step_info = self.forward_steps[step]
            active_nodes = step_info['active']
            description = step_info['desc']
            is_backward = False
        elif step == len(self.forward_steps):
            # 순전파 완료 pause
            self.phase = 'pause'
            active_nodes = []
            description = '순전파 완료! 역전파 시작...'
            is_backward = False
        else:
            self.phase = 'backward'
            backward_idx = step - len(self.forward_steps) - 1
            if backward_idx < len(self.backward_steps):
                step_info = self.backward_steps[backward_idx]
                active_nodes = step_info['active']
                description = step_info['desc']
                is_backward = True
            else:
                active_nodes = []
                description = '역전파 완료!'
                is_backward = True

        # 제목
        phase_text = '순전파 (Forward)' if self.phase == 'forward' else '역전파 (Backward)' if self.phase == 'backward' else ''
        phase_color = '#3498db' if self.phase == 'forward' else '#e74c3c' if self.phase == 'backward' else '#2c3e50'
        self.ax.text(7, 7.5, phase_text, ha='center', fontsize=16, fontweight='bold', color=phase_color)
        self.ax.text(7, 7.0, description, ha='center', fontsize=12, color='#2c3e50')

        # 엣지 그리기
        for from_node, to_node in self.edges:
            edge_active = (from_node in active_nodes and to_node in active_nodes)
            self.draw_edge(from_node, to_node, active=edge_active, is_backward=is_backward)

        # 노드 그리기
        for name, pos in self.node_positions.items():
            active = name in active_nodes
            value = self.get_node_value(name) if self.phase != 'pause' else self.get_node_value(name)
            self.draw_node(name, pos, active=active, value=value, is_backward=is_backward)

        # 그라디언트 정보 표시 (역전파 시)
        if self.phase == 'backward' and 'grads' in self.net.cache:
            grad_text = "현재 그라디언트:\n"
            grads = self.net.cache['grads']
            for key in ['dL_dy_hat', 'dL_dW2', 'dL_dh', 'dL_dz1', 'dL_dW1']:
                if key in grads:
                    val = grads[key]
                    if hasattr(val, '__len__'):
                        val = val.flatten()[0]
                    grad_text += f"  {key}: {val:.4f}\n"
            self.ax.text(0.5, 3.5, grad_text, fontsize=9, family='monospace',
                        verticalalignment='top', color='#c0392b')

        # 범례
        legend_y = 2.5
        self.ax.add_patch(patches.Rectangle((10, legend_y), 0.3, 0.2, facecolor='#4ecdc4'))
        self.ax.text(10.5, legend_y+0.1, '순전파', fontsize=9, va='center')
        self.ax.add_patch(patches.Rectangle((12, legend_y), 0.3, 0.2, facecolor='#ff6b6b'))
        self.ax.text(12.5, legend_y+0.1, '역전파', fontsize=9, va='center')

        return []

    def animate(self, frame):
        """애니메이션 프레임"""
        return self.draw_frame(frame)

    def run(self, x, y_true, save_path=None):
        """애니메이션 실행"""
        # 순전파 실행
        self.net.forward(x)
        self.net.compute_loss(y_true)
        self.net.backward()

        print("=" * 50)
        print("계산 그래프 애니메이션: 순전파 & 역전파")
        print("=" * 50)
        print(f"\n입력: x = {x}")
        print(f"정답: y = {y_true}")
        print(f"\n[순전파 결과]")
        print(f"  z1 = {self.net.cache['z1'][0]:.4f}")
        print(f"  h  = {self.net.cache['h'][0]:.4f}")
        print(f"  y^ = {self.net.cache['y_hat'][0]:.4f}")
        print(f"  L  = {self.net.cache['loss'][0]:.4f}")
        print(f"\n[역전파 결과 - 그라디언트]")
        for key, val in self.net.cache['grads'].items():
            if hasattr(val, '__len__'):
                print(f"  {key}: {val.flatten()}")
            else:
                print(f"  {key}: {val:.4f}")
        print("\n" + "=" * 50)
        print("애니메이션을 시작합니다... (창을 닫으면 종료)")
        print("=" * 50)

        # 애니메이션 생성
        anim = FuncAnimation(self.fig, self.animate, frames=self.total_steps,
                           interval=1500, repeat=True, blit=False)

        if save_path:
            anim.save(save_path, writer='pillow', fps=1)
            print(f"\n애니메이션 저장됨: {save_path}")

        plt.tight_layout()
        plt.show()

        return anim


def main():
    """메인 실행 함수"""
    # 네트워크 생성
    net = SimpleNetwork()

    # 입력 데이터
    x = np.array([0.5, 0.8])  # 입력
    y_true = 1.0              # 정답

    # 시각화 실행
    viz = ComputationGraphVisualizer(net)
    viz.run(x, y_true)


if __name__ == "__main__":
    main()
