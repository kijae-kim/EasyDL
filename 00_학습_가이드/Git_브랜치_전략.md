# 🌿 Git 브랜치 전략

> develop 브랜치로 일상 학습, main 브랜치로 마일스톤 관리

---

## 🎯 브랜치 전략 개요

### 브랜치 구조

```
main (프로덕션)
  ↑
  | (PR & 병합)
  |
develop (개발/학습)
  ↑
  | (자동 커밋)
  |
일상 학습 & 코드 구현
```

### 역할

| 브랜치 | 용도 | 커밋 빈도 |
|--------|------|-----------|
| **develop** | 일상 학습, 코드 구현, 실험 | 자동 (10분마다) |
| **main** | 완성된 Chapter, 중요 마일스톤 | 수동 (주간/월간) |

---

## 📋 워크플로우

### 일상 학습 (develop 브랜치)

```bash
# 1. develop 브랜치에서 작업
git checkout develop

# 2. Obsidian에서 노트 작성
#    VSCode에서 코드 구현

# 3. 자동 커밋 (Obsidian Git 또는 스크립트)
#    → develop 브랜치에 자동 푸시

# 4. GitHub에서 확인
#    https://github.com/kijae-kim/EasyDL/tree/develop
```

### Chapter 완료 시 (main으로 병합)

```bash
# 1. Chapter 학습 완료 확인
#    예: Chapter 1의 모든 강의 완료

# 2. main 브랜치로 이동
git checkout main

# 3. develop 병합
git merge develop

# 4. 버전 태그 추가 (선택)
git tag -a v1.0-chapter1 -m "Chapter 1 완료: 딥러닝 시작"

# 5. GitHub에 푸시
git push origin main --tags
```

---

## 🔧 현재 설정

### ✅ 생성된 브랜치

```bash
✅ main: 안정적인 마일스톤 버전
✅ develop: 일상 학습 및 개발 (현재 브랜치)
```

### ✅ 기본 브랜치: develop

**Obsidian Git 플러그인**과 **자동 커밋 스크립트**는 현재 브랜치(develop)에 커밋합니다.

---

## 🚀 빠른 시작

### Step 1: develop 브랜치 확인

```bash
cd /Users/gimgijae/Desktop/Paper/EasyDL
git branch --show-current
```

출력: `develop` ✅

### Step 2: Obsidian Git 플러그인 설정

Obsidian에서 이미 설정되어 있다면 **아무것도 변경할 필요 없습니다!**

플러그인은 현재 브랜치(develop)에 자동으로 커밋/푸시합니다.

### Step 3: 학습 시작

평소처럼 학습하면 됩니다!
- Obsidian에서 노트 작성
- VSCode에서 코드 구현
- 자동으로 develop 브랜치에 커밋

---

## 📊 브랜치별 사용 시나리오

### develop 브랜치 (일상 작업)

#### 사용 시기
- ✅ 매일 강의 시청 및 노트 작성
- ✅ 코드 실습 및 실험
- ✅ Claude와 Q&A
- ✅ 미완성 코드 또는 초안

#### 특징
- 🔄 자동 커밋/푸시
- 🧪 실험적인 코드 허용
- 📝 완벽하지 않아도 OK
- 🚀 빠른 반복 학습

---

### main 브랜치 (마일스톤)

#### 사용 시기
- ✅ Chapter 완료
- ✅ 프로젝트 완성
- ✅ 중요한 업데이트
- ✅ 블로그 포스팅 전

#### 특징
- 🏆 완성된 코드만
- 📚 정제된 문서
- 🔖 버전 태그 사용
- 🎯 안정적인 상태

---

## 🔄 브랜치 전환

### develop → main 병합 (Chapter 완료 시)

```bash
# 1. 현재 작업 커밋 (develop)
git add .
git commit -m "Chapter 1 완료"
git push

# 2. main으로 전환
git checkout main

# 3. develop 병합
git merge develop

# 4. 병합 내용 확인
git log --oneline -5

# 5. 태그 추가 (선택)
git tag -a v1.0-chapter1 -m "Chapter 1: 딥러닝 시작 완료"

# 6. GitHub에 푸시
git push origin main --tags
```

### main → develop 다시 돌아오기

```bash
git checkout develop
```

---

## 📝 커밋 메시지 규칙

### develop 브랜치 (자동)

Obsidian Git 또는 자동 스크립트:
```
학습 기록 자동 저장 - 2025-01-08 15:30:45

- 학습 노트: 2개 파일 수정
- 코드 구현: 3개 파일 수정
```

### main 브랜치 (수동)

중요한 마일스톤:
```
feat: Chapter 1 완료 - 딥러닝 시작

- 퍼셉트론 학습 및 구현
- 신경망 기초 이해
- 텐서플로우 실습 완료
```

---

## 🎓 학습 단계별 가이드

### Week 1-2: Chapter 1 학습 (develop)

```bash
# develop 브랜치에서 작업
git checkout develop

# 매일 자동 커밋
# - 퍼셉트론 노트 작성
# - 신경망 코드 구현
# - 실험 결과 정리
```

**GitHub**: `https://github.com/kijae-kim/EasyDL/tree/develop`

### Week 2 끝: Chapter 1 완료 (main)

```bash
# main으로 병합
git checkout main
git merge develop
git tag -a v1.0-chapter1 -m "Chapter 1 완료"
git push origin main --tags

# 다시 develop으로
git checkout develop
```

**GitHub**: `https://github.com/kijae-kim/EasyDL` (main 브랜치)

---

## 🔍 브랜치 확인 명령어

### 현재 브랜치 확인

```bash
git branch --show-current
```

### 모든 브랜치 보기

```bash
git branch -a
```

출력:
```
  main
* develop
  remotes/origin/main
  remotes/origin/develop
```

### 브랜치 간 차이 확인

```bash
# main과 develop 차이
git diff main..develop

# 파일 목록만
git diff --name-only main..develop
```

---

## 🌐 GitHub에서 확인

### develop 브랜치 (일상 작업)

```
https://github.com/kijae-kim/EasyDL/tree/develop
```

### main 브랜치 (완성본)

```
https://github.com/kijae-kim/EasyDL
```

### Pull Request 만들기 (선택)

Chapter 완료 시 PR을 만들어 리뷰할 수 있습니다:

```
https://github.com/kijae-kim/EasyDL/compare/main...develop
```

---

## 💡 자주 묻는 질문

### Q1: 지금 어떤 브랜치에 있나요?

```bash
git branch --show-current
```

### Q2: 실수로 main에 커밋했어요!

```bash
# 1. 커밋 취소 (로컬만)
git reset --soft HEAD~1

# 2. develop으로 이동
git checkout develop

# 3. 다시 커밋
git add .
git commit -m "메시지"
git push
```

### Q3: develop을 main으로 병합하는 시기는?

**추천 타이밍**:
- ✅ Chapter 완료 (예: Chapter 1 완료)
- ✅ 주간 학습 마무리 (금요일)
- ✅ 블로그 포스팅 전
- ✅ 프로젝트 완성 시

### Q4: Obsidian Git 플러그인 설정 변경 필요한가요?

**아니요!** 플러그인은 현재 브랜치에 자동으로 커밋합니다.
- develop 브랜치에 있으면 → develop에 커밋
- main 브랜치에 있으면 → main에 커밋

---

## 📊 버전 태그 가이드 (선택 사항)

### 태그 형식

```
v<major>.<minor>-<chapter/feature>
```

### 예시

```bash
# Chapter 완료
git tag -a v1.0-chapter1 -m "Chapter 1: 딥러닝 시작"
git tag -a v2.0-chapter2 -m "Chapter 2: 인공신경망"

# 프로젝트 마일스톤
git tag -a v0.5-setup -m "초기 환경 설정 완료"
git tag -a v4.0-midpoint -m "커리큘럼 50% 완료"
git tag -a v8.0-complete -m "전체 커리큘럼 완료"
```

### 태그 푸시

```bash
# 특정 태그 푸시
git push origin v1.0-chapter1

# 모든 태그 푸시
git push origin --tags
```

---

## ✅ 체크리스트

### 초기 설정 (완료!)
- [x] develop 브랜치 생성
- [x] develop을 GitHub에 푸시
- [x] 자동 커밋 스크립트 업데이트

### 일상 학습 (매일)
- [ ] develop 브랜치 확인
- [ ] Obsidian 노트 작성
- [ ] 코드 구현
- [ ] 자동 커밋 확인

### Chapter 완료 시 (주간/월간)
- [ ] develop의 모든 작업 커밋
- [ ] main으로 병합
- [ ] 버전 태그 추가
- [ ] GitHub 푸시
- [ ] develop으로 복귀

---

## 🚀 요약

### 평소 학습 (99%)
```bash
git checkout develop
# 학습 → 자동 커밋 → develop 브랜치 푸시
```

### Chapter 완료 (1%)
```bash
git checkout main
git merge develop
git tag -a v1.0-chapter1 -m "Chapter 1 완료"
git push origin main --tags
git checkout develop
```

---

**simple하게 develop에서 학습하고, 완료되면 main으로 병합!**

질문이 있으면 언제든 물어보세요! 🌟
