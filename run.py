#!/usr/bin/env python3
"""
Main entry point for AI Agent Ecosystem
"""
import sys
from pathlib import Path

# CRITICAL: Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

import argparse
import asyncio
from config.settings import settings
from orchestrator.execution_engine import AgentOrchestrator

def parse_args():
    parser = argparse.ArgumentParser(description="AI Agent Ecosystem")
    parser.add_argument("--mode", choices=["api", "cli", "dashboard", "pipeline"], default="cli")
    parser.add_argument("--idea", type=str, help="Business idea to analyze")
    parser.add_argument("--industry", type=str, help="Industry to analyze")
    return parser.parse_args()

async def run_cli(idea: str = None):
    from rich.console import Console
    from rich.prompt import Prompt
    
    console = Console()
    console.print("[bold blue]🤖 AI Agent Ecosystem[/bold blue]")
    
    if not idea:
        idea = Prompt.ask("Enter your business idea")
    
    orchestrator = AgentOrchestrator()
    
    with console.status("[bold green]Running pipeline..."):
        result = await orchestrator.execute_pipeline(idea)
    
    console.print("\n[bold green]✅ Pipeline Complete![/bold green]")
    console.print(f"\n📁 Report: reports/{result['pipeline_id']}.json")

def run_api():
    import uvicorn
    from api.server import app
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT, log_level=settings.LOG_LEVEL.lower())

def run_dashboard():
    import subprocess
    subprocess.run(["streamlit", "run", str(PROJECT_ROOT / "monitoring" / "dashboard.py")])

async def main():
    args = parse_args()
    
    if args.mode == "api":
        run_api()
    elif args.mode == "dashboard":
        run_dashboard()
    else:
        try:
            await run_cli(args.idea)
        except Exception as e:
            from rich.console import Console
            console = Console()
            console.print(f"[bold red]❌ Error:[/bold red] {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())