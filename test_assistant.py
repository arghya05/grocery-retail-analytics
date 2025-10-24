#!/usr/bin/env python3
"""
Quick test of the Store Manager Assistant
"""

from store_manager_assistant import StoreManagerAssistant
import sys

print("\n" + "="*70)
print("TESTING STORE MANAGER AI ASSISTANT")
print("="*70)

try:
    # Initialize assistant
    print("\n1. Initializing assistant...")
    assistant = StoreManagerAssistant(model="llama3.2:1b")
    print("✓ Assistant initialized successfully")

    # Test question
    print("\n2. Testing with a simple question...")
    print("   Question: 'What is our total revenue?'")
    print("\n   Generating response...\n")

    response = assistant.ask_ollama("What is our total revenue?")

    print("="*70)
    print("RESPONSE:")
    print("="*70)
    print(response)
    print("="*70)

    print("\n✓ Test completed successfully!")
    print("\nYou can now use the full assistant with:")
    print("  python store_manager_assistant.py")
    print("  OR")
    print("  ./start_assistant.sh")

except Exception as e:
    print(f"\n❌ Test failed: {str(e)}")
    sys.exit(1)
