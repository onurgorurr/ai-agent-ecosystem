"""
Pydantic Schemas - Request/Response models
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class BusinessIdea(BaseModel):
    """Business idea input"""
    idea: str = Field(..., description="Business idea to analyze", min_length=3, max_length=500)
    industry: Optional[str] = Field(None, description="Industry classification")
    budget: Optional[float] = Field(None, description="Budget in USD", ge=0)
    timeline_months: Optional[int] = Field(None, description="Timeline in months", ge=1, le=60)
    
    class Config:
        json_schema_extra = {
            "example": {
                "idea": "AI-powered sustainable packaging marketplace",
                "industry": "Sustainability & E-commerce",
                "budget": 500000,
                "timeline_months": 12
            }
        }


class PipelineResponse(BaseModel):
    """Pipeline execution response"""
    status: str = Field(..., description="Pipeline status")
    pipeline_id: str = Field(..., description="Unique pipeline ID")
    summary: Optional[Dict[str, Any]] = Field(None, description="Pipeline summary")
    next_steps: Optional[List[str]] = Field(None, description="Recommended next steps")


class MarketResearchResponse(BaseModel):
    """Market research response"""
    status: str
    report_id: str
    data: Dict[str, Any]
    report_path: str


class OpportunityResponse(BaseModel):
    """Opportunity analysis response"""
    opportunities: List[Dict[str, Any]]
    recommended: Dict[str, Any]
    total_opportunities: int


class StrategyResponse(BaseModel):
    """Strategy response"""
    business_model: Dict[str, Any]
    gtm_strategy: Dict[str, Any]
    financial_projections: Dict[str, Any]


class ProductResponse(BaseModel):
    """Product development response"""
    prd: Dict[str, Any]
    codebase_path: str
    qa_plan: Dict[str, Any]
    deployment_ready: bool


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    agents_available: int
    api_key_configured: bool
    timestamp: str


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())