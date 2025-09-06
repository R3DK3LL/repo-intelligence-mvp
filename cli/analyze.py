#!/usr/bin/env python3
"""
Repository Intelligence CLI Tool
Simple command-line interface for analyzing repositories
"""
import sys
import json
import click
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.analyzer import RepositoryAnalyzer
from collectors.github_collector import GitHubCollector


@click.command()
@click.argument("repo_url")
@click.option(
    "--threshold",
    "-t",
    default=0.7,
    type=float,
    help="Classification threshold (default: 0.7)",
)
@click.option(
    "--output",
    "-o",
    type=click.File("w"),
    default="-",
    help="Output file (default: stdout)",
)
@click.option(
    "--format",
    "output_format",
    default="json",
    type=click.Choice(["json", "summary"]),
    help="Output format (default: json)",
)
@click.option(
    "--github-token",
    envvar="GITHUB_TOKEN",
    help="GitHub API token (can also use GITHUB_TOKEN env var)",
)
def analyze(repo_url, threshold, output, output_format, github_token):
    """
    Analyze a GitHub repository using the Repository Intelligence System

    REPO_URL: GitHub repository URL (e.g., https://github.com/user/repo)

    Examples:
        python cli/analyze.py https://github.com/microsoft/vscode
        python cli/analyze.py https://github.com/user/repo -t 0.8 --format summary
    """

    click.echo(f"🔍 Analyzing repository: {repo_url}", err=True)

    try:
        # Initialize analyzer
        analyzer = RepositoryAnalyzer()

        # Show engine info
        engine_info = analyzer.get_engine_info()
        if not analyzer.proprietary_available:
            click.echo(
                "⚠️  Running in demo mode - install repo-intelligence-core for full analysis",
                err=True,
            )

        # Analyze repository
        result = analyzer.analyze_repository(repo_url, threshold)

        # Format output
        if output_format == "json":
            json.dump(result, output, indent=2)
        elif output_format == "summary":
            _print_summary(result, output)

        # Print status to stderr
        status = (
            "✅ HEALTHY"
            if result.get("classification") == "HEALTHY"
            else "⚠️  NEEDS ATTENTION"
        )
        click.echo(f"\n{status} (Score: {result.get('M_score', 'N/A')})", err=True)

    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


def _print_summary(result, output):
    """Print human-readable summary"""
    click.echo("=" * 50, file=output)
    click.echo("REPOSITORY INTELLIGENCE ANALYSIS", file=output)
    click.echo("=" * 50, file=output)

    # Basic info
    click.echo(f"Repository: {result.get('repository', 'N/A')}", file=output)
    click.echo(f"Classification: {result.get('classification', 'N/A')}", file=output)
    click.echo(f"Overall Score (M): {result.get('M_score', 'N/A'):.3f}", file=output)
    click.echo(f"Threshold: {result.get('threshold', 'N/A')}", file=output)

    # Metrics breakdown
    if "metrics" in result:
        click.echo("\nMETRICS BREAKDOWN:", file=output)
        click.echo("-" * 20, file=output)
        metrics = result["metrics"]
        click.echo(f"H (Commit Entropy): {metrics.get('H', 'N/A'):.3f}", file=output)
        click.echo(f"V (Velocity):       {metrics.get('V', 'N/A'):.3f}", file=output)
        click.echo(f"C (Collaboration):  {metrics.get('C', 'N/A'):.3f}", file=output)
        click.echo(f"A (Anti-patterns):  {metrics.get('A', 'N/A'):.3f}", file=output)

    # Recommendations
    if result.get("recommendations"):
        click.echo("\nRECOMMENDATIONS:", file=output)
        click.echo("-" * 15, file=output)
        for i, rec in enumerate(result["recommendations"], 1):
            click.echo(f"{i}. {rec}", file=output)

    # Demo mode warning
    if result.get("demo_mode"):
        click.echo("\n" + "!" * 50, file=output)
        click.echo(
            "DEMO MODE - Install repo-intelligence-core for real analysis", file=output
        )
        click.echo("!" * 50, file=output)


@click.command()
def info():
    """Show information about the Repository Intelligence System"""
    analyzer = RepositoryAnalyzer()
    engine_info = analyzer.get_engine_info()

    click.echo("Repository Intelligence System")
    click.echo("=" * 30)
    click.echo(f"Engine: {engine_info['engine']}")
    click.echo(f"Capabilities: {', '.join(engine_info['capabilities'])}")

    if "version" in engine_info:
        click.echo(f"Version: {engine_info['version']}")

    if "message" in engine_info:
        click.echo(f"\nNote: {engine_info['message']}")


# CLI group
@click.group()
def cli():
    """Repository Intelligence System CLI"""
    pass


cli.add_command(analyze)
cli.add_command(info)

if __name__ == "__main__":
    cli()
