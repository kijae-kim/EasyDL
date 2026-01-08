# 🔄 Git 자동 커밋 가이드

> Obsidian 학습 노트와 코드를 GitHub에 자동으로 커밋하는 방법

---

## 🎯 목표

**Obsidian에서 학습 + Claude Code로 코드 구현 → GitHub 자동 커밋**

```
매일 학습 워크플로우:

1. Obsidian에서 학습 노트 작성
   ↓
2. VSCode에서 코드 구현 (Claude Code 도움)
   ↓
3. 자동 커밋 (Obsidian Git 플러그인 or 스크립트)
   ↓
4. GitHub 자동 푸시
```

---

## 🚀 방법 1: Obsidian Git 플러그인 (추천)

**완전 자동화 - 설정 후 아무것도 안 해도 됨!**

### Step 1: Obsidian Git 플러그인 설치

1. Obsidian 실행
2. `Settings (⚙️)` → `Community plugins` 클릭
3. `Browse` 클릭
4. 검색창에 **"Git"** 입력
5. **"Obsidian Git"** 플러그인 설치
6. `Enable` 클릭

### Step 2: 플러그인 설정

`Settings` → `Community plugins` → `Obsidian Git` 설정:

#### 기본 설정

```
✅ Vault backup interval (minutes): 10
   → 10분마다 자동 커밋

✅ Auto pull interval (minutes): 10
   → 10분마다 원격에서 가져오기 (다른 기기와 동기화)

✅ Commit message: {{date}} 학습 기록 자동 저장
   → 커밋 메시지 형식

✅ Auto push after commit: ON
   → 커밋 후 자동으로 GitHub 푸시

✅ Pull updates on startup: ON
   → Obsidian 시작 시 최신 상태로 업데이트
```

#### 고급 설정

```
✅ Disable notifications: OFF
   → 커밋/푸시 알림 받기 (선택)

✅ Show status bar: ON
   → 하단 상태 표시줄에 Git 상태 표시

✅ Commit Author: Your Name <your@email.com>
   → 본인 정보 입력 (선택)
```

### Step 3: GitHub 저장소 연결

#### 방법 A: 스크립트 사용 (간단)

터미널에서:

```bash
cd /Users/gimgijae/Desktop/Paper/EasyDL
./scripts/setup_github.sh
```

프롬프트에 따라 GitHub URL 입력

#### 방법 B: 수동 설정

1. **GitHub에서 새 저장소 생성**
   - https://github.com/new
   - 저장소 이름: `EasyDL`
   - Public 또는 Private 선택
   - `Create repository` 클릭

2. **로컬에서 원격 저장소 연결**

   터미널에서:
   ```bash
   cd /Users/gimgijae/Desktop/Paper/EasyDL

   git remote add origin https://github.com/kijae-kim/EasyDL.git
   git branch -M main
   git push -u origin main
   ```

### Step 4: 테스트

1. Obsidian에서 아무 노트나 수정
2. 10분 기다리거나 `Cmd+P` → "Git: Commit" 실행
3. GitHub에서 커밋 확인!

---

## 🔧 방법 2: 자동 커밋 스크립트

**플러그인 없이 스크립트로 자동화**

### 사용법

#### 수동 실행

학습이 끝난 후 터미널에서:

```bash
cd /Users/gimgijae/Desktop/Paper/EasyDL
./scripts/auto_commit.sh
```

자동으로:
- ✅ 변경된 파일 감지
- ✅ 커밋 메시지 생성 (노트/코드/자료 분류)
- ✅ Git commit
- ✅ GitHub push (선택)

#### 자동 실행 (Cron)

**매일 특정 시간에 자동 커밋**

1. Crontab 열기:
   ```bash
   crontab -e
   ```

2. 다음 줄 추가:
   ```bash
   # 매일 밤 11시에 자동 커밋
   0 23 * * * cd /Users/gimgijae/Desktop/Paper/EasyDL && ./scripts/auto_commit.sh >> logs/auto_commit.log 2>&1

   # 또는 2시간마다 자동 커밋
   0 */2 * * * cd /Users/gimgijae/Desktop/Paper/EasyDL && ./scripts/auto_commit.sh >> logs/auto_commit.log 2>&1
   ```

3. 저장 후 종료 (`:wq`)

---

## 🎓 학습 워크플로우

### 일일 학습 루틴

```bash
# 1. 가상환경 활성화
cd /Users/gimgijae/Desktop/Paper/EasyDL
source activate_env.sh

# 2. Obsidian 실행 (별도 앱)
open -a Obsidian

# 3. VSCode에서 코드 작성 (Claude Code 활용)
code .
```

#### Obsidian에서:
1. 새 노트 생성 (템플릿 사용)
2. 강의 시청하며 이론 정리
3. Claude와 Q&A 내용 추가

#### VSCode에서:
1. `code/` 폴더에 Python 파일 생성
2. Claude Code에게 질문하며 코드 구현
3. 실행 및 테스트

#### 자동 저장:
- **Obsidian Git 플러그인**: 10분마다 자동 커밋/푸시
- **또는 수동**: `./scripts/auto_commit.sh` 실행

---

## 📊 커밋 메시지 예시

### Obsidian Git 플러그인

```
2025-01-08 15:30 학습 기록 자동 저장
```

### 자동 커밋 스크립트

```
학습 기록 자동 저장 - 2025-01-08 15:30:45

- 학습 노트: 2개 파일 수정
- 코드 구현: 3개 파일 수정
- 자료 추가: 1개 파일 추가

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## 🔍 Git 상태 확인

### Obsidian에서

- 하단 상태바에 Git 아이콘 표시
- 클릭하면 상세 정보

### 터미널에서

```bash
# 현재 상태
git status

# 최근 커밋 확인
git log --oneline -5

# 원격 저장소 확인
git remote -v

# 원격과 로컬 차이
git log origin/main..main
```

---

## 🐛 문제 해결

### 1. Obsidian Git 플러그인이 작동하지 않아요

**원인**: 원격 저장소가 설정되지 않음

**해결**:
```bash
cd /Users/gimgijae/Desktop/Paper/EasyDL
./scripts/setup_github.sh
```

### 2. "Permission denied" 오류

**원인**: SSH 키 또는 HTTPS 인증 문제

**해결**:
```bash
# HTTPS 사용 (추천)
git remote set-url origin https://github.com/kijae-kim/EasyDL.git

# Personal Access Token 사용
# GitHub → Settings → Developer settings → Personal access tokens
# Token 생성 후 비밀번호 대신 사용
```

### 3. 자동 커밋이 너무 자주/적게 발생해요

**Obsidian Git 플러그인 간격 조정**:
- `Settings` → `Obsidian Git`
- `Vault backup interval` 값 변경
- 추천: 10-30분

### 4. 특정 파일을 커밋하고 싶지 않아요

`.gitignore` 파일 수정:

```bash
# 예시: 개인 노트 제외
private/
**/private.md

# 예시: 대용량 데이터셋 제외
datasets/
*.csv

# 예시: 실험용 파일 제외
**/test_*.py
scratch/
```

---

## 🎯 추천 설정

### 초보자 (간단)

- ✅ Obsidian Git 플러그인 사용
- ✅ 자동 커밋 간격: 30분
- ✅ 자동 푸시: ON

### 중급자 (제어)

- ✅ 자동 커밋 스크립트
- ✅ 학습 종료 후 수동 실행
- ✅ 커밋 메시지 확인 후 푸시

### 고급자 (완전 자동화)

- ✅ Obsidian Git 플러그인 + Cron
- ✅ GitHub Actions 추가 (CI/CD)
- ✅ 자동 테스트 실행

---

## 📚 참고 자료

- [Obsidian Git 플러그인 문서](https://github.com/denolehov/obsidian-git)
- [Git 기본 명령어](https://git-scm.com/docs)
- [GitHub 가이드](https://guides.github.com/)

---

## ✅ 설정 완료 체크리스트

- [ ] Obsidian Git 플러그인 설치
- [ ] 플러그인 자동 커밋 설정 (10-30분)
- [ ] GitHub 저장소 생성
- [ ] 원격 저장소 연결 (`./scripts/setup_github.sh`)
- [ ] 첫 자동 커밋 테스트
- [ ] GitHub에서 커밋 확인

---

완료되면 학습에만 집중하세요! Git은 자동으로 관리됩니다. 🎓
