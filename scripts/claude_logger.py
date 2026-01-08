#!/usr/bin/env python3
"""
Claude 대화 자동 로깅 스크립트

VSCode Claude Code와의 대화 내용을 구조화하여 Obsidian 노트에 자동으로 추가합니다.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path


class ClaudeLogger:
    """Claude 대화를 로깅하고 Obsidian 노트에 통합하는 클래스"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.log_dir = self.project_root / "logs"
        self.log_dir.mkdir(exist_ok=True)

    def parse_conversation(self, conversation_text: str) -> list[dict]:
        """
        대화 텍스트를 파싱하여 Q&A 형식으로 변환

        Args:
            conversation_text: 원본 대화 텍스트

        Returns:
            [{"question": "...", "answer": "...", "timestamp": "..."}]
        """
        qa_pairs = []

        # 간단한 패턴 매칭 (실제로는 더 정교한 파싱 필요)
        lines = conversation_text.split('\n')
        current_q = None
        current_a = []

        for line in lines:
            if line.startswith("Q:") or line.startswith("질문:"):
                if current_q and current_a:
                    qa_pairs.append({
                        "question": current_q,
                        "answer": "\n".join(current_a),
                        "timestamp": datetime.now().isoformat()
                    })
                current_q = line.split(":", 1)[1].strip()
                current_a = []
            elif line.startswith("A:") or line.startswith("답변:"):
                current_a.append(line.split(":", 1)[1].strip())
            elif current_q:
                current_a.append(line)

        # 마지막 Q&A 추가
        if current_q and current_a:
            qa_pairs.append({
                "question": current_q,
                "answer": "\n".join(current_a),
                "timestamp": datetime.now().isoformat()
            })

        return qa_pairs

    def save_to_json(self, qa_pairs: list[dict], filename: str):
        """Q&A 쌍을 JSON 파일로 저장"""
        log_file = self.log_dir / f"{filename}.json"

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(qa_pairs, f, ensure_ascii=False, indent=2)

        print(f"✅ 대화 로그 저장 완료: {log_file}")

    def append_to_note(self, qa_pairs: list[dict], note_path: str):
        """
        Q&A를 기존 Obsidian 노트에 추가

        Args:
            qa_pairs: Q&A 쌍 리스트
            note_path: 노트 파일 경로 (상대 경로)
        """
        full_path = self.project_root / note_path

        if not full_path.exists():
            print(f"⚠️  노트 파일이 존재하지 않습니다: {full_path}")
            return

        # 기존 내용 읽기
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Q&A 섹션 찾기 또는 생성
        qa_section_marker = "## 🤔 Claude와의 Q&A"

        if qa_section_marker not in content:
            print(f"⚠️  Q&A 섹션을 찾을 수 없습니다. 템플릿을 사용하세요.")
            return

        # Q&A 내용 생성
        qa_text = "\n\n"
        for i, qa in enumerate(qa_pairs, 1):
            qa_text += f"### Q{i}: {qa['question']}\n\n"
            qa_text += f"**A{i}**: {qa['answer']}\n\n"
            qa_text += f"*{qa['timestamp']}*\n\n"
            qa_text += "---\n\n"

        # Q&A 섹션 다음에 내용 삽입
        parts = content.split(qa_section_marker)
        if len(parts) == 2:
            # 다음 섹션(##) 찾기
            next_section_match = re.search(r'\n## ', parts[1])
            if next_section_match:
                insert_pos = next_section_match.start()
                new_content = (
                    parts[0] +
                    qa_section_marker +
                    parts[1][:insert_pos] +
                    qa_text +
                    parts[1][insert_pos:]
                )
            else:
                new_content = parts[0] + qa_section_marker + parts[1] + qa_text

            # 파일 업데이트
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✅ Q&A 추가 완료: {full_path}")

    def create_daily_log(self):
        """일일 대화 로그 파일 생성"""
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.log_dir / f"claude_log_{today}.md"

        if not log_file.exists():
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"# Claude 대화 로그 - {today}\n\n")
                f.write("---\n\n")

        return log_file


def main():
    """메인 함수 - 사용 예시"""

    # 프로젝트 루트 경로
    project_root = Path(__file__).parent.parent

    # 로거 생성
    logger = ClaudeLogger(project_root)

    # 예시: 대화 텍스트 (실제로는 VSCode에서 가져옴)
    conversation = """
Q: 경사하강법이 뭔가요?
A: 경사하강법(Gradient Descent)은 손실 함수를 최소화하기 위해
파라미터를 조금씩 업데이트하는 최적화 알고리즘입니다.

Q: 학습률은 어떻게 정하나요?
A: 학습률(Learning Rate)은 일반적으로 0.001 ~ 0.1 사이 값으로 시작하며,
학습 과정을 관찰하면서 조정합니다.
    """

    # 대화 파싱
    qa_pairs = logger.parse_conversation(conversation)

    # JSON으로 저장
    logger.save_to_json(qa_pairs, f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}")

    # Obsidian 노트에 추가 (예시)
    # logger.append_to_note(qa_pairs, "02_Chapter2_인공신경망/notes/04_경사하강법.md")

    print("✅ Claude 대화 로깅 완료!")


if __name__ == "__main__":
    main()
