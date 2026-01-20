---
chapter: Chapter 2
topic: "Adam 논문 요약"
paper_title: "Adam: A Method for Stochastic Optimization"
authors: "Diederik P. Kingma, Jimmy Ba"
publication: "ICLR 2015"
arxiv: "arXiv:1412.6980"
date: 2026-01-20
status: 완료
tags:
  - 딥러닝
  - EasyDL
  - 최적화
  - Adam
  - 논문요약
---

# Adam: A Method for Stochastic Optimization

> **논문 원문**: [arXiv:1412.6980](https://arxiv.org/abs/1412.6980)
> **저자**: Diederik P. Kingma, Jimmy Ba (2014)
> **인용 수**: 234,000+ (역대 가장 많이 인용된 ML 논문 중 하나)

---

## 핵심 아이디어

Adam(Adaptive Moment Estimation)은 **Momentum**과 **RMSProp**의 장점을 결합한 최적화 알고리즘이다.

| 구성 요소 | 역할 | 기여 알고리즘 |
|----------|------|--------------|
| 1차 모멘트 (m) | 그래디언트의 이동 평균 (방향성) | Momentum |
| 2차 모멘트 (v) | 그래디언트 제곱의 이동 평균 (스케일 조정) | RMSProp |
| 편향 보정 | 초기 학습 안정화 | Adam 고유 |

---

## 알고리즘 수식

### Step 1: 그래디언트 계산

시간 $t$에서 파라미터 $\theta$에 대한 손실 함수의 그래디언트를 계산한다:

$$g_t = \nabla_\theta L(\theta_{t-1})$$

### Step 2: 1차 모멘트 추정 (Momentum)

그래디언트의 지수 가중 이동 평균을 계산한다:

$$m_t = \beta_1 \cdot m_{t-1} + (1 - \beta_1) \cdot g_t$$

- **의미**: 과거 그래디언트의 방향성을 누적하여 이동 방향 결정
- **$\beta_1$**: 이전 모멘트의 영향력 (기본값 0.9)

### Step 3: 2차 모멘트 추정 (RMSProp)

그래디언트 제곱의 지수 가중 이동 평균을 계산한다:

$$v_t = \beta_2 \cdot v_{t-1} + (1 - \beta_2) \cdot g_t^2$$

- **의미**: 각 파라미터별 그래디언트의 크기(분산)를 추적
- **$\beta_2$**: 이전 2차 모멘트의 영향력 (기본값 0.999)

### Step 4: 편향 보정 (Bias Correction)

$m_t$와 $v_t$는 0으로 초기화되므로 학습 초기에 0으로 편향된다. 이를 보정한다:

$$\hat{m}_t = \frac{m_t}{1 - \beta_1^t}$$

$$\hat{v}_t = \frac{v_t}{1 - \beta_2^t}$$

- **왜 필요한가?**
  - $t=1$일 때, $m_1 = (1-\beta_1) \cdot g_1$ 로 실제 그래디언트보다 매우 작음
  - 보정 항 $\frac{1}{1-\beta_1^t}$가 초기에는 크고 $t \to \infty$에서 1에 수렴

### Step 5: 파라미터 업데이트

최종적으로 파라미터를 업데이트한다:

$$\theta_t = \theta_{t-1} - \alpha \cdot \frac{\hat{m}_t}{\sqrt{\hat{v}_t} + \epsilon}$$

- **$\alpha$**: 학습률 (기본값 0.001)
- **$\epsilon$**: 수치 안정성을 위한 작은 상수 (기본값 $10^{-8}$)

---

## 전체 알고리즘 의사코드

```
초기화: m₀ = 0, v₀ = 0, t = 0

반복 (수렴할 때까지):
    t = t + 1
    gₜ = ∇θL(θₜ₋₁)                          # 그래디언트 계산
    mₜ = β₁·mₜ₋₁ + (1-β₁)·gₜ                # 1차 모멘트 업데이트
    vₜ = β₂·vₜ₋₁ + (1-β₂)·gₜ²               # 2차 모멘트 업데이트
    m̂ₜ = mₜ / (1-β₁ᵗ)                       # 편향 보정
    v̂ₜ = vₜ / (1-β₂ᵗ)                       # 편향 보정
    θₜ = θₜ₋₁ - α·m̂ₜ / (√v̂ₜ + ε)           # 파라미터 업데이트
```

---

## 하이퍼파라미터 상세

| 파라미터 | 기본값 | 역할 | 조정 가이드 |
|---------|-------|------|-----------|
| $\alpha$ (학습률) | 0.001 | 스텝 크기 조절 | 발산 시 낮추고, 수렴이 느리면 높임 |
| $\beta_1$ | 0.9 | 1차 모멘트 감쇠율 | 노이즈가 많으면 높임 (0.95) |
| $\beta_2$ | 0.999 | 2차 모멘트 감쇠율 | 희소 그래디언트면 높임 (0.9999) |
| $\epsilon$ | $10^{-8}$ | 수치 안정성 | 거의 변경 불필요 |

### 하이퍼파라미터 직관적 이해

- **$\beta_1 = 0.9$**: 현재 그래디언트의 10%와 과거 모멘트의 90%를 사용
- **$\beta_2 = 0.999$**: 현재 그래디언트 제곱의 0.1%와 과거 2차 모멘트의 99.9%를 사용
- **편향 보정 효과**:
  - $t=1$: $\hat{m}_1 = m_1 / 0.1 = 10 \times m_1$ (10배 증폭)
  - $t=10$: $\hat{m}_{10} = m_{10} / 0.65 \approx 1.5 \times m_{10}$
  - $t=100$: 보정 효과 거의 없음 (1에 수렴)

---

## Momentum, RMSProp과의 비교

### Momentum

$$v_t = \gamma v_{t-1} + \alpha \nabla_\theta L$$
$$\theta_t = \theta_{t-1} - v_t$$

- 그래디언트를 누적하여 **방향 안정성** 확보
- 지그재그 움직임 감소
- 모든 파라미터에 **동일한 학습률** 적용

### RMSProp

$$v_t = \beta v_{t-1} + (1-\beta) g_t^2$$
$$\theta_t = \theta_{t-1} - \frac{\alpha}{\sqrt{v_t} + \epsilon} g_t$$

- 각 파라미터별 **적응적 학습률**
- 가파른 방향은 작게, 완만한 방향은 크게 이동
- 그래디언트 누적 없음 (방향성 없음)

### Adam = Momentum + RMSProp + 편향 보정

| 특성 | Momentum | RMSProp | Adam |
|-----|----------|---------|------|
| 방향 누적 | O | X | O |
| 적응적 학습률 | X | O | O |
| 편향 보정 | X | X | O |
| 희소 그래디언트 | 약함 | 강함 | 강함 |
| 초기 학습 안정성 | 보통 | 보통 | 높음 |

---

## AdaMax 변형

논문에서는 Adam의 변형인 **AdaMax**도 제안한다.

Adam의 2차 모멘트 $v_t$는 $L^2$ norm을 사용하지만, 이를 $L^\infty$ norm으로 일반화할 수 있다:

$$u_t = \max(\beta_2 \cdot u_{t-1}, |g_t|)$$

$$\theta_t = \theta_{t-1} - \frac{\alpha}{u_t} \hat{m}_t$$

- **장점**: $L^\infty$ norm은 편향 보정이 필요 없음
- **활용**: 임베딩 학습 등 특정 상황에서 유용

---

## 수렴 특성

### 이론적 보장

논문에서는 온라인 볼록 최적화 프레임워크에서 Adam의 **regret bound**를 증명:

$$R(T) = O(\sqrt{T})$$

- SGD와 동일한 수렴 속도
- 실제로는 적응적 학습률로 인해 더 빠르게 수렴하는 경우가 많음

### 실제 주의사항

- **일부 경우 최적해 미수렴**: SGD가 더 나은 일반화 성능을 보이기도 함
- **Learning Rate Warmup**: 큰 배치 사이즈에서는 초기 학습률을 점진적으로 증가시키는 것이 효과적
- **Weight Decay 분리**: AdamW에서는 가중치 감쇠를 그래디언트 업데이트와 분리

---

## 구현 예시

### PyTorch

```python
import torch.optim as optim

optimizer = optim.Adam(
    model.parameters(),
    lr=0.001,           # alpha
    betas=(0.9, 0.999), # (beta1, beta2)
    eps=1e-8            # epsilon
)
```

### TensorFlow/Keras

```python
from tensorflow.keras.optimizers import Adam

optimizer = Adam(
    learning_rate=0.001,
    beta_1=0.9,
    beta_2=0.999,
    epsilon=1e-8
)
```

---

## 핵심 정리

1. **Adam = Momentum + RMSProp + 편향 보정**
2. **1차 모멘트**: 방향성 (어디로 갈지)
3. **2차 모멘트**: 스케일 (얼마나 갈지)
4. **편향 보정**: 초기 학습 안정화
5. **기본 하이퍼파라미터**: $\alpha=0.001$, $\beta_1=0.9$, $\beta_2=0.999$, $\epsilon=10^{-8}$

---

## 참고 자료

- [원 논문 (arXiv)](https://arxiv.org/abs/1412.6980)
- [Cornell Optimization Wiki](https://optimization.cbe.cornell.edu/index.php?title=Adam)
- [GeeksforGeeks - Adam Optimizer](https://www.geeksforgeeks.org/deep-learning/adam-optimizer/)
- [Dive into Deep Learning - Adam](http://d2l.ai/chapter_optimization/adam.html)

---

## 관련 노트

- [[선형회귀]] - 경사하강법 및 최적화 알고리즘 개요
- [[인공신경망]] - 신경망 기초
