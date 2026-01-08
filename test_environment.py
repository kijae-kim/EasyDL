#!/usr/bin/env python3
"""
환경 설정 테스트 스크립트
"""

import sys

def test_imports():
    """주요 라이브러리 임포트 테스트"""
    print("=" * 60)
    print("📦 패키지 임포트 테스트")
    print("=" * 60)

    try:
        import tensorflow as tf
        print(f"✅ TensorFlow {tf.__version__}")
    except ImportError as e:
        print(f"❌ TensorFlow 임포트 실패: {e}")
        return False

    try:
        import torch
        print(f"✅ PyTorch {torch.__version__}")
    except ImportError as e:
        print(f"❌ PyTorch 임포트 실패: {e}")
        return False

    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__}")
    except ImportError as e:
        print(f"❌ NumPy 임포트 실패: {e}")
        return False

    try:
        import pandas as pd
        print(f"✅ Pandas {pd.__version__}")
    except ImportError as e:
        print(f"❌ Pandas 임포트 실패: {e}")
        return False

    try:
        import matplotlib
        print(f"✅ Matplotlib {matplotlib.__version__}")
    except ImportError as e:
        print(f"❌ Matplotlib 임포트 실패: {e}")
        return False

    return True

def test_tensorflow():
    """TensorFlow 기본 동작 테스트"""
    print("\n" + "=" * 60)
    print("🔥 TensorFlow 기본 동작 테스트")
    print("=" * 60)

    try:
        import tensorflow as tf

        # 간단한 텐서 생성
        a = tf.constant([[1, 2], [3, 4]])
        b = tf.constant([[5, 6], [7, 8]])
        c = tf.matmul(a, b)

        print(f"행렬 곱셈 결과:\n{c.numpy()}")
        print("✅ TensorFlow 정상 작동")
        return True
    except Exception as e:
        print(f"❌ TensorFlow 테스트 실패: {e}")
        return False

def test_pytorch():
    """PyTorch 기본 동작 테스트"""
    print("\n" + "=" * 60)
    print("🔥 PyTorch 기본 동작 테스트")
    print("=" * 60)

    try:
        import torch

        # 간단한 텐서 생성
        x = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
        y = torch.tensor([[5, 6], [7, 8]], dtype=torch.float32)
        z = torch.matmul(x, y)

        print(f"행렬 곱셈 결과:\n{z.numpy()}")
        print("✅ PyTorch 정상 작동")
        return True
    except Exception as e:
        print(f"❌ PyTorch 테스트 실패: {e}")
        return False

def main():
    """메인 함수"""
    print("\n🚀 EasyDL 환경 설정 테스트 시작\n")

    results = []

    # 1. 임포트 테스트
    results.append(test_imports())

    # 2. TensorFlow 테스트
    results.append(test_tensorflow())

    # 3. PyTorch 테스트
    results.append(test_pytorch())

    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 테스트 결과 요약")
    print("=" * 60)

    if all(results):
        print("✅ 모든 테스트 통과!")
        print("🎉 환경 설정이 완료되었습니다!")
        print("\n다음 단계:")
        print("  1. Obsidian에서 Vault 연결")
        print("  2. 00_학습_가이드/시작하기.md 확인")
        print("  3. Chapter 1 학습 시작!")
        return 0
    else:
        print("❌ 일부 테스트 실패")
        print("문제 해결:")
        print("  1. 가상환경 활성화 확인: source EasyDL/bin/activate")
        print("  2. 패키지 재설치: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
