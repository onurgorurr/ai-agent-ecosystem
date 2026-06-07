#!/usr/bin/env python3
"""
AI-Powered Business Idea Discovery Tool
Generates innovative business ideas for a given industry with detailed market analysis
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
from rich.syntax import Syntax
from rich.progress import track

console = Console()


def display_business_idea(idea: dict, index: int):
    """Display a business idea in a formatted way"""
    console.print(f"\n[bold cyan]💡 Idea #{index}: {idea.get('name', 'Unnamed')}[/bold cyan]")
    console.print(f"   [yellow]Problem:[/yellow] {idea.get('problem_statement', 'N/A')}")
    console.print(f"   [green]Solution:[/green] {idea.get('solution', 'N/A')}")
    console.print(f"   [magenta]Value Prop:[/magenta] {idea.get('value_proposition', 'N/A')}")
    
    # Display key metrics
    console.print(f"\n   [bold]Key Metrics:[/bold]")
    console.print(f"   • Market Size: {idea.get('estimated_market_size', 'Unknown')}")
    console.print(f"   • TAM: ${idea.get('tam_billions', 0):.1f}B")
    console.print(f"   • Revenue Model: {idea.get('revenue_model', 'Unknown')}")
    console.print(f"   • Competition Level: {idea.get('competition_level', 'N/A')}")
    console.print(f"   • Time to Market: {idea.get('time_to_market_months', 'Unknown')} months")
    
    # Display scoring
    console.print(f"\n   [bold]Opportunity Scores:[/bold]")
    innovation = idea.get('innovation_score', 0)
    feasibility = idea.get('feasibility_score', 0)
    attractiveness = idea.get('market_attractiveness_score', 0)
    overall = idea.get('overall_opportunity_score', 0)
    
    console.print(f"   • Innovation: {'█' * innovation}{'░' * (10 - innovation)} {innovation}/10")
    console.print(f"   • Feasibility: {'█' * feasibility}{'░' * (10 - feasibility)} {feasibility}/10")
    console.print(f"   • Market Attractiveness: {'█' * attractiveness}{'░' * (10 - attractiveness)} {attractiveness}/10")
    console.print(f"   • Overall Score: {'█' * overall}{'░' * (10 - overall)} {overall}/10")
    
    # Display target segments
    segments = idea.get('target_segments', [])
    if segments:
        console.print(f"\n   [bold]Target Segments:[/bold]")
        for segment in segments[:3]:
            console.print(f"   • {segment}")
    
    # Display key differentiators
    differentiators = idea.get('key_differentiators', [])
    if differentiators:
        console.print(f"\n   [bold]Key Differentiators:[/bold]")
        for diff in differentiators[:3]:
            console.print(f"   • {diff}")
    
    # Display GTM strategy
    if idea.get('gtm_strategy'):
        console.print(f"\n   [bold]GTM Strategy:[/bold]")
        console.print(f"   {idea.get('gtm_strategy')}")


def display_industry_insights(insights: dict):
    """Display industry insights"""
    console.print(f"\n[bold magenta]📊 Industry Insights[/bold magenta]")
    
    # Key trends
    trends = insights.get('key_trends', [])
    if trends:
        console.print(f"\n[bold cyan]Key Trends:[/bold cyan]")
        for trend in trends[:5]:
            console.print(f"  • {trend}")
    
    # Market gaps
    gaps = insights.get('market_gaps', [])
    if gaps:
        console.print(f"\n[bold yellow]Market Gaps:[/bold yellow]")
        for gap in gaps[:5]:
            console.print(f"  • {gap}")
    
    # Emerging opportunities
    opportunities = insights.get('emerging_opportunities', [])
    if opportunities:
        console.print(f"\n[bold green]Emerging Opportunities:[/bold green]")
        for opp in opportunities[:5]:
            console.print(f"  • {opp}")
    
    # Technology enablers
    tech = insights.get('technology_enablers', [])
    if tech:
        console.print(f"\n[bold blue]Technology Enablers:[/bold blue]")
        for t in tech[:5]:
            console.print(f"  • {t}")
    
    # Customer pain points
    pains = insights.get('customer_pain_points', [])
    if pains:
        console.print(f"\n[bold red]Customer Pain Points:[/bold red]")
        for pain in pains[:5]:
            console.print(f"  • {pain}")


def display_top_recommendation(rec: dict):
    """Display top recommendation"""
    console.print(f"\n[bold green]🎯 Top Recommended Idea[/bold green]")
    console.print(f"[bold cyan]{rec.get('idea_name', 'N/A')}[/bold cyan]")
    console.print(f"\n[bold]Why pursue this:[/bold]")
    console.print(f"{rec.get('why_pursue_this', 'N/A')}")
    
    steps = rec.get('next_validation_steps', [])
    if steps:
        console.print(f"\n[bold]Next Validation Steps:[/bold]")
        for i, step in enumerate(steps[:5], 1):
            console.print(f"  {i}. {step}")


async def main():
    """Main function"""
    from orchestrator.execution_engine import AgentOrchestrator

    console.print(Panel.fit("🚀 AI Business Idea Discovery Engine", style="bold blue"))
    console.print("\n[cyan]Generate innovative business ideas for your industry[/cyan]\n")

    # Get industry input
    industry = console.input("[bold green]Enter the industry to analyze (e.g., Healthcare, FinTech, EdTech, AgriTech, ClimaTech):[/bold green] ")

    if not industry:
        industry = "ClimaTech"
        console.print(f"[yellow]Using default industry: {industry}[/yellow]")

    # Optional: Get specific focus
    focus = console.input(f"\n[bold green]Any specific focus area within {industry}? (optional, press Enter to skip):[/bold green] ")
    if focus:
        industry = f"{industry} - {focus}"

    # Initialize orchestrator
    orchestrator = AgentOrchestrator()

    console.print(f"\n[bold cyan]Analyzing {industry} industry and generating business ideas...[/bold cyan]\n")

    with console.status("[bold green]🔍 Running market analysis...[/bold green]"):
        # Run industry-specific market research and idea generation
        research_data = await orchestrator._run_industry_research(industry)

    # Display results
    console.print(Panel(f"📈 Market Research Results for {industry}", style="bold blue"))

    if isinstance(research_data, dict):
        console.print("\n[green]✅ Market analysis and idea generation completed successfully![/green]")

        # Save results to reports directory
        reports_dir = PROJECT_ROOT / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        industry_safe = industry.replace(" ", "_").replace("-", "_")
        report_file = reports_dir / f"business_ideas_{industry_safe}_{timestamp}.json"
        
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(research_data, f, indent=2, default=str)
        
        console.print(f"\n✅ [green]Full report saved to:[/green] {report_file}")

        # Display industry insights
        if "industry_analysis" in research_data:
            analysis = research_data.get("industry_analysis", {})
            if isinstance(analysis, dict) and "status" not in analysis:
                console.print(f"\n[bold magenta]📊 Industry Analysis[/bold magenta]")
                for key, value in list(analysis.items())[:5]:
                    console.print(f"  • {key}: {str(value)[:100]}")

        # Display business ideas
        ideas = research_data.get("business_ideas", [])
        if isinstance(ideas, list) and ideas:
            console.print(f"\n[bold cyan]{'=' * 80}[/bold cyan]")
            console.print(f"[bold cyan]💡 Generated Business Ideas ({len(ideas)} ideas)[/bold cyan]")
            console.print(f"[bold cyan]{'=' * 80}[/bold cyan]")
            
            # Display each idea
            for i, idea in enumerate(ideas[:10], 1):
                if isinstance(idea, dict):
                    display_business_idea(idea, i)
                    
                    if i < len(ideas):
                        console.print(f"\n[dim]{'─' * 80}[/dim]")

        # Display industry insights
        full_response = research_data
        if isinstance(full_response, dict):
            # Try to find insights in the response
            for key in ['industry_insights', 'insights', 'analysis']:
                if key in full_response and isinstance(full_response[key], dict):
                    display_industry_insights(full_response[key])
                    break

        # Display top recommendation
        for key in ['top_recommendation', 'recommendation', 'best_idea']:
            if key in full_response and isinstance(full_response[key], dict):
                display_top_recommendation(full_response[key])
                break

    else:
        console.print("[red]Error: Invalid response from market research[/red]")
        console.print(research_data)

    console.print(f"\n[bold green]{'=' * 80}[/bold green]")
    console.print("[bold green]✅ Business idea discovery complete![/bold green]")
    console.print(f"[bold green]{'=' * 80}[/bold green]")
    console.print(f"\n[cyan]Next Steps:[/cyan]")
    console.print(f"  1. Review the generated ideas above")
    console.print(f"  2. Check the full report: {report_file}")
    console.print(f"  3. Validate top ideas with potential customers")
    console.print(f"  4. Develop a detailed business plan for your chosen idea")


if __name__ == "__main__":
    asyncio.run(main())
