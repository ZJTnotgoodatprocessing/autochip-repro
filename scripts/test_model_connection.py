"""Quick test: verify LLM API connectivity via the relay."""

import sys
from pathlib import Path

# Allow running from project root: python scripts/test_model_connection.py
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from src.llm.client import generate


def main():
    print("Testing LLM connection...")
    print(f"  Sending: 'Reply with exactly: Hello AutoChip'")
    try:
        reply = generate("Reply with exactly: Hello AutoChip", temperature=0.0)
        print(f"  Response: {reply.strip()}")
        print("Connection OK")
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
