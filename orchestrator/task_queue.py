"""
Task Queue - Celery-based task queue for background agent execution
"""
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
from loguru import logger
import asyncio
import json
from pathlib import Path

# Initialize Celery
celery_app = Celery(
    'ai_agent_tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_max_tasks_per_child=100,
    worker_prefetch_multiplier=1
)

# Configure periodic tasks
celery_app.conf.beat_schedule = {
    'daily-market-scan': {
        'task': 'orchestrator.task_queue.daily_market_scan',
        'schedule': crontab(hour=6, minute=0),  # 6 AM daily
    },
    'weekly-competitor-update': {
        'task': 'orchestrator.task_queue.weekly_competitor_update',
        'schedule': crontab(hour=7, minute=0, day_of_week=1),  # Monday 7 AM
    },
    'hourly-health-check': {
        'task': 'orchestrator.task_queue.health_check',
        'schedule': timedelta(hours=1),
    },
}


@celery_app.task(name='orchestrator.task_queue.run_market_research')
def run_market_research(idea: str, industries: list = None):
    """
    Run market research as a background task
    
    Args:
        idea: Business idea to research
        industries: List of industries to analyze
    """
    logger.info(f"Starting market research task for: {idea}")
    
    from orchestrator.execution_engine import AgentOrchestrator
    
    async def _run():
        orchestrator = AgentOrchestrator()
        result = await orchestrator._run_market_research(idea)
        return result
    
    result = asyncio.run(_run())
    
    # Save results
    output_path = Path("reports") / f"task_{run_market_research.request.id}.json"
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    logger.info(f"Market research task completed: {output_path}")
    return {"status": "completed", "output_file": str(output_path)}


@celery_app.task(name='orchestrator.task_queue.run_full_pipeline')
def run_full_pipeline(idea: str):
    """
    Run complete pipeline as background task
    
    Args:
        idea: Business idea to analyze and develop
    """
    logger.info(f"Starting full pipeline task for: {idea}")
    
    from orchestrator.execution_engine import AgentOrchestrator
    
    async def _run():
        orchestrator = AgentOrchestrator()
        result = await orchestrator.execute_pipeline(idea)
        return result
    
    result = asyncio.run(_run())
    
    logger.info(f"Full pipeline task completed: {result.get('pipeline_id')}")
    return {
        "status": "completed",
        "pipeline_id": result.get('pipeline_id'),
        "summary": result.get('summary')
    }


@celery_app.task(name='orchestrator.task_queue.generate_product_code')
def generate_product_code(prd: dict):
    """
    Generate product code from PRD as background task
    
    Args:
        prd: Product Requirements Document
    """
    logger.info("Starting code generation task")
    
    from agents.product_dev.code_generator import CodeGenerationAgent
    
    async def _run():
        agent = CodeGenerationAgent()
        result = await agent.generate_fullstack_app(prd)
        return result
    
    result = asyncio.run(_run())
    
    logger.info(f"Code generation completed: {result.get('project_name')}")
    return {"status": "completed", "project": result}


@celery_app.task(name='orchestrator.task_queue.daily_market_scan')
def daily_market_scan():
    """
    Daily automated market scan for trending opportunities
    """
    logger.info("Running daily market scan")
    
    from orchestrator.execution_engine import AgentOrchestrator
    
    async def _run():
        orchestrator = AgentOrchestrator()
        
        # Scan trending industries
        trending = ["AI/ML", "Climate Tech", "Health Tech", "Fintech"]
        results = {}
        
        for industry in trending:
            logger.info(f"Scanning industry: {industry}")
            market_data = await orchestrator._run_market_research(industry)
            results[industry] = market_data
        
        return results
    
    results = asyncio.run(_run())
    
    # Save daily scan
    from datetime import datetime
    output_path = Path("reports") / f"daily_scan_{datetime.now().strftime('%Y%m%d')}.json"
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info(f"Daily scan completed: {output_path}")
    return {"status": "completed", "file": str(output_path)}


@celery_app.task(name='orchestrator.task_queue.weekly_competitor_update')
def weekly_competitor_update():
    """
    Weekly competitor landscape update
    """
    logger.info("Running weekly competitor update")
    
    from agents.market_research.competitor_analyzer import CompetitorAnalysisAgent
    
    async def _run():
        agent = CompetitorAnalysisAgent()
        result = await agent.analyze_competitors("Technology")
        return result
    
    result = asyncio.run(_run())
    
    from datetime import datetime
    output_path = Path("reports") / f"competitor_update_{datetime.now().strftime('%Y%m%d')}.json"
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    logger.info(f"Weekly competitor update completed: {output_path}")
    return {"status": "completed", "file": str(output_path)}


@celery_app.task(name='orchestrator.task_queue.health_check')
def health_check():
    """
    Hourly health check for all agents and services
    """
    logger.info("Running health check")
    
    from config.settings import settings
    
    health_status = {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "openai_api": bool(settings.OPENAI_API_KEY),
        "redis_url": settings.REDIS_URL,
        "database_url": settings.DATABASE_URL
    }
    
    # Check if reports directory is writable
    reports_dir = Path("reports")
    health_status["reports_writable"] = reports_dir.exists() and os.access(reports_dir, os.W_OK)
    
    logger.info(f"Health check: {health_status}")
    return health_status