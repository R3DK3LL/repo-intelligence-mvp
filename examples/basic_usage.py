#!/usr/bin/env python3
"""
Repository Intelligence System - Basic Usage Examples
Demonstrates how to use the system programmatically
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.analyzer import RepositoryAnalyzer
from collectors.github_collector import GitHubCollector


def example_single_analysis():
    """Example: Analyze a single repository"""
    print("=" * 50)
    print("SINGLE REPOSITORY ANALYSIS")
    print("=" * 50)

    # Initialize analyzer
    analyzer = RepositoryAnalyzer()

    # Analyze repository
    repo_url = "https://github.com/microsoft/vscode"
    print(f"Analyzing: {repo_url}")

    try:
        result = analyzer.analyze_repository(repo_url, threshold=0.7)

        print(f"\nClassification: {result['classification']}")
        print(f"Overall Score: {result['M_score']:.3f}")
        print(f"Demo Mode: {result.get('demo_mode', False)}")

        if "metrics" in result:
            print("\nMetrics:")
            for metric, value in result["metrics"].items():
                print(f"  {metric}: {value:.3f}")

    except Exception as e:
        print(f"Error: {e}")


def example_batch_analysis():
    """Example: Analyze multiple repositories"""
    print("\n" + "=" * 50)
    print("BATCH ANALYSIS")
    print("=" * 50)

    repos = [
        "https://github.com/microsoft/vscode",
        "https://github.com/facebook/react",
        "https://github.com/google/go",
        "https://github.com/rust-lang/rust",
    ]

    analyzer = RepositoryAnalyzer()
    results = []

    for repo_url in repos:
        try:
            print(f"Analyzing {repo_url}...")
            result = analyzer.analyze_repository(repo_url)
            results.append(
                {
                    "url": repo_url,
                    "score": result["M_score"],
                    "classification": result["classification"],
                }
            )
        except Exception as e:
            print(f"  Error: {e}")
            results.append({"url": repo_url, "score": None, "classification": "ERROR"})

    # Summary
    print(f"\nBATCH ANALYSIS SUMMARY:")
    print("-" * 30)
    for result in results:
        status = "✅" if result["classification"] == "HEALTHY" else "⚠️"
        score = f"{result['score']:.3f}" if result["score"] else "N/A"
        print(f"{status} {score} - {result['url']}")


def example_engine_info():
    """Example: Get engine information"""
    print("\n" + "=" * 50)
    print("ENGINE INFORMATION")
    print("=" * 50)

    analyzer = RepositoryAnalyzer()
    info = analyzer.get_engine_info()

    print(f"Engine: {info['engine']}")
    print(f"Capabilities: {', '.join(info['capabilities'])}")

    if "version" in info:
        print(f"Version: {info['version']}")

    if "message" in info:
        print(f"Note: {info['message']}")


def example_data_collection():
    """Example: Collect raw repository data"""
    print("\n" + "=" * 50)
    print("DATA COLLECTION EXAMPLE")
    print("=" * 50)

    collector = GitHubCollector()
    repo_url = "https://github.com/octocat/Hello-World"

    try:
        print(f"Collecting data from: {repo_url}")
        data = collector.extract_repo_data(repo_url)

        print(f"\nBasic Info:")
        basic = data["basic_info"]
        print(f"  Name: {basic['name']}")
        print(f"  Language: {basic['language']}")
        print(f"  Stars: {basic['stars']}")
        print(f"  Forks: {basic['forks']}")

        print(f"\nData Collected:")
        print(f"  Commits: {len(data['commits'])}")
        print(f"  Pull Requests: {len(data['pull_requests'])}")
        print(f"  Contributors: {len(data['contributors'])}")
        print(f"  Branches: {len(data['branches'])}")

    except Exception as e:
        print(f"Error collecting data: {e}")


def example_custom_threshold():
    """Example: Using custom threshold values"""
    print("\n" + "=" * 50)
    print("CUSTOM THRESHOLD ANALYSIS")
    print("=" * 50)

    analyzer = RepositoryAnalyzer()
    repo_url = "https://github.com/microsoft/vscode"

    thresholds = [0.5, 0.7, 0.9]

    print(f"Testing different thresholds on: {repo_url}")

    for threshold in thresholds:
        try:
            result = analyzer.analyze_repository(repo_url, threshold)
            print(
                f"  Threshold {threshold}: {result['classification']} (Score: {result['M_score']:.3f})"
            )
        except Exception as e:
            print(f"  Threshold {threshold}: Error - {e}")


if __name__ == "__main__":
    print("Repository Intelligence System - Basic Usage Examples")
    print("This demonstrates the core functionality of the system")

    example_engine_info()
    example_single_analysis()
    example_custom_threshold()
    example_batch_analysis()
    example_data_collection()

    print("\n" + "=" * 50)
    print("Examples completed!")
    print("For API usage, see: python -m uvicorn src.api.main:app --reload")
    print("For CLI usage, see: python cli/analyze.py --help")
