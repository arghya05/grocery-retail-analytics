#!/usr/bin/env python3
"""
Ask a question to the LangGraph Store Manager
Usage: python3 ask_question.py "Your question here"
"""

import sys
from langgraph_multi_agent_store_manager import LangGraphStoreManager

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ask_question.py \"Your question here\"")
        sys.exit(1)

    # Get question from command line
    question = " ".join(sys.argv[1:])

    # Initialize system (loads all data)
    system = LangGraphStoreManager()

    print(f"\n{'='*70}")
    print(f"YOUR QUESTION: {question}")
    print("="*70 + "\n")

    # Get answer through multi-agent pipeline
    answer = system.ask(question)

    print(f"\n💼 STORE MANAGER'S ANSWER:")
    print("="*70)
    print(answer)
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
