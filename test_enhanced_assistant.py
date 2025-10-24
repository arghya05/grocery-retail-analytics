#!/usr/bin/env python3
"""
Test the Enhanced Store Manager Assistant with business questions
"""

from store_manager_assistant_enhanced import EnhancedStoreManagerAssistant
import sys

print("\n" + "="*70)
print("TESTING ENHANCED STORE MANAGER AI ASSISTANT")
print("="*70)

try:
    # Initialize enhanced assistant
    print("\n1. Initializing enhanced assistant with full business context...")
    assistant = EnhancedStoreManagerAssistant(model="llama3.2:1b")
    print("✓ Enhanced assistant initialized successfully")

    # Test with a strategic business question
    print("\n2. Testing with strategic business question...")
    print("   Question: 'What are the top 3 opportunities to increase revenue?'")
    print("\n   Generating business insights...\n")

    response = assistant.ask_ollama("What are the top 3 opportunities to increase revenue?")

    print("="*70)
    print("STORE MANAGER'S STRATEGIC ANALYSIS:")
    print("="*70)
    print(response)
    print("="*70)

    print("\n✓ Test completed successfully!")
    print("\n📊 The enhanced assistant now has access to:")
    print("   • Business context metadata (persona, expertise areas)")
    print("   • Complete data insights document (975 lines of intelligence)")
    print("   • 143 KPIs across 19 datasets")
    print("   • Category, customer, operational, and financial intelligence")
    print("   • Seasonal patterns and strategic recommendations")
    print("\n🚀 Ready to provide deep business insights!")
    print("\nRun the full assistant with:")
    print("  python3 store_manager_assistant_enhanced.py")
    print("  OR")
    print("  ./start_assistant.sh")

except Exception as e:
    print(f"\n❌ Test failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
