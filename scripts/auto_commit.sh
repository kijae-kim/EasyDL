#!/bin/bash
# Git 자동 커밋 스크립트
# 변경사항을 감지하고 자동으로 커밋합니다.

set -e  # 에러 발생 시 스크립트 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 프로젝트 루트로 이동
cd "$(dirname "$0")/.."

# 현재 브랜치 확인
CURRENT_BRANCH=$(git branch --show-current)

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🔄 Git 자동 커밋 시작${NC}"
echo -e "${BLUE}📍 현재 브랜치: ${CURRENT_BRANCH}${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Git 상태 확인
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Git 저장소가 아닙니다.${NC}"
    exit 1
fi

# 변경사항 확인
if git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}📝 변경사항이 없습니다.${NC}"
    exit 0
fi

# 변경된 파일 출력
echo -e "\n${GREEN}📂 변경된 파일:${NC}"
git status --short

# 커밋 메시지 생성
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
CHANGED_FILES=$(git diff --name-only | wc -l | tr -d ' ')

# 변경된 파일 분류
NOTES_CHANGED=$(git diff --name-only | grep -c "notes/.*\.md" || echo 0)
CODE_CHANGED=$(git diff --name-only | grep -c "code/.*\.py" || echo 0)
ASSETS_CHANGED=$(git diff --name-only | grep -c "assets/" || echo 0)

# 커밋 메시지 구성
COMMIT_MSG="학습 기록 자동 저장 - ${TIMESTAMP}"

if [ "$NOTES_CHANGED" -gt 0 ]; then
    COMMIT_MSG="${COMMIT_MSG}\n\n- 학습 노트: ${NOTES_CHANGED}개 파일 수정"
fi

if [ "$CODE_CHANGED" -gt 0 ]; then
    COMMIT_MSG="${COMMIT_MSG}\n- 코드 구현: ${CODE_CHANGED}개 파일 수정"
fi

if [ "$ASSETS_CHANGED" -gt 0 ]; then
    COMMIT_MSG="${COMMIT_MSG}\n- 자료 추가: ${ASSETS_CHANGED}개 파일 추가"
fi

# Git add
echo -e "\n${BLUE}➕ 변경사항 스테이징...${NC}"
git add .

# Git commit
echo -e "\n${BLUE}💾 커밋 생성...${NC}"
git commit -m "$(echo -e "${COMMIT_MSG}\n\nCo-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>")"

echo -e "\n${GREEN}✅ 커밋 완료!${NC}"

# 원격 저장소 푸시 여부 확인
if git remote get-url origin > /dev/null 2>&1; then
    echo -e "\n${YELLOW}🔗 원격 저장소가 연결되어 있습니다.${NC}"
    read -p "원격 저장소에 푸시하시겠습니까? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${BLUE}⬆️  원격 저장소로 푸시 중...${NC}"
        git push
        echo -e "${GREEN}✅ 푸시 완료!${NC}"
    else
        echo -e "${YELLOW}📌 로컬에만 커밋되었습니다.${NC}"
        echo -e "${YELLOW}   나중에 푸시하려면: git push${NC}"
    fi
else
    echo -e "\n${YELLOW}📌 원격 저장소가 설정되지 않았습니다.${NC}"
    echo -e "${YELLOW}   GitHub 연동을 원하면 scripts/setup_github.sh를 실행하세요.${NC}"
fi

echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 완료!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
