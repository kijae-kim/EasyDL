#!/bin/bash
# EasyDL 가상환경 활성화 스크립트

echo "🚀 EasyDL 가상환경을 활성화합니다..."

# 프로젝트 루트로 이동
cd "$(dirname "$0")"

# 가상환경 활성화
source EasyDL/bin/activate

echo "✅ 가상환경 활성화 완료!"
echo "📦 Python $(python --version)"
echo "📍 Working directory: $(pwd)"
echo ""
echo "사용 가능한 명령어:"
echo "  - python: Python 실행"
echo "  - pip: 패키지 관리"
echo "  - jupyter notebook: Jupyter 실행"
echo "  - deactivate: 가상환경 비활성화"
echo ""
echo "학습을 시작하려면 00_학습_가이드/시작하기.md를 참고하세요!"
