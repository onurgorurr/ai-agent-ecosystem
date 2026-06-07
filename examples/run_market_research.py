#!/usr/bin/env python3
"""
Quick market research example
"""

import sys
import os
from pathlib import Path

# CRITICAL: Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Now import the rest
import asyncio
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


async def main():
    # Import here to ensure path is set first
    from orchestrator.execution_engine import AgentOrchestrator

    console.print(Panel.fit("🤖 AI Market Research - Business Idea Generator", style="bold blue"))

    # Get industry input
    industry = console.input("\n[bold green]Enter the industry to research (e.g., Healthcare, FinTech, EdTech):[/bold green] ")

    if not industry:
        industry = "SustainableTech"
        console.print(f"[yellow]Using default industry: {industry}[/yellow]")

    # Initialize orchestrator
    orchestrator = AgentOrchestrator()

    with console.status("[bold green]Analyzing industry and generating new business ideas...[/bold green]"):
        # Run industry-specific market research
        market_data = await orchestrator._run_industry_research(industry)

    # Display results
    console.print("\n[bold blue]📊 Market Research & Business Ideas for {industry}[/bold blue]\n")

    if isinstance(market_data, dict):
        console.print("[green]Market research and idea generation completed successfully![/green]")
        
        # Save results to reports directory with timestamped filename
        reports_dir = PROJECT_ROOT / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_file = (
            reports_dir
            / f"business_ideas_{industry}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(market_data, f, indent=2, default=str)
        console.print(f"\n✅ Results saved in: {report_file}")

        # Display generated business ideas
        if "business_ideas" in market_data:
            ideas = market_data.get("business_ideas", [])
            if isinstance(ideas, list) and ideas:
                console.print(f"\n[bold cyan]💡 Generated Business Ideas for {industry}:[/bold cyan]")
                for i, idea in enumerate(ideas[:5], 1):
                    if isinstance(idea, dict):
                        idea_name = idea.get("name", "Unnamed Idea")
                        description = idea.get("description", "No description")
                        market_size = idea.get("estimated_market_size", "Unknown")
                        console.print(f"\n  {i}. [bold]{idea_name}[/bold]")
                        console.print(f"     📝 {description}")
                        console.print(f"     💰 Market Size: {market_size}")

        # Print industry analysis summary
        if "industry_analysis" in market_data:
            analysis = market_data["industry_analysis"]
            if isinstance(analysis, dict):
                console.print(f"\n[bold cyan]📈 Industry Overview:[/bold cyan]")
                for key, value in analysis.items():
                    if key not in ["status", "error"]:
                        console.print(f"  • {key}: {value}")

    console.print("\n[bold green]✅ Research complete![/bold green]")


if __name__ == "__main__":
    asyncio.run(main())
