from agents.base_agent import BaseAgent
from typing import Dict, List
from loguru import logger
import json

class ProductManagerAgent(BaseAgent):
    """AI Product Manager for product strategy and requirements"""
    
    def __init__(self):
        super().__init__("Product Manager Agent")
        logger.info("Product Manager Agent ready")
    
    async def create_prd(self, opportunity: Dict) -> Dict:
        """Generate Product Requirements Document"""
        
        logger.info("Creating PRD from opportunity")
        
        prompt = f"""
        Create a comprehensive Product Requirements Document (PRD) based on
        this business opportunity:
        
        {json.dumps(opportunity, indent=2)}
        
        Include:
        1. Product Vision & Strategy
        2. Target User Personas (3-5 detailed personas)
        3. Core Features with MoSCoW prioritization
        4. User Stories with acceptance criteria
        5. Success Metrics (OKRs and KPIs)
        6. MVP Scope Definition
        7. Technical Requirements Overview
        8. Development Timeline Estimate
        9. Resource Requirements
        10. Risk Assessment
        """
        
        schema = {
            "product_vision": {
                "elevator_pitch": "string",
                "mission_statement": "string",
                "unique_value_proposition": "string",
                "target_market_summary": "string"
            },
            "user_personas": [
                {
                    "name": "string",
                    "role": "string",
                    "demographics": {
                        "age_range": "string",
                        "income_level": "string",
                        "education": "string"
                    },
                    "goals": ["list"],
                    "pain_points": ["list"],
                    "behaviors": ["list"],
                    "tech_savviness": "low/medium/high"
                }
            ],
            "features": [
                {
                    "feature_name": "string",
                    "category": "core/differentiator/table_stakes",
                    "priority": "must_have/should_have/could_have/wont_have",
                    "user_story": "As a [user], I want [feature] so that [benefit]",
                    "acceptance_criteria": ["list"],
                    "effort_estimate_story_points": "number",
                    "dependencies": ["list"],
                    "success_metric": "string"
                }
            ],
            "mvp_definition": {
                "mvp_features": ["list of must-have features"],
                "mvp_timeline_weeks": "number",
                "mvp_budget_estimate_usd": "number",
                "mvp_success_criteria": ["list"]
            },
            "success_metrics": {
                "north_star_metric": "string",
                "primary_kpis": [
                    {
                        "metric": "string",
                        "target": "string",
                        "measurement_frequency": "string"
                    }
                ],
                "secondary_metrics": ["list"]
            },
            "technical_requirements": {
                "platform": "web/mobile/desktop/api",
                "recommended_stack": {
                    "frontend": "string",
                    "backend": "string",
                    "database": "string",
                    "infrastructure": "string"
                },
                "integrations_required": ["list"],
                "performance_requirements": "string",
                "security_requirements": ["list"]
            },
            "development_roadmap": [
                {
                    "phase": "string",
                    "duration_weeks": "number",
                    "key_deliverables": ["list"],
                    "team_size": "number"
                }
            ],
            "risks": [
                {
                    "risk": "string",
                    "probability": "high/medium/low",
                    "impact": "high/medium/low",
                    "mitigation_strategy": "string"
                }
            ]
        }
        
        return await self.analyze_with_structure(prompt, schema)
    
    async def prioritize_features(self, features: List[Dict]) -> List[Dict]:
        """Prioritize features using RICE framework"""
        
        prompt = f"""
        Prioritize these features using the RICE framework (Reach, Impact, Confidence, Effort).
        Score each feature and sort by RICE score.
        
        Features:
        {json.dumps(features, indent=2)}
        """
        
        schema = {
            "prioritized_features": [
                {
                    "feature": "string",
                    "rice_score": "number",
                    "reach_score": "number 1-10",
                    "impact_score": "number 1-10",
                    "confidence_score": "percentage",
                    "effort_score": "number 1-10",
                    "priority_rank": "number"
                }
            ]
        }
        
        result = await self.analyze_with_structure(prompt, schema)
        return result.get("prioritized_features", [])