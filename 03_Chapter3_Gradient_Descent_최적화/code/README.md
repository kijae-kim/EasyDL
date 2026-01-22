# Chapter 3: 역전파 시각화 코드

## 개요

이 폴더에는 **순전파(Forward Propagation)**와 **역전파(Back Propagation)**의 작동 원리를 시각적으로 이해하기 위한 코드가 포함되어 있습니다.

---

## 파일 구조

```
code/
├── README.md                         # 본 문서
└── backpropagation_visualization.py  # 역전파 시각화 애니메이션
```

---

## 실행 방법

### 1. 가상환경 활성화

```bash
cd /Users/gimgijae/Desktop/Paper/EasyDL
source activate_env.sh
```

### 2. 코드 실행

```bash
python 03_Chapter3_Gradient_Descent_최적화/code/backpropagation_visualization.py
```

### 3. 결과 확인

- 터미널에 순전파/역전파 계산 결과 출력
- matplotlib 창에서 애니메이션 자동 재생 (1.5초 간격)

---

## 기획 의도

### 문제 인식

역전파는 딥러닝의 핵심 알고리즘이지만, 수식만으로는 다음을 이해하기 어렵습니다:

| 어려운 점 | 설명 |
|-----------|------|
| **흐름 파악** | 그라디언트가 어떤 순서로 전파되는지 |
| **연쇄법칙** | 각 노드에서 어떻게 미분이 곱해지는지 |
| **값의 변화** | 순전파 값과 역전파 그라디언트의 실제 크기 |

### 해결 방안

**계산 그래프 애니메이션**을 통해:

1. **순전파**: 입력 → 출력 방향으로 값이 전파되는 과정을 단계별로 시각화
2. **역전파**: 출력 → 입력 방향으로 그라디언트가 전파되는 과정을 시각화
3. **실시간 값 표시**: 각 노드의 현재 값/그라디언트를 숫자로 표시

---

## 코드 구조

### 클래스 구성

```
backpropagation_visualization.py
│
├── SimpleNetwork            # 2층 신경망 구현
│   ├── forward()           # 순전파 (중간값 저장)
│   ├── compute_loss()      # MSE 손실 계산
│   └── backward()          # 역전파 (그라디언트 계산)
│
└── ComputationGraphVisualizer  # 시각화 담당
    ├── draw_node()         # 노드 그리기
    ├── draw_edge()         # 엣지 그리기
    ├── draw_frame()        # 프레임 렌더링
    └── run()               # 애니메이션 실행
```

### 네트워크 구조

```
입력층 (2)  →  히든층 (1)  →  출력층 (1)
   x₁ ─┐
       ├─→ [×W₁] → [+b₁] → [σ] → h → [×W₂] → [+b₂] → ŷ → [Loss] → L
   x₂ ─┘
```

### 사용된 수식

**순전파:**
- $z_1 = x \cdot W_1 + b_1$
- $h = \sigma(z_1)$ (sigmoid)
- $\hat{y} = h \cdot W_2 + b_2$
- $L = \frac{1}{2}(\hat{y} - y)^2$

**역전파:**
- $\frac{\partial L}{\partial \hat{y}} = \hat{y} - y$
- $\frac{\partial L}{\partial W_2} = h \cdot \frac{\partial L}{\partial \hat{y}}$
- $\frac{\partial L}{\partial h} = W_2 \cdot \frac{\partial L}{\partial \hat{y}}$
- $\frac{\partial L}{\partial z_1} = \frac{\partial L}{\partial h} \cdot \sigma'(z_1)$
- $\frac{\partial L}{\partial W_1} = x \cdot \frac{\partial L}{\partial z_1}$

---

## 실행 결과

### 터미널 출력 예시

```
==================================================
순전파/역전파 계산 테스트
==================================================
입력: x = [0.5 0.8]
정답: y = 1.0

[순전파 결과]
  z1 = 0.5900
  h  = 0.6434
  y^ = 0.6504
  L  = 0.0611

[역전파 결과 - 그라디언트]
  dL_dy_hat: [-0.3496]
  dL_dW2: [-0.2249]
  dL_dh: [-0.2448]
  dL_dz1: [-0.0562]
  dL_dW1: [-0.0281 -0.0449]
```

### 애니메이션 단계

**순전파 (9단계):**

| 단계 | 활성 노드 | 설명 |
|------|-----------|------|
| 1 | x₁, x₂ | 입력값 설정 |
| 2 | x₁, x₂, W₁ | 가중치 곱셈 |
| 3 | z₁, b₁ | 편향 덧셈 |
| 4 | σ | 활성화 함수 적용 |
| 5 | h | 히든층 출력 |
| 6 | h, W₂ | 가중치 곱셈 |
| 7 | z₂, b₂ | 편향 덧셈 |
| 8 | ŷ | 예측값 출력 |
| 9 | ŷ, y, L | 손실 계산 |

**역전파 (5단계):**

| 단계 | 활성 노드 | 계산되는 그라디언트 |
|------|-----------|---------------------|
| 1 | L | dL/dŷ |
| 2 | ŷ, W₂ | dL/dW₂ |
| 3 | h | dL/dh |
| 4 | σ, z₁ | dL/dz₁ |
| 5 | W₁ | dL/dW₁ |

### 시각화 요소

| 색상 | 의미 |
|------|------|
| 청록색 (#4ecdc4) | 순전파 활성 노드 |
| 빨간색 (#ff6b6b) | 역전파 활성 노드 |
| 회색 (#ecf0f1) | 비활성 노드 |
| 파란색 화살표 | 순전파 방향 |
| 빨간색 화살표 | 역전파 방향 |

---

## 향후 개선 방향

### 1. 기능 확장

| 개선 사항 | 설명 |
|-----------|------|
| **다층 네트워크** | 3층 이상의 네트워크로 확장하여 기울기 소실 현상 시각화 |
| **다양한 활성화 함수** | ReLU, Tanh 등 선택 가능하도록 확장 |
| **인터랙티브 모드** | 사용자가 입력값/가중치를 조절하며 실시간 확인 |
| **GIF 저장** | 애니메이션을 GIF로 저장하여 노트에 첨부 |

### 2. 학습 연계

| 연계 내용 | 관련 챕터 |
|-----------|-----------|
| **기울기 소실 시각화** | Chapter 6 - 딥러닝 문제와 해결방안 |
| **다양한 옵티마이저** | Chapter 3 - SGD, Adam 등 비교 |
| **배치 학습** | Chapter 3 - Mini-batch GD 시각화 |

### 3. 코드 개선

```python
# TODO: 추가 구현 예정
- [ ] 다층 네트워크 지원 (n층)
- [ ] 활성화 함수 선택 옵션
- [ ] Jupyter Notebook 위젯 버전
- [ ] 학습 과정 전체 시각화 (여러 epoch)
```

---

## 참고 자료

- **관련 노트**: `03_Chapter3_Gradient_Descent_최적화/notes/역전파.md`
- **교재**: Easy Deep Learning (혁펜하임) Chapter 3
- **강의**: [YouTube 링크 - Chapter 3]

---

## 문제 해결

### 한글이 깨지는 경우

macOS에서 폰트 문제가 발생하면:

```python
# 코드 상단에서 폰트 설정 변경
plt.rcParams['font.family'] = ['Apple SD Gothic Neo', 'AppleGothic']
```

### 애니메이션이 느린 경우

`interval` 값을 조절:

```python
# ComputationGraphVisualizer.run() 메서드에서
anim = FuncAnimation(..., interval=1000, ...)  # 1초 간격
```

---

*마지막 업데이트: 2026-01-22*
