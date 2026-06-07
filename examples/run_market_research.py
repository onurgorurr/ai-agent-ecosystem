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

    console.print(Panel.fit("🤖 AI Market Research Agent", style="bold blue"))

    # Get business idea
    idea = console.input("\n[bold green]Enter your business idea:[/bold green] ")

    if not idea:
        idea = "AI-powered sustainable packaging marketplace"
        console.print(f"[yellow]Using default idea: {idea}[/yellow]")

    # Initialize orchestrator
    orchestrator = AgentOrchestrator()

    with console.status("[bold green]Researching market...[/bold green]"):
        # Run only market research phase
        market_data = await orchestrator._run_market_research(idea)

    # Display results
    console.print("\n[bold blue]📊 Market Research Results[/bold blue]\n")

    if isinstance(market_data, dict):
        console.print("[green]Market research completed successfully![/green]")
        # Save results to reports directory with timestamped filename
        reports_dir = PROJECT_ROOT / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_file = (
            reports_dir
            / f"market_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(market_data, f, indent=2, default=str)
        console.print(f"\nResults saved in: {report_file}")

        # Print some details if available
        if "industry_analysis" in market_data:
            analysis = market_data["industry_analysis"]
            console.print(f"\n[bold]Analysis:[/bold] {str(analysis)[:200]}...")

    console.print("\n[bold green]✅ Research complete![/bold green]")


if __name__ == "__main__":
    asyncio.run(main())
