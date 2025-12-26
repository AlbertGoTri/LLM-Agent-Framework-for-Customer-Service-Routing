"""
Evaluation script for comparing LLM routing performance across different providers.
Measures accuracy, latency, and generates a comparison report.
"""

import os
import sys
from pathlib import Path
import time
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from project root
project_root = Path(__file__).parent.parent
load_dotenv(project_root / "environment.env")

# Add project root to path for imports
sys.path.insert(0, str(project_root))

from evaluation.test_data import get_test_cases
from src.router import initialize_client, route_query, DEFAULT_MODELS

# Providers to evaluate and their API key names
PROVIDERS = {
    "google": "GOOGLE_API_KEY",
    "groq": "GROQ_API_KEY"
}

# Rate limits per minute for free tier (to add delays)
RATE_LIMITS = {
    "google": 5,  # 5 requests per minute
    "groq": 30    # 30 requests per minute
}


def evaluate_provider(provider: str, test_cases: list) -> dict:
    """
    Evaluate a single provider on all test cases.
    Returns metrics including accuracy, latency, and detailed results.
    """
    results = {
        "provider": provider,
        "model": DEFAULT_MODELS.get(provider),
        "total": len(test_cases),
        "correct": 0,
        "incorrect": 0,
        "errors": 0,
        "accuracy": 0.0,
        "avg_latency_ms": 0.0,
        "total_latency_ms": 0.0,
        "details": []
    }
    
    try:
        initialize_client(provider)
    except Exception as e:
        print(f"  [ERROR] Failed to initialize {provider}: {e}")
        results["errors"] = len(test_cases)
        return results
    
    latencies = []
    
    # Calculate delay needed to respect rate limits
    rate_limit = RATE_LIMITS.get(provider, 60)
    delay_seconds = 60.0 / rate_limit + 0.5  # Add 0.5s buffer
    
    if rate_limit < 10:
        print(f"  [NOTE] Rate limit is {rate_limit}/min - adding {delay_seconds:.1f}s delay between requests")
    
    for i, test_case in enumerate(test_cases):
        query = test_case["query"]
        expected = test_case["expected"]
        
        # Add delay for rate-limited providers (after first request)
        if i > 0 and rate_limit < 10:
            time.sleep(delay_seconds)
        
        # Measure latency
        start_time = time.time()
        try:
            predicted = route_query(query)
            latency_ms = (time.time() - start_time) * 1000
            latencies.append(latency_ms)
            
            is_correct = predicted == expected
            if is_correct:
                results["correct"] += 1
            else:
                results["incorrect"] += 1
            
            results["details"].append({
                "query": query,
                "expected": expected,
                "predicted": predicted,
                "correct": is_correct,
                "latency_ms": round(latency_ms, 2)
            })
            
            # Progress indicator
            status = "OK" if is_correct else "FAIL"
            print(f"  [{i+1}/{len(test_cases)}] {status} {query[:50]}...")
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            results["errors"] += 1
            results["details"].append({
                "query": query,
                "expected": expected,
                "predicted": "ERROR",
                "correct": False,
                "latency_ms": round(latency_ms, 2),
                "error": str(e)
            })
            print(f"  [{i+1}/{len(test_cases)}] ERROR: {query[:40]}...")
    
    # Calculate metrics
    if latencies:
        results["avg_latency_ms"] = round(sum(latencies) / len(latencies), 2)
        results["total_latency_ms"] = round(sum(latencies), 2)
    
    results["accuracy"] = round(results["correct"] / results["total"] * 100, 2) if results["total"] > 0 else 0.0
    
    return results


def print_comparison_table(all_results: list):
    """Print a formatted comparison table of all providers."""
    print("\n" + "=" * 80)
    print("EVALUATION RESULTS SUMMARY")
    print("=" * 80)
    
    # Header
    print(f"\n{'Provider':<12} {'Model':<28} {'Accuracy':<12} {'Avg Latency':<15} {'Errors':<8}")
    print("-" * 80)
    
    # Sort by accuracy descending
    sorted_results = sorted(all_results, key=lambda x: x["accuracy"], reverse=True)
    
    for r in sorted_results:
        print(f"{r['provider'].upper():<12} {r['model']:<28} {r['accuracy']:>6.1f}%     {r['avg_latency_ms']:>8.0f} ms     {r['errors']:<8}")
    
    print("-" * 80)
    
    # Determine best model
    best = sorted_results[0]
    print(f"\nBEST MODEL: {best['provider'].upper()} ({best['model']})")
    print(f"   Accuracy: {best['accuracy']}% | Avg Latency: {best['avg_latency_ms']} ms")


def save_results(all_results: list, filename: str = None):
    """Save detailed results to a JSON file."""
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"evaluation_results_{timestamp}.json"
    
    filepath = results_dir / filename
    
    output = {
        "timestamp": datetime.now().isoformat(),
        "summary": [
            {
                "provider": r["provider"],
                "model": r["model"],
                "accuracy": r["accuracy"],
                "avg_latency_ms": r["avg_latency_ms"],
                "correct": r["correct"],
                "incorrect": r["incorrect"],
                "errors": r["errors"]
            }
            for r in all_results
        ],
        "detailed_results": all_results
    }
    
    with open(filepath, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nDetailed results saved to: {filepath}")


def main():
    """Main evaluation function."""
    print("=" * 80)
    print("LLM ROUTER EVALUATION")
    print("=" * 80)
    
    # Check which providers are available
    available_providers = []
    for provider, key_name in PROVIDERS.items():
        if os.getenv(key_name):
            available_providers.append(provider)
            print(f"[OK] {provider.upper()} - API key found")
        else:
            print(f"[--] {provider.upper()} - API key not found ({key_name})")
    
    if not available_providers:
        print("\n[ERROR] No API keys found. Please configure environment.env file.")
        sys.exit(1)
    
    # Allow specifying providers via command line
    if len(sys.argv) > 1:
        requested = [p.lower() for p in sys.argv[1:]]
        available_providers = [p for p in requested if p in available_providers]
        if not available_providers:
            print(f"\n[ERROR] None of the requested providers are available.")
            sys.exit(1)
    
    print(f"\nEvaluating providers: {', '.join(p.upper() for p in available_providers)}")
    
    # Get test cases
    test_cases = get_test_cases()
    print(f"Test cases: {len(test_cases)}")
    
    # Evaluate each provider
    all_results = []
    for provider in available_providers:
        print(f"\n{'-' * 40}")
        print(f"Evaluating: {provider.upper()} ({DEFAULT_MODELS.get(provider)})")
        print(f"{'-' * 40}")
        
        results = evaluate_provider(provider, test_cases)
        all_results.append(results)
    
    # Print comparison table
    print_comparison_table(all_results)
    
    # Save results
    save_results(all_results)
    
    # Print incorrect predictions for analysis
    print("\n" + "=" * 80)
    print("INCORRECT PREDICTIONS (for analysis)")
    print("=" * 80)
    
    for r in all_results:
        incorrect = [d for d in r["details"] if not d["correct"]]
        if incorrect:
            print(f"\n{r['provider'].upper()}:")
            for d in incorrect:
                print(f"  Query: {d['query']}")
                print(f"  Expected: {d['expected']} | Predicted: {d['predicted']}")
                print()


if __name__ == "__main__":
    main()
