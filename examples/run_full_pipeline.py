#!/usr/bin/env python3
"""
Run complete AI Agent pipeline
"""
import sys
from pathlib import Path

# CRITICAL: Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import asyncio
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
import json
from datetime import datetime

console = Console()

async def main():
    from orchestrator.execution_engine import AgentOrchestrator
    
    console.print(Panel.fit(
        "🚀 AI Agent Ecosystem - Full Pipeline Execution",
        style="bold blue"
    ))
    
    idea = console.input("\n[bold green]Enter your business idea:[/bold green] ")
    
    if not idea:
        idea = "AI-powered personalized learning platform"
        console.print(f"[yellow]Using: {idea}[/yellow]")
    
    orchestrator = AgentOrchestrator()
    
    with Progress() as progress:
        task = progress.add_task("[green]Running pipeline...", total=4)
        
        console.print("\n[bold]Phase 1/4:[/bold] Market Research & Analysis")
        market_data = await orchestrator._run_market_research(idea)
        progress.update(task, advance=1)
        
        console.print("[bold]Phase 2/4:[/bold] Opportunity Identification")
        opportunities = await orchestrator._identify_opportunities(market_data)
        progress.update(task, advance=1)
        
        console.print("[bold]Phase 3/4:[/bold] Strategy Development")
        strategy = await orchestrator._develop_strategy(opportunities, market_data)
        progress.update(task, advance=1)
        
        console.print("[bold]Phase 4/4:[/bold] Product Development")
        product = await orchestrator._develop_product(strategy)
        progress.update(task, advance=1)
    
    results = {
        'pipeline_id': f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'business_idea': idea,
        'market_research': market_data,
        'opportunities': opportunities,
        'strategy': strategy,
        'product': product
    }
    
    report_path = Path("reports") / f"{results['pipeline_id']}.json"
    report_path.parent.mkdir(exist_ok=True)
    
    # Convert to serializable format
    def convert_to_serializable(obj):
        if hasattr(obj, '__dict__'):
            return str(obj)
        return obj
    
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2, default=convert_to_serializable)
    
    console.print(Panel.fit(
        f"✅ Pipeline Complete!\n\n"
        f"📁 Report: {report_path}\n"
        f"💻 Generated Code: generated_projects/",
        style="bold green"
    ))
    
    console.print("\n[bold cyan]Next Steps:[/bold cyan]")
    console.print("1. Review market research in reports/")
    console.print("2. Check generated code in generated_projects/")
    console.print("3. Validate business opportunities")
    console.print("4. Start MVP development")

if __name__ == "__main__":
    asyncio.run(main())