"""
Tests for Pipeline Execution
"""
import pytest
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.pipeline import Pipeline, PipelineStep, PipelineStage
from orchestrator.execution_engine import AgentOrchestrator


class TestPipeline:
    """Test pipeline functionality"""
    
    def test_pipeline_creation(self):
        """Test pipeline initialization"""
        pipeline = Pipeline("Test Pipeline")
        assert pipeline.name == "Test Pipeline"
        assert pipeline.status == "initialized"
        assert len(pipeline.steps) == 0
    
    def test_add_step(self):
        """Test adding steps to pipeline"""
        pipeline = Pipeline("Test")
        
        async def mock_step():
            return {"result": "success"}
        
        step = PipelineStep(
            name="test_step",
            stage=PipelineStage.MARKET_RESEARCH,
            agent_method=mock_step
        )
        
        pipeline.add_step(step)
        assert len(pipeline.steps) == 1
        assert pipeline.steps[0].name == "test_step"
    
    @pytest.mark.asyncio
    async def test_pipeline_execution(self):
        """Test pipeline execution"""
        pipeline = Pipeline("Test Execution")
        
        async def step1():
            return {"data": "step1_complete"}
        
        async def step2():
            return {"data": "step2_complete"}
        
        pipeline.add_step(PipelineStep("step1", PipelineStage.MARKET_RESEARCH, step1))
        pipeline.add_step(PipelineStep("step2", PipelineStage.MARKET_RESEARCH, step2))
        
        results = await pipeline.execute()
        
        assert pipeline.status == "completed"
        assert "step1" in results
        assert "step2" in results
        assert results["step1"] == {"data": "step1_complete"}
    
    @pytest.mark.asyncio
    async def test_pipeline_with_dependencies(self):
        """Test pipeline with step dependencies"""
        pipeline = Pipeline("Test Dependencies")
        
        results_order = []
        
        async def step1():
            results_order.append("step1")
            return {"value": 1}
        
        async def step2():
            results_order.append("step2")
            return {"value": 2}
        
        pipeline.add_step(PipelineStep("step1", PipelineStage.MARKET_RESEARCH, step1))
        pipeline.add_step(
            PipelineStep("step2", PipelineStage.MARKET_RESEARCH, step2, depends_on=["step1"])
        )
        
        await pipeline.execute()
        
        # Step1 should execute before step2
        assert results_order[0] == "step1"
        assert results_order[1] == "step2"
    
    def test_pipeline_status(self):
        """Test pipeline status reporting"""
        pipeline = Pipeline("Status Test")
        status = pipeline.get_status()
        
        assert status["name"] == "Status Test"
        assert status["status"] == "initialized"
        assert status["steps_total"] == 0
        assert status["steps_completed"] == 0


class TestAgentOrchestrator:
    """Test orchestrator functionality"""
    
    def test_orchestrator_initialization(self):
        """Test orchestrator creation"""
        orchestrator = AgentOrchestrator()
        assert len(orchestrator.agents) > 0
        assert 'trend_analyzer' in orchestrator.agents
        assert 'product_manager' in orchestrator.agents
    
    @pytest.mark.asyncio
    async def test_market_research_execution(self):
        """Test market research phase execution"""
        orchestrator = AgentOrchestrator()
        
        # This test doesn't require API calls - it tests structure
        result = await orchestrator._run_market_research("test market")
        
        assert isinstance(result, dict)
        assert "industry_analysis" in result
        assert "competitive_landscape" in result
        assert "consumer_insights" in result
        assert "technology_assessment" in result


@pytest.mark.integration
class TestFullPipeline:
    """Full integration tests"""
    
    @pytest.mark.skipif(
        not __import__('os').getenv("OPENAI_API_KEY"),
        reason="OPENAI_API_KEY not set"
    )
    @pytest.mark.asyncio
    async def test_complete_pipeline(self):
        """Test complete pipeline execution"""
        orchestrator = AgentOrchestrator()
        
        result = await orchestrator.execute_pipeline("AI education platform")
        
        assert isinstance(result, dict)
        assert 'pipeline_id' in result
        assert 'summary' in result
        assert 'next_steps' in result