#!/bin/bash
# GitHub 원격 저장소 연결 스크립트

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 프로젝트 루트로 이동
cd "$(dirname "$0")/.."

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🔗 GitHub 원격 저장소 연결${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# 이미 연결되어 있는지 확인
if git remote get-url origin > /dev/null 2>&1; then
    CURRENT_URL=$(git remote get-url origin)
    echo -e "\n${YELLOW}⚠️  이미 원격 저장소가 연결되어 있습니다:${NC}"
    echo -e "   ${CURRENT_URL}"
    read -p "변경하시겠습니까? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}취소되었습니다.${NC}"
        exit 0
    fi
    git remote remove origin
fi

echo -e "\n${BLUE}📝 GitHub 저장소 정보를 입력해주세요:${NC}"
echo -e "${YELLOW}   (예시: https://github.com/kijae-kim/EasyDL.git)${NC}"
echo

read -p "GitHub 저장소 URL: " REPO_URL

# URL 검증
if [[ ! $REPO_URL =~ ^https://github.com/.+/.+\.git$ ]]; then
    echo -e "\n${RED}❌ 올바른 GitHub URL 형식이 아닙니다.${NC}"
    echo -e "${YELLOW}   형식: https://github.com/사용자명/저장소명.git${NC}"
    exit 1
fi

# 원격 저장소 추가
echo -e "\n${BLUE}🔗 원격 저장소 연결 중...${NC}"
git remote add origin "$REPO_URL"

echo -e "${GREEN}✅ 원격 저장소 연결 완료!${NC}"

# 브랜치 확인
CURRENT_BRANCH=$(git branch --show-current)
echo -e "\n${BLUE}현재 브랜치: ${CURRENT_BRANCH}${NC}"

# 푸시 여부 확인
echo -e "\n${YELLOW}지금 원격 저장소로 푸시하시겠습니까?${NC}"
read -p "(y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "\n${BLUE}⬆️  푸시 중...${NC}"
    git push -u origin "$CURRENT_BRANCH"
    echo -e "\n${GREEN}✅ 푸시 완료!${NC}"
    echo -e "\n${GREEN}🎉 GitHub에서 확인하세요: ${REPO_URL%.git}${NC}"
else
    echo -e "\n${YELLOW}📌 나중에 푸시하려면:${NC}"
    echo -e "   ${BLUE}git push -u origin ${CURRENT_BRANCH}${NC}"
fi

echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}완료!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
