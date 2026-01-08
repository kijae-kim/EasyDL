# 📘 Obsidian 설정 가이드

> EasyDL 프로젝트를 Obsidian Vault로 연결하는 방법

---

## 🎯 Obsidian이란?

**Obsidian**은 마크다운 기반의 강력한 노트 작성 도구입니다.

### 장점
- ✅ 로컬 파일 기반 (Git 연동 용이)
- ✅ 마크다운 완벽 지원
- ✅ 양방향 링크로 지식 연결
- ✅ 플러그인을 통한 확장성
- ✅ 무료 (개인 사용)

---

## 📥 설치 방법

### macOS (M1/M2)
```bash
brew install --cask obsidian
```

### 또는 직접 다운로드
[Obsidian 공식 사이트](https://obsidian.md/)에서 다운로드

---

## 🔧 Vault 설정

### 1단계: Obsidian 실행

Obsidian을 실행하면 "Open folder as vault" 선택

### 2단계: EasyDL 폴더 선택

```
/Users/gimgijae/Desktop/Paper/EasyDL
```

위 경로를 Vault로 설정

### 3단계: Trust author 선택

처음 열 때 "Trust author and enable plugins" 선택

---

## 🔌 필수 플러그인 설치

### Core Plugins (기본 활성화)

Settings (⚙️) → Core plugins에서 다음 활성화:

- ✅ **File explorer**: 파일 탐색
- ✅ **Search**: 검색
- ✅ **Quick switcher**: 빠른 파일 전환
- ✅ **Graph view**: 지식 그래프
- ✅ **Backlinks**: 역링크
- ✅ **Templates**: 템플릿 사용
- ✅ **Daily notes**: 일일 노트

---

### Community Plugins (추가 설치)

Settings → Community plugins → Browse

#### 1. **Templater** (필수)
- 고급 템플릿 기능
- 날짜, 시간 자동 삽입

**설정**:
```
Template folder: templates
Trigger Templater on new file creation: ON
```

#### 2. **Dataview** (필수)
- 학습 진행 상황 시각화
- 자동 통계 생성

**사용 예시**:
```dataview
TABLE status, date
FROM "02_Chapter2_인공신경망/notes"
WHERE status = "🔄 학습중"
```

#### 3. **Git** (권장)
- Obsidian 내에서 Git 커밋/푸시

**설정**:
```
Vault backup interval: 10 (10분마다 자동 커밋)
Commit message: "vault backup: {{date}}"
```

#### 4. **Advanced Tables** (권장)
- 마크다운 테이블 편집 지원

#### 5. **Calendar** (선택)
- 일일 학습 기록 시각화

---

## 📝 템플릿 설정

### Settings → Templates

- **Template folder location**: `templates`
- **Date format**: `YYYY-MM-DD`
- **Time format**: `HH:mm`

### 템플릿 사용 방법

1. 새 노트 생성
2. `Cmd/Ctrl + P` → "Insert template" 선택
3. "학습_노트_템플릿" 선택

---

## 🎨 외관 설정 (선택)

### 테마 추천

Settings → Appearance → Themes

- **Minimal**: 깔끔한 디자인
- **Blue Topaz**: 한국어 지원 우수
- **Things**: macOS 스타일

---

## 🔗 핵심 기능 사용법

### 1. 양방향 링크

```markdown
이전 학습: [[02_선형회귀]]
다음 학습: [[04_경사하강법]]
```

### 2. 임베드 (문서 포함)

```markdown
![[커리큘럼#Chapter 2]]
```

### 3. 태그

```markdown
#딥러닝 #경사하강법 #최적화
```

### 4. 코드 블록

```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
```

### 5. 수식 (LaTeX)

```markdown
손실 함수: $L(\theta) = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$

$$
\theta_{t+1} = \theta_t - \eta \nabla L(\theta_t)
$$
```

---

## 📊 학습 대시보드 만들기

`00_학습_가이드/대시보드.md` 파일 생성:

```markdown
# 📊 학습 대시보드

## 🔄 현재 학습 중

\`\`\`dataview
TABLE topic, date
FROM "01_Chapter1_딥러닝_시작/notes" OR "02_Chapter2_인공신경망/notes"
WHERE status = "🔄 학습중"
SORT date DESC
\`\`\`

## ✅ 완료한 학습

\`\`\`dataview
TABLE topic, date
FROM ""
WHERE status = "✅ 완료"
SORT date DESC
LIMIT 10
\`\`\`

## 📈 이번 주 학습 시간

\`\`\`dataview
TABLE sum(학습시간) as "총 시간"
WHERE date >= date(today) - dur(7 days)
\`\`\`
```

---

## 🎯 워크플로우

### 1. 강의 시청 전
1. 새 노트 생성
2. 템플릿 삽입
3. 학습 목표 작성

### 2. 강의 시청 중
1. 핵심 개념 정리
2. 코드 실습
3. Claude와 Q&A

### 3. 강의 시청 후
1. 핵심 정리 작성
2. 다음 학습 링크 연결
3. Git 커밋
4. 블로그 포스팅

---

## 🔥 단축키 (필수)

| 기능 | macOS | Windows |
|------|-------|---------|
| 명령 팔레트 | `Cmd+P` | `Ctrl+P` |
| 빠른 검색 | `Cmd+O` | `Ctrl+O` |
| 새 노트 | `Cmd+N` | `Ctrl+N` |
| 그래프 뷰 | `Cmd+G` | `Ctrl+G` |
| 설정 | `Cmd+,` | `Ctrl+,` |

---

## 📚 추가 자료

- [Obsidian 공식 문서](https://help.obsidian.md/)
- [Dataview 플러그인 문서](https://blacksmithgu.github.io/obsidian-dataview/)
- [Templater 플러그인 문서](https://silentvoid13.github.io/Templater/)

---

## ✅ 설정 완료 체크리스트

- [ ] Obsidian 설치
- [ ] EasyDL 폴더를 Vault로 설정
- [ ] Core plugins 활성화
- [ ] Templater 플러그인 설치 및 설정
- [ ] Dataview 플러그인 설치
- [ ] Git 플러그인 설치 (선택)
- [ ] 템플릿 폴더 설정
- [ ] 첫 번째 노트 생성 테스트

---

완료되면 학습을 시작할 준비가 완료됩니다! 🚀
