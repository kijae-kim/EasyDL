# 🚀 Easy Deep Learning 학습 프로젝트

> AI 엔지니어를 목표로 딥러닝 기초부터 체계적으로 학습하는 프로젝트

---

## 📚 학습 자료

- **교재**: 혁펜하임의 "Easy Deep Learning"
- **강의**: [YouTube 재생목록](https://www.youtube.com/playlist?list=PL_iJu012NOxdw1jc3KEo8Mq5oD5SXKhLu)

---

## 📂 프로젝트 구조

```
EasyDL/
├── 00_학습_가이드/              # 커리큘럼 및 진행 상황
├── 01_Chapter1_딥러닝_시작/
│   ├── notes/                  # 학습 노트 (Obsidian)
│   ├── code/                   # 실습 코드
│   └── assets/                 # 이미지, 그래프
├── 02_Chapter2_인공신경망/
├── 03_Chapter3_Gradient_Descent_최적화/
├── 04_Chapter4_이진분류와_다중분류/
├── 05_Chapter5_Universal_Approximation_Theorem/
├── 06_Chapter6_딥러닝_문제와_해결방안/
├── 07_Chapter7_CNN/
├── 08_Chapter8_RNN_Transformer/
├── 99_부록_수학_기초/
├── templates/                  # Obsidian 템플릿
└── scripts/                    # 자동화 스크립트
    ├── claude_logger.py       # Claude 대화 로깅
    └── tistory_poster.py      # 티스토리 자동 포스팅
```

---

## 📖 커리큘럼

### Chapter 1: 딥러닝 시작
- [퍼셉트론](https://youtu.be/13wbFxjz0d4)
- [신경망 기초](https://youtu.be/MNa62h4lacA)
- [텐서플로우 기초](https://youtu.be/ketAbA150R0)

### Chapter 2: 인공신경망 이해하기
- [인공신경망 이해하기](https://youtu.be/jBGKm7tUZiI)
- [인공신경망은 함수다](https://youtu.be/fbwmWEWMer0)
- [선형회귀](https://youtu.be/YjPV_sYKAbg)
- [경사하강법](https://youtu.be/YjPV_sYKAbg)

### Chapter 3: Gradient Descent 최적화
- [Gradient Descent의 치명적인 단점](https://youtu.be/tbxCzN3yrVU)
- [SGD](https://youtu.be/goBkxDdJX8Y)
- [mini-batch GD & 배치사이즈](https://youtu.be/WsdTEBlCQQ8)
- [모멘텀](https://youtu.be/gUPFazl5xW4)
- [RMSProp](https://youtu.be/3U527WpOquY)
- [Adam](https://youtu.be/wVBuPlBBbAE)

### Chapter 4-8
*(상세 내용은 각 Chapter 폴더 참조)*

---

## 🛠️ 기술 스택

- **언어**: Python 3.12.5
- **프레임워크**: TensorFlow 2.20.0, PyTorch 2.9.1
- **노트**: Obsidian (마크다운)
- **버전 관리**: Git/GitHub (자동 커밋)
- **AI 도우미**: Claude Code (VSCode 통합)
- **블로그**: 티스토리 (수동 포스팅)

---

## 🎯 학습 방법

1. 📹 강의 시청 및 교재 학습
2. 📝 Obsidian에 학습 노트 작성
3. 💻 VSCode + Claude Code로 코드 구현
4. 🤖 Claude와 대화하며 이해도 증진
5. 🔄 **자동 Git Commit & Push** (10분마다)
6. 📤 주간 단위로 티스토리 포스팅

---

## ⚡ 빠른 시작

### 1. 가상환경 활성화
```bash
cd /Users/gimgijae/Desktop/Paper/EasyDL
source activate_env.sh
```

### 2. Obsidian Vault 연결
- Obsidian 실행 → "Open folder as vault"
- `/Users/gimgijae/Desktop/Paper/EasyDL` 선택

### 3. GitHub 연결
```bash
./scripts/setup_github.sh
```

### 4. Obsidian Git 플러그인 설치
- `Settings` → `Community plugins` → "Git" 검색
- 자동 커밋 간격: 10분

**자세한 가이드**: [빠른_시작.md](00_학습_가이드/빠른_시작.md)

---

## 🔄 자동화 기능

### Git 자동 커밋
- ✅ **Obsidian Git 플러그인**: 10분마다 자동 커밋/푸시
- ✅ **수동 스크립트**: `./scripts/auto_commit.sh`
- ✅ **변경사항 추적**: 노트/코드/자료 자동 분류

### 학습 워크플로우
```
Obsidian 노트 작성
   ↓ (자동)
Git 커밋 (10분마다)
   ↓ (자동)
GitHub 푸시
   ↓ (완료)
학습 기록 백업 완료!
```

---

## 📊 학습 진행 상황

전체 진행률: `0%` (0/8 Chapters)

| Chapter | 주제 | 진행률 | 상태 |
|---------|------|--------|------|
| 1 | 딥러닝 시작 | 0% | ⏳ 대기중 |
| 2 | 인공신경망 | 0% | ⏳ 대기중 |
| 3 | Gradient Descent | 0% | ⏳ 대기중 |
| 4 | 이진/다중 분류 | 0% | ⏳ 대기중 |
| 5 | Universal Approximation | 0% | ⏳ 대기중 |
| 6 | 딥러닝 문제 해결 | 0% | ⏳ 대기중 |
| 7 | CNN | 0% | ⏳ 대기중 |
| 8 | RNN & Transformer | 0% | ⏳ 대기중 |

---

## 📖 블로그 포스팅

학습 내용은 자동으로 티스토리 블로그에 업로드됩니다.

- 블로그 주소: (추후 추가)

---

## 📝 라이선스

이 프로젝트는 개인 학습 목적으로 작성되었습니다.

---

## 📧 문의

- GitHub: [@kijae-kim](https://github.com/kijae-kim)
- Email: (추가 예정)
