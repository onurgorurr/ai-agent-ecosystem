"""
API Routes - All API endpoints
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from fastapi.responses import JSONResponse, FileResponse
from loguru import logger
from pathlib import Path
from typing import Optional, List
from datetime import datetime
import json

from .schemas import (
    BusinessIdea, PipelineResponse, MarketResearchResponse,
    OpportunityResponse, StrategyResponse, ProductResponse,
    ErrorResponse
)
from orchestrator.execution_engine import AgentOrchestrator

router = APIRouter()


@router.post("/research", response_model=MarketResearchResponse, tags=["Research"])
async def research_market(idea: BusinessIdea):
    """
    Run market research for a business idea
    """
    logger.info(f"Market research requested for: {idea.idea}")
    
    try:
        orchestrator = AgentOrchestrator()
        result = await orchestrator._run_market_research(idea.idea)
        
        # Save results
        report_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        report_path = Path("reports") / f"{report_id}.json"
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        return MarketResearchResponse(
            status="completed",
            report_id=report_id,
            data=result,
            report_path=str(report_path)
        )
        
    except Exception as e:
        logger.error(f"Research failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pipeline", response_model=PipelineResponse, tags=["Pipeline"])
async def run_pipeline(
    idea: BusinessIdea,
    background_tasks: BackgroundTasks,
    phases: Optional[List[str]] = Query(None, description="Phases to execute")
):
    """
    Run complete or partial pipeline
    """
    logger.info(f"Pipeline requested for: {idea.idea}")
    
    try:
        orchestrator = AgentOrchestrator()
        result = await orchestrator.execute_pipeline(idea.idea)
        
        return PipelineResponse(
            status="completed",
            pipeline_id=result['pipeline_id'],
            summary=result.get('summary', {}),
            next_steps=result.get('next_steps', [])
        )
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pipeline/async", response_model=PipelineResponse, tags=["Pipeline"])
async def run_pipeline_async(
    idea: BusinessIdea,
    background_tasks: BackgroundTasks
):
    """
    Start pipeline asynchronously (returns immediately)
    """
    logger.info(f"Async pipeline requested for: {idea.idea}")
    
    pipeline_id = f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Add background task
    from orchestrator.task_queue import run_full_pipeline
    task = run_full_pipeline.delay(idea.idea)
    
    return PipelineResponse(
        status="started",
        pipeline_id=pipeline_id,
        summary={"task_id": task.id, "message": "Pipeline started in background"},
        next_steps=["Check status with /api/v1/pipeline/{pipeline_id}/status"]
    )


@router.get("/pipeline/{pipeline_id}/status", tags=["Pipeline"])
async def get_pipeline_status(pipeline_id: str):
    """
    Get pipeline execution status
    """
    report_path = Path("reports") / f"{pipeline_id}.json"
    
    if report_path.exists():
        with open(report_path) as f:
            data = json.load(f)
        return {"status": "completed", "pipeline_id": pipeline_id, "data": data}
    else:
        return {"status": "running", "pipeline_id": pipeline_id, "message": "Pipeline still running"}


@router.get("/pipeline/{pipeline_id}/report", tags=["Pipeline"])
async def get_pipeline_report(pipeline_id: str):
    """
    Download pipeline report
    """
    report_path = Path("reports") / f"{pipeline_id}.json"
    
    if report_path.exists():
        return FileResponse(
            report_path,
            media_type="application/json",
            filename=f"{pipeline_id}.json"
        )
    else:
        raise HTTPException(status_code=404, detail="Report not found")


@router.get("/reports", tags=["Reports"])
async def list_reports(limit: int = Query(10, ge=1, le=100)):
    """
    List all available reports
    """
    reports_dir = Path("reports")
    if not reports_dir.exists():
        return {"reports": []}
    
    reports = sorted(reports_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    return {
        "reports": [
            {
                "name": r.name,
                "size_bytes": r.stat().st_size,
                "created": datetime.fromtimestamp(r.stat().st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(r.stat().st_mtime).isoformat()
            }
            for r in reports[:limit]
        ]
    }


@router.get("/products", tags=["Products"])
async def list_products():
    """
    List generated products
    """
    products_dir = Path("generated_projects")
    if not products_dir.exists():
        return {"products": []}
    
    products = [d for d in products_dir.iterdir() if d.is_dir()]
    
    return {
        "products": [
            {
                "name": p.name,
                "path": str(p),
                "created": datetime.fromtimestamp(p.stat().st_ctime).isoformat()
            }
            for p in products
        ]
    }


@router.get("/products/{product_name}/download", tags=["Products"])
async def download_product(product_name: str):
    """
    Download generated product as zip
    """
    import shutil
    
    product_path = Path("generated_projects") / product_name
    
    if not product_path.exists():
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Create zip
    zip_path = Path("temp") / f"{product_name}.zip"
    zip_path.parent.mkdir(exist_ok=True)
    
    shutil.make_archive(str(zip_path.with_suffix('')), 'zip', product_path)
    
    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=f"{product_name}.zip"
    )