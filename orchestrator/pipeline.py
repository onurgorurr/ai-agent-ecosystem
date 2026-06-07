"""
Pipeline - Defines workflow pipelines for agent execution
"""
from typing import Dict, List, Callable, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from loguru import logger
import asyncio


class PipelineStage(Enum):
    """Pipeline stages"""
    MARKET_RESEARCH = "market_research"
    OPPORTUNITY_IDENTIFICATION = "opportunity_identification"
    STRATEGY_DEVELOPMENT = "strategy_development"
    PRODUCT_DEVELOPMENT = "product_development"
    DEPLOYMENT = "deployment"


@dataclass
class PipelineStep:
    """Individual step in a pipeline"""
    name: str
    stage: PipelineStage
    agent_method: Callable
    depends_on: List[str] = None
    timeout_seconds: int = 600  # Increased default from 300s to 600s for LLM operations
    
    def __post_init__(self):
        if self.depends_on is None:
            self.depends_on = []


class Pipeline:
    """Manages execution of multi-stage agent pipelines"""
    
    def __init__(self, name: str):
        self.name = name
        self.steps: List[PipelineStep] = []
        self.results: Dict[str, Any] = {}
        self.status = "initialized"
        self.started_at = None
        self.completed_at = None
        logger.info(f"Pipeline '{name}' created")
    
    def add_step(self, step: PipelineStep):
        """Add a step to the pipeline"""
        self.steps.append(step)
        logger.info(f"Added step: {step.name} (Stage: {step.stage.value})")
    
    def add_steps(self, steps: List[PipelineStep]):
        """Add multiple steps to the pipeline"""
        for step in steps:
            self.add_step(step)
    
    async def execute(self) -> Dict[str, Any]:
        """Execute the pipeline"""
        self.status = "running"
        self.started_at = datetime.now()
        logger.info(f"Starting pipeline: {self.name}")
        
        # Group steps by stage
        stages = {}
        for step in self.steps:
            if step.stage not in stages:
                stages[step.stage] = []
            stages[step.stage].append(step)
        
        # Execute stages sequentially
        for stage in PipelineStage:
            if stage in stages:
                logger.info(f"Executing stage: {stage.value}")
                stage_steps = stages[stage]
                
                # Execute steps within stage (can be parallel if no dependencies)
                await self._execute_stage(stage, stage_steps)
        
        self.status = "completed"
        self.completed_at = datetime.now()
        duration = (self.completed_at - self.started_at).total_seconds()
        logger.info(f"Pipeline completed in {duration:.2f} seconds")
        
        return self.results
    
    async def _execute_stage(self, stage: PipelineStage, steps: List[PipelineStep]):
        """Execute all steps in a stage"""
        
        # Separate independent and dependent steps
        independent = [s for s in steps if not s.depends_on]
        dependent = [s for s in steps if s.depends_on]
        
        # Execute independent steps in parallel
        if independent:
            tasks = [self._execute_step(step) for step in independent]
            await asyncio.gather(*tasks)
        
        # Execute dependent steps
        for step in dependent:
            # Check dependencies
            deps_met = all(dep in self.results for dep in step.depends_on)
            if deps_met:
                await self._execute_step(step)
            else:
                logger.warning(f"Skipping {step.name}: dependencies not met")
    
    async def _execute_step(self, step: PipelineStep):
        """Execute a single pipeline step"""
        logger.info(f"Executing step: {step.name} (timeout: {step.timeout_seconds}s)")
        
        try:
            # Execute with timeout
            result = await asyncio.wait_for(
                step.agent_method(),
                timeout=step.timeout_seconds
            )
            self.results[step.name] = result
            logger.info(f"✅ Step completed: {step.name}")
            
        except asyncio.TimeoutError:
            error_msg = f"Step timed out after {step.timeout_seconds}s"
            logger.error(f"⏱️  {error_msg}: {step.name}")
            self.results[step.name] = {"error": error_msg, "status": "timeout"}
        except Exception as e:
            error_msg = f"Step failed: {str(e)}"
            logger.error(f"❌ {error_msg}: {step.name}")
            self.results[step.name] = {"error": error_msg, "status": "failed"}
    
    def get_results(self) -> Dict[str, Any]:
        """Get pipeline results"""
        return self.results
    
    def get_status(self) -> Dict[str, Any]:
        """Get pipeline status"""
        return {
            "name": self.name,
            "status": self.status,
            "steps_total": len(self.steps),
            "steps_completed": len(self.results),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }