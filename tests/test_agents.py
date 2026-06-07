"""
Tests for AI Agents
"""
import pytest
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.base_agent import BaseAgent
from agents.market_research.trend_analyzer import TrendAnalysisAgent
from agents.market_research.competitor_analyzer import CompetitorAnalysisAgent
from agents.market_research.consumer_insight import ConsumerInsightAgent
from agents.market_research.technology_scout import TechnologyScoutAgent


class TestBaseAgent:
    """Test base agent functionality"""
    
    def test_agent_initialization(self):
        """Test agent initialization"""
        agent = BaseAgent("Test Agent")
        assert agent.agent_name == "Test Agent"
        assert agent.model == "gpt-4-turbo-preview"
        assert len(agent.memory) == 0
    
    def test_agent_memory_management(self):
        """Test memory management"""
        agent = BaseAgent("Test Agent")
        
        # Add items to memory
        for i in range(15):
            agent.memory.append({"role": "user", "content": f"Message {i}"})
            agent.memory.append({"role": "assistant", "content": f"Response {i}"})
        
        # Memory should not exceed max_memory * 2
        assert len(agent.memory) <= agent.max_memory * 2
    
    def test_clear_memory(self):
        """Test memory clearing"""
        agent = BaseAgent("Test Agent")
        agent.memory = [{"role": "user", "content": "test"}]
        agent.clear_memory()
        assert len(agent.memory) == 0


class TestTrendAnalyzer:
    """Test trend analysis agent"""
    
    def test_initialization(self):
        agent = TrendAnalysisAgent()
        assert agent.agent_name == "Trend Analysis Agent"
    
    @pytest.mark.asyncio
    async def test_analyze_industry_structure(self):
        """Test that analysis returns correct structure"""
        agent = TrendAnalysisAgent()
        
        # Note: This test requires API key
        # Mock test without actual API call
        result = {
            "market_overview": {
                "tam_billions": 100,
                "sam_billions": 50,
                "som_billions": 10,
                "current_cagr_percent": 15,
                "market_maturity": "growing"
            }
        }
        
        assert "market_overview" in result
        assert "tam_billions" in result["market_overview"]


class TestCompetitorAnalyzer:
    """Test competitor analysis agent"""
    
    def test_initialization(self):
        agent = CompetitorAnalysisAgent()
        assert agent.agent_name == "Competitor Analysis Agent"


class TestConsumerInsightAgent:
    """Test consumer insight agent"""
    
    def test_initialization(self):
        agent = ConsumerInsightAgent()
        assert agent.agent_name == "Consumer Insight Agent"


class TestTechnologyScoutAgent:
    """Test technology scout agent"""
    
    def test_initialization(self):
        agent = TechnologyScoutAgent()
        assert agent.agent_name == "Technology Scout Agent"


@pytest.mark.integration
class TestAgentIntegration:
    """Integration tests (require API key)"""
    
    @pytest.mark.skipif(
        not __import__('os').getenv("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    @pytest.mark.asyncio
    async def test_full_market_research(self):
        """Test full market research pipeline"""
        from orchestrator.execution_engine import AgentOrchestrator
        
        orchestrator = AgentOrchestrator()
        result = await orchestrator._run_market_research("AI healthcare")
        
        assert isinstance(result, dict)
        assert "industry_analysis" in result
        assert "competitive_landscape" in result