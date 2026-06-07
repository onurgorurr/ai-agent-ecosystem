"""
Opportunity Scanner Agent - Identifies and ranks business opportunities
"""
from agents.base_agent import BaseAgent
from typing import Dict, List
from loguru import logger
import json


class OpportunityScannerAgent(BaseAgent):
    """Scans market data to identify and rank business opportunities"""
    
    def __init__(self):
        super().__init__("Opportunity Scanner Agent")
        logger.info("Opportunity Scanner Agent initialized")
    
    async def scan_opportunities(self, market_data: Dict) -> Dict:
        """
        Scan market data to identify viable business opportunities
        """
        logger.info("Scanning for business opportunities")
        
        prompt = f"""
        Analyze this market data and identify the most promising business opportunities:
        
        {json.dumps(market_data, indent=2)}
        
        For each opportunity, evaluate:
        1. Market size and growth potential
        2. Competition intensity
        3. Entry barriers
        4. Revenue potential
        5. Resource requirements
        6. Time to market
        7. Risk factors
        8. Strategic fit
        
        Rank opportunities by overall attractiveness score.
        """
        
        schema = {
            "top_opportunities": [
                {
                    "opportunity_name": "string",
                    "description": "string",
                    "market_size_billions": "number",
                    "growth_rate_percent": "number",
                    "competition_level": "low/medium/high",
                    "entry_barriers": "low/medium/high",
                    "revenue_potential_3yr_millions": "number",
                    "profit_margin_potential_percent": "number",
                    "time_to_market_months": "number",
                    "resource_requirements": {
                        "team_size": "number",
                        "initial_investment_usd": "number",
                        "key_skills_required": ["list"]
                    },
                    "risk_assessment": {
                        "overall_risk": "low/medium/high",
                        "key_risks": ["list"],
                        "risk_mitigation": ["list"]
                    },
                    "attractiveness_score": "number 1-100",
                    "strategic_fit_score": "number 1-100",
                    "feasibility_score": "number 1-100"
                }
            ],
            "recommended_opportunity": {
                "name": "string",
                "rationale": "string",
                "key_success_factors": ["list"],
                "go_no_go_criteria": ["list"]
            },
            "opportunity_matrix": {
                "quick_wins": ["list"],
                "major_projects": ["list"],
                "fill_ins": ["list"],
                "thankless_tasks": ["list"]
            },
            "market_timing": {
                "overall_timing": "too_early/optimal/too_late",
                "window_of_opportunity": "string",
                "urgency_level": "low/medium/high"
            }
        }
        
        return await self.analyze_with_structure(prompt, schema)
    
    async def validate_opportunity(self, opportunity: Dict) -> Dict:
        """
        Deep validation of a specific opportunity
        """
        prompt = f"""
        Validate this business opportunity thoroughly:
        {json.dumps(opportunity, indent=2)}
        
        Provide a rigorous assessment including:
        - Market demand validation
        - Competitive advantage sustainability
        - Unit economics analysis
        - Customer acquisition feasibility
        - Technical feasibility
        - Regulatory considerations
        """
        
        schema = {
            "validation_result": {
                "overall_viability": "viable/risky/not_viable",
                "confidence_score": "percentage",
                "validation_grade": "A/B/C/D/F"
            },
            "market_validation": {
                "demand_exists": "boolean",
                "demand_evidence": ["list"],
                "market_size_validated": "boolean",
                "customer_willingness_to_pay": "boolean"
            },
            "competitive_validation": {
                "sustainable_advantage": "boolean",
                "differentiation_score": "number 1-10",
                "moat_assessment": "strong/moderate/weak"
            },
            "financial_validation": {
                "unit_economics_positive": "boolean",
                "breakeven_timeline_months": "number",
                "funding_required_usd": "number",
                "roi_3yr_percent": "number"
            },
            "execution_validation": {
                "technical_feasibility": "high/medium/low",
                "team_capability_match": "high/medium/low",
                "time_to_market_realistic": "boolean"
            },
            "red_flags": ["list"],
            "green_flags": ["list"],
            "recommendation": "pursue/pivot/abandon",
            "next_steps": ["list"]
        }
        
        return await self.analyze_with_structure(prompt, schema)
    
    async def generate_opportunity_hypotheses(self, industry: str, trends: List[str]) -> List[Dict]:
        """Generate opportunity hypotheses based on industry trends"""
        
        prompt = f"""
        Based on these trends in the {industry} industry:
        {json.dumps(trends, indent=2)}
        
        Generate 10 innovative business opportunity hypotheses.
        Think creatively about unmet needs, emerging technologies, and market gaps.
        """
        
        schema = {
            "hypotheses": [
                {
                    "hypothesis": "string",
                    "problem_solved": "string",
                    "target_customer": "string",
                    "value_proposition": "string",
                    "why_now": "string",
                    "early_signals": ["list"],
                    "assumptions_to_test": ["list"],
                    "innovation_type": "incremental/disruptive/architectural/radical"
                }
            ]
        }
        
        result = await self.analyze_with_structure(prompt, schema)
        return result.get("hypotheses", [])
    
    async def generate_business_ideas(self, industry: str, market_data: Dict) -> List[Dict]:
        """Generate innovative business ideas for a specific industry"""
        
        logger.info(f"Generating business ideas for industry: {industry}")
        
        prompt = f"""
        You are an expert startup advisor and market strategist. Analyze the {industry} industry 
        using the provided market research data and generate innovative, actionable business ideas.
        
        Market Research Data:
        {json.dumps(market_data, indent=2)}
        
        Generate 10 concrete, implementable business ideas that:
        1. Address real market gaps and unmet customer needs
        2. Leverage emerging technologies and market trends
        3. Offer clear differentiation from existing solutions
        4. Have realistic paths to market entry
        5. Show strong unit economics potential
        
        For each idea, provide specific details about:
        - The core value proposition
        - Target customer segments
        - Revenue model
        - Competitive advantages
        - Market opportunity size
        - Key success factors
        - Initial go-to-market strategy
        - Why this is the right time for this idea
        """
        
        schema = {
            "business_ideas": [
                {
                    "name": "string",
                    "description": "string",
                    "problem_statement": "string",
                    "solution": "string",
                    "target_segments": ["list"],
                    "value_proposition": "string",
                    "key_differentiators": ["list"],
                    "revenue_model": "subscription/transaction/licensing/freemium/marketplace/other",
                    "estimated_market_size": "string",
                    "tam_billions": "number",
                    "initial_investment_usd": "number",
                    "time_to_market_months": "number",
                    "competition_level": "low/medium/high",
                    "required_technologies": ["list"],
                    "team_requirements": ["list"],
                    "key_partnerships": ["list"],
                    "key_success_factors": ["list"],
                    "main_risks": ["list"],
                    "first_customer_profile": "string",
                    "gtm_strategy": "string",
                    "year_1_goals": ["list"],
                    "innovation_score": "number 1-10",
                    "feasibility_score": "number 1-10",
                    "market_attractiveness_score": "number 1-10",
                    "overall_opportunity_score": "number 1-10"
                }
            ],
            "industry_insights": {
                "key_trends": ["list"],
                "market_gaps": ["list"],
                "emerging_opportunities": ["list"],
                "technology_enablers": ["list"],
                "customer_pain_points": ["list"],
                "timing_rationale": "string"
            },
            "top_recommendation": {
                "idea_name": "string",
                "why_pursue_this": "string",
                "next_validation_steps": ["list"]
            }
        }
        
        result = await self.analyze_with_structure(prompt, schema)
        return result.get("business_ideas", [])