#!/usr/bin/env python3
"""
티스토리 자동 포스팅 스크립트

Obsidian 마크다운 노트를 티스토리 블로그에 자동으로 포스팅합니다.
"""

import os
import json
import re
import requests
from pathlib import Path
from datetime import datetime
import markdown


class TistoryPoster:
    """티스토리 API를 사용한 자동 포스팅 클래스"""

    def __init__(self, config_path: str = None):
        """
        초기화

        Args:
            config_path: 설정 파일 경로 (JSON)
        """
        if config_path is None:
            config_path = Path(__file__).parent / "tistory_config.json"

        self.config = self.load_config(config_path)
        self.api_url = "https://www.tistory.com/apis/post/write"

    def load_config(self, config_path: str) -> dict:
        """
        티스토리 API 설정 로드

        설정 파일 예시 (tistory_config.json):
        {
            "access_token": "YOUR_ACCESS_TOKEN",
            "blog_name": "your-blog-name",
            "category_mapping": {
                "Chapter1": "123456",
                "Chapter2": "123457"
            }
        }
        """
        config_path = Path(config_path)

        if not config_path.exists():
            print(f"⚠️  설정 파일이 없습니다: {config_path}")
            print("📝 tistory_config.json 파일을 생성하세요.")
            return {}

        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def markdown_to_html(self, markdown_text: str) -> str:
        """
        마크다운을 HTML로 변환

        Args:
            markdown_text: 마크다운 텍스트

        Returns:
            HTML 텍스트
        """
        # 코드 하이라이팅을 위한 확장
        html = markdown.markdown(
            markdown_text,
            extensions=[
                'fenced_code',
                'codehilite',
                'tables',
                'toc'
            ]
        )
        return html

    def extract_frontmatter(self, markdown_text: str) -> tuple[dict, str]:
        """
        마크다운에서 YAML frontmatter 추출

        Returns:
            (frontmatter dict, 본문 텍스트)
        """
        frontmatter = {}
        content = markdown_text

        # YAML frontmatter 파싱
        if markdown_text.startswith('---'):
            parts = markdown_text.split('---', 2)
            if len(parts) >= 3:
                frontmatter_text = parts[1]
                content = parts[2].strip()

                # 간단한 YAML 파싱
                for line in frontmatter_text.strip().split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip().strip('"')

        return frontmatter, content

    def post_to_tistory(
        self,
        title: str,
        content: str,
        category: str = "0",
        visibility: int = 3,
        tag: str = ""
    ) -> dict:
        """
        티스토리에 포스팅

        Args:
            title: 글 제목
            content: 글 내용 (HTML)
            category: 카테고리 ID
            visibility: 발행 상태 (0: 비공개, 1: 보호, 3: 발행)
            tag: 태그 (쉼표로 구분)

        Returns:
            API 응답
        """
        if not self.config:
            print("⚠️  티스토리 설정이 없습니다.")
            return {}

        params = {
            'access_token': self.config.get('access_token'),
            'blogName': self.config.get('blog_name'),
            'title': title,
            'content': content,
            'visibility': visibility,
            'category': category,
            'tag': tag,
            'output': 'json'
        }

        try:
            response = requests.post(self.api_url, data=params)
            result = response.json()

            if result.get('tistory', {}).get('status') == '200':
                print(f"✅ 포스팅 성공: {title}")
                post_url = result.get('tistory', {}).get('url')
                print(f"🔗 URL: {post_url}")
                return result
            else:
                print(f"❌ 포스팅 실패: {result}")
                return result

        except Exception as e:
            print(f"❌ 에러 발생: {e}")
            return {}

    def post_from_markdown_file(self, markdown_file: str, dry_run: bool = False):
        """
        마크다운 파일을 읽어서 티스토리에 포스팅

        Args:
            markdown_file: 마크다운 파일 경로
            dry_run: True면 실제 포스팅하지 않고 미리보기만
        """
        file_path = Path(markdown_file)

        if not file_path.exists():
            print(f"⚠️  파일이 존재하지 않습니다: {file_path}")
            return

        # 마크다운 읽기
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_text = f.read()

        # Frontmatter 추출
        frontmatter, content = self.extract_frontmatter(markdown_text)

        # 제목 추출 (첫 번째 H1 또는 frontmatter의 topic)
        title = frontmatter.get('topic', '제목 없음')
        if title == '제목 없음':
            h1_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if h1_match:
                title = h1_match.group(1)

        # HTML 변환
        html_content = self.markdown_to_html(content)

        # 카테고리 매핑
        chapter = frontmatter.get('chapter', '')
        category_id = self.config.get('category_mapping', {}).get(chapter, '0')

        # 태그 추출
        tags = frontmatter.get('tags', '[]')
        if isinstance(tags, str):
            tags = tags.strip('[]').replace(',', ', ')

        if dry_run:
            print("=" * 60)
            print("📝 포스팅 미리보기 (dry_run 모드)")
            print("=" * 60)
            print(f"제목: {title}")
            print(f"카테고리: {category_id}")
            print(f"태그: {tags}")
            print("-" * 60)
            print(html_content[:500])
            print("=" * 60)
        else:
            # 실제 포스팅
            self.post_to_tistory(
                title=title,
                content=html_content,
                category=category_id,
                tag=tags
            )


def main():
    """메인 함수 - 사용 예시"""

    # 포스터 생성
    poster = TistoryPoster()

    # 예시: 특정 마크다운 파일 포스팅 (dry_run 모드)
    example_file = Path(__file__).parent.parent / "02_Chapter2_인공신경망/notes/03_선형회귀.md"

    if example_file.exists():
        poster.post_from_markdown_file(example_file, dry_run=True)
    else:
        print("📝 사용법:")
        print("  python tistory_poster.py")
        print("")
        print("설정 파일 생성 (scripts/tistory_config.json):")
        print(json.dumps({
            "access_token": "YOUR_TISTORY_ACCESS_TOKEN",
            "blog_name": "your-blog-name",
            "category_mapping": {
                "Chapter 1": "123456",
                "Chapter 2": "123457"
            }
        }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
