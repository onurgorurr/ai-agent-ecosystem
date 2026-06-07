#!/usr/bin/env python3
"""
Mock market research runner — generates a deterministic report without calling APIs.
"""

import asyncio
import json
import textwrap
from datetime import datetime
from pathlib import Path

from orchestrator.execution_engine import AgentOrchestrator


class MockAgent:
    def __init__(self, name=None):
        self.name = name or "mock"

    async def analyze_industry(self, idea):
        return {
            "market_overview": {
                "tam_billions": 10,
                "sam_billions": 5,
                "som_billions": 1,
                "current_cagr_percent": 8,
                "market_maturity": "growing",
            }
        }

    async def analyze_competitors(self, idea):
        return {"competitors": [{"company": "Acme", "market_share_percent": 20}]}

    async def analyze_consumers(self, idea):
        return {"insights": ["consumers prefer sustainability"]}

    async def scout_technology(self, idea):
        return {"technologies": ["biodegradable polymer", "recycling automation"]}


async def main():
    orchestrator = AgentOrchestrator()

    # Replace market research agents with mocks
    orchestrator.agents["trend_analyzer"] = MockAgent("trend")
    orchestrator.agents["competitor_analyzer"] = MockAgent("competitor")
    orchestrator.agents["consumer_insight"] = MockAgent("consumer")
    orchestrator.agents["technology_scout"] = MockAgent("tech")

    idea = "AI-powered sustainable packaging marketplace (mock run)"
    market_data = await orchestrator._run_market_research(idea)

    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Prepare printable content
    content = json.dumps(market_data, indent=2, default=str)

    # Try to create a PDF using matplotlib; fallback to text file saved with .pdf extension
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = reports_dir / f"market_research_mock_{timestamp}.pdf"

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig = plt.figure(figsize=(8.5, 11))
        fig.patch.set_facecolor("white")

        # Wrap the content for readability
        wrapped = "\n".join(textwrap.wrap(content, width=100))
        fig.text(
            0.01, 0.99, wrapped, ha="left", va="top", fontsize=8, family="monospace"
        )
        plt.axis("off")
        fig.savefig(pdf_path, bbox_inches="tight")
        plt.close(fig)

        print(f"Mock PDF report written to: {pdf_path}")

    except Exception as e:
        # Fallback: write plain text and name it .pdf so user can inspect
        fallback_path = reports_dir / f"market_research_mock_{timestamp}.pdf"
        with open(fallback_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(
            f"Could not generate binary PDF (matplotlib missing); wrote text to: {fallback_path}"
        )


if __name__ == "__main__":
    asyncio.run(main())
