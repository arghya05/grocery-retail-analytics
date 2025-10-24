#!/usr/bin/env python3
"""
Demo script to ask a question to the LangGraph Store Manager
- Uses the system programmatically (no CLI input needed)
- Demonstrates all 3 layers of context working together
"""

from langgraph_multi_agent_store_manager import LangGraphStoreManager

def main():
    print("\n" + "="*70)
    print("LANGGRAPH STORE MANAGER - DEMO QUESTION")
    print("="*70)

    # Initialize system (loads all data automatically)
    system = LangGraphStoreManager()

    # Example questions - change this to ask your own question
    questions = [
        "What are the top 3 revenue opportunities?",
        # Uncomment any of these to try different questions:
        # "How can we reduce perishable wastage?",
        # "Which customer segment should we prioritize?",
        # "Why is beverage performance strong?",
        # "What should we do about underperforming stores?",
    ]

    for question in questions:
        print(f"\n\n{'='*70}")
        print(f"QUESTION: {question}")
        print("="*70)

        # Get answer through multi-agent pipeline
        answer = system.ask(question)

        print(f"\n💼 STORE MANAGER'S ANSWER:")
        print("="*70)
        print(answer)
        print("="*70)

if __name__ == "__main__":
    main()
