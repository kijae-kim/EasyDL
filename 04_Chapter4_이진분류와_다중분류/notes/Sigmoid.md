
BCE Loss 와 MSE Loss의 차이

Sigmoid
전구간 미분 가능 Gradient Descent 가능
좀 더 부드러운 분류 가능
확률(어느 정도)로 해석 가능
가장 합리적인 분류경계선 확인

로지스틱 회귀 분석

4.4 딥러닝과 MLE
BCE Loss 와 MLE Loss는 엇뜻 보기에는 전혀 관련이 없는 손실함수처럼 보인다.
하지만, Likelihood라는 공통점을 지니고 있다.
Loss를 최소화하는 파라미터를 찾는 딥러닝의 학습 과정이 사실 MLE(Maximum Likelihho Estimation)과 같다는 것을 의미하는 것이다.

*MLE?

NLL - 가우시안, 베르누이, 라플라스, 카테고리
AI 학습은 w를 추정하기 위한 MLE를 수행하는 과정이다.

Softmax
Softmax 회귀