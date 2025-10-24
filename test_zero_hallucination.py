#!/usr/bin/env python3
"""
Test script for Zero-Hallucination Store Manager
Tests problematic questions that previously caused hallucinations
"""

import sys
import json

# Test questions that previously caused hallucinations
TEST_QUESTIONS = [
    {
        "question": "What are the stores that are not performing?",
        "expected_features": [
            "Specific store IDs (STR_XXX)",
            "Exact revenue numbers",
            "Comparison with data",
            "No generic advice"
        ],
        "hallucination_risks": [
            "Generic statements without store IDs",
            "Made-up percentages",
            "Typos like 'Occasiall'",
            "Recommendations without data"
        ]
    },
    {
        "question": "What are the top 5 stores by revenue?",
        "expected_features": [
            "Exactly 5 store IDs",
            "Revenue in ₹M format",
            "Sorted by revenue",
            "Exact numbers from data"
        ],
        "hallucination_risks": [
            "Wrong store IDs",
            "Incorrect revenue numbers",
            "More or less than 5 stores",
            "Unsorted list"
        ]
    },
    {
        "question": "Which customer segment should we prioritize and why?",
        "expected_features": [
            "Segment names from data",
            "Customer counts",
            "Average transaction values",
            "Calculated revenue opportunity"
        ],
        "hallucination_risks": [
            "Made-up segment names",
            "Incorrect customer counts",
            "Generic recommendations",
            "No quantified impact"
        ]
    },
    {
        "question": "How is Beverages category performing?",
        "expected_features": [
            "Total revenue",
            "Transaction count",
            "Average transaction value",
            "Comparison with other categories"
        ],
        "hallucination_risks": [
            "Made-up revenue numbers",
            "Incorrect percentages",
            "Generic category insights",
            "No specific metrics"
        ]
    },
    {
        "question": "What is the revenue gap between top and bottom stores?",
        "expected_features": [
            "Top store ID and revenue",
            "Bottom store ID and revenue",
            "Calculated gap",
            "Percentage difference"
        ],
        "hallucination_risks": [
            "Wrong store identification",
            "Incorrect calculations",
            "Made-up gap numbers",
            "No verification"
        ]
    }
]


def validate_answer_format(answer: str, test_case: dict) -> dict:
    """Validate that answer meets expectations and avoids hallucinations"""

    results = {
        "has_specific_data": False,
        "has_verified_badge": False,
        "no_generic_advice": True,
        "no_typos": True,
        "issues": []
    }

    # Check for verified badge
    if "100% Data-Backed" in answer or "verified" in answer.lower():
        results["has_verified_badge"] = True
    else:
        results["issues"].append("Missing verification badge")

    # Check for specific data citations
    has_store_ids = "STR_" in answer
    has_numbers = "₹" in answer or any(char.isdigit() for char in answer)

    if has_store_ids or has_numbers:
        results["has_specific_data"] = True
    else:
        results["issues"].append("No specific data citations found")

    # Check for generic advice patterns
    generic_patterns = [
        "we should improve",
        "consider implementing",
        "focus on better",
        "enhance the",
        "some stores",
        "various categories"
    ]

    for pattern in generic_patterns:
        if pattern in answer.lower():
            results["no_generic_advice"] = False
            results["issues"].append(f"Generic advice found: '{pattern}'")

    # Check for common typos/hallucinations
    typo_patterns = ["occasiall", "bevrage", "cusotmer"]
    for typo in typo_patterns:
        if typo in answer.lower():
            results["no_typos"] = False
            results["issues"].append(f"Typo/hallucination found: '{typo}'")

    return results


def run_test(system, test_case: dict) -> dict:
    """Run a single test case"""

    print("\n" + "="*80)
    print(f"TEST: {test_case['question']}")
    print("="*80)

    print("\n📋 Expected Features:")
    for feature in test_case['expected_features']:
        print(f"  ✓ {feature}")

    print("\n⚠️  Hallucination Risks:")
    for risk in test_case['hallucination_risks']:
        print(f"  • {risk}")

    print("\n🤖 Asking system...")
    print("-" * 80)

    try:
        answer = system.ask(test_case['question'])

        print("\n💼 ANSWER:")
        print("-" * 80)
        print(answer)
        print("-" * 80)

        # Validate answer
        validation = validate_answer_format(answer, test_case)

        print("\n✅ VALIDATION RESULTS:")
        print(f"  • Has Specific Data: {validation['has_specific_data']}")
        print(f"  • Has Verified Badge: {validation['has_verified_badge']}")
        print(f"  • No Generic Advice: {validation['no_generic_advice']}")
        print(f"  • No Typos: {validation['no_typos']}")

        if validation['issues']:
            print("\n⚠️  ISSUES FOUND:")
            for issue in validation['issues']:
                print(f"  • {issue}")

        # Overall score
        score = sum([
            validation['has_specific_data'],
            validation['has_verified_badge'],
            validation['no_generic_advice'],
            validation['no_typos']
        ])

        print(f"\n📊 SCORE: {score}/4")

        return {
            "question": test_case['question'],
            "answer": answer,
            "validation": validation,
            "score": score,
            "passed": score >= 3
        }

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

        return {
            "question": test_case['question'],
            "error": str(e),
            "passed": False
        }


def run_all_tests():
    """Run all test cases"""

    print("\n" + "="*80)
    print("ZERO-HALLUCINATION SYSTEM TEST SUITE")
    print("="*80)
    print(f"\nRunning {len(TEST_QUESTIONS)} test cases...")

    # Import the system
    try:
        from langgraph_multi_agent_store_manager_validated import ZeroHallucinationStoreManager
        system = ZeroHallucinationStoreManager()
    except Exception as e:
        print(f"\n❌ Failed to import system: {e}")
        print("\nMake sure langgraph_multi_agent_store_manager_validated.py is in the same directory")
        sys.exit(1)

    # Run all tests
    results = []
    for i, test_case in enumerate(TEST_QUESTIONS, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}/{len(TEST_QUESTIONS)}")
        print(f"{'='*80}")

        result = run_test(system, test_case)
        results.append(result)

        # Brief pause between tests
        import time
        time.sleep(2)

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    passed = sum(1 for r in results if r.get('passed', False))
    total = len(results)

    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Success Rate: {passed/total*100:.1f}%")

    print("\n📊 DETAILED RESULTS:")
    for i, result in enumerate(results, 1):
        status = "✅ PASS" if result.get('passed', False) else "❌ FAIL"
        score = result.get('score', 0)
        print(f"\n{i}. {status} ({score}/4)")
        print(f"   Q: {result['question']}")

        if 'validation' in result:
            validation = result['validation']
            if validation['issues']:
                print(f"   Issues: {', '.join(validation['issues'][:2])}")

    # Save results
    with open('test_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Detailed results saved to test_results.json")

    return passed == total


def run_single_test(question: str):
    """Run a single custom test"""

    print("\n" + "="*80)
    print("SINGLE QUESTION TEST")
    print("="*80)

    try:
        from langgraph_multi_agent_store_manager_validated import ZeroHallucinationStoreManager
        system = ZeroHallucinationStoreManager()
    except Exception as e:
        print(f"\n❌ Failed to import system: {e}")
        sys.exit(1)

    test_case = {
        "question": question,
        "expected_features": ["Specific data", "Verified claims"],
        "hallucination_risks": ["Generic advice", "Made-up numbers"]
    }

    result = run_test(system, test_case)

    if result.get('passed'):
        print("\n✅ Test PASSED")
        return True
    else:
        print("\n❌ Test FAILED")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Run single test with custom question
        question = " ".join(sys.argv[1:])
        success = run_single_test(question)
    else:
        # Run all tests
        success = run_all_tests()

    sys.exit(0 if success else 1)
