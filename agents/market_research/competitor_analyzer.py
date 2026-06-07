from agents.base_agent import BaseAgent
from typing import Dict, List
from loguru import logger

class CompetitorAnalysisAgent(BaseAgent):
    """Agent for competitive intelligence and landscape analysis"""
    
    def __init__(self):
        super().__init__("Competitor Analysis Agent")
        logger.info("Competitor Analysis Agent ready")
    
    async def analyze_competitors(self, market: str) -> Dict:
        """Deep competitive analysis"""
        
        logger.info(f"Analyzing competitors in: {market}")
        
        prompt = f"""
        Perform a comprehensive competitive analysis for the {market} market.
        
        Analyze:
        1. Direct competitors (top 10)
        2. Indirect competitors
        3. Potential entrants
        4. Substitute products/services
        
        For each competitor, provide:
        - Company overview
        - Market share estimate
        - Revenue estimates
        - Funding history
        - Key strengths
        - Weaknesses
        - Pricing strategy
        - Target customer segments
        - Technology stack
        - Recent strategic moves
        """
        
        schema = {
            "competitive_landscape": {
                "market_concentration": "fragmented/moderate/concentrated",
                "hhi_index": "number",
                "top3_market_share_percent": "number",
                "competition_intensity": "low/medium/high"
            },
            "direct_competitors": [
                {
                    "name": "string",
                    "founded_year": "number",
                    "headquarters": "string",
                    "employees": "number",
                    "revenue_estimate_millions": "number",
                    "market_share_percent": "number",
                    "total_funding_millions": "number",
                    "last_funding_round": "string",
                    "strengths": ["list"],
                    "weaknesses": ["list"],
                    "pricing_model": "freemium/subscription/usage_based/enterprise",
                    "target_segment": "enterprise/smb/consumer",
                    "technology_stack": ["list"],
                    "competitive_moat": "string"
                }
            ],
            "indirect_competitors": [
                {
                    "name": "string",
                    "threat_level": "high/medium/low",
                    "description": "string"
                }
            ],
            "market_whitespace": [
                {
                    "opportunity": "string",
                    "unserved_segment": "string",
                    "potential_revenue_millions": "number",
                    "entry_difficulty": "low/medium/high"
                }
            ],
            "competitive_advantages": {
                "sustainable_differentiators": ["list"],
                "temporary_advantages": ["list"],
                "recommended_positioning": "string"
            }
        }
        
        return await self.analyze_with_structure(prompt, schema)
    
    async def swot_analysis(self, company: str = None) -> Dict:
        """SWOT analysis for a specific company or market"""
        
        target = company if company else "the market leader"
        
        prompt = f"""
        Perform a detailed SWOT analysis for {target} in the context of
        current market dynamics and future trends.
        """
        
        schema = {
            "strengths": [
                {
                    "factor": "string",
                    "importance": "critical/important/notable",
                    "sustainability": "sustainable/temporary"
                }
            ],
            "weaknesses": [
                {
                    "factor": "string",
                    "severity": "critical/moderate/minor",
                    "fixability": "easy/moderate/difficult"
                }
            ],
            "opportunities": [
                {
                    "opportunity": "string",
                    "potential_impact": "high/medium/low",
                    "time_window": "immediate/short_term/long_term"
                }
            ],
            "threats": [
                {
                    "threat": "string",
                    "probability": "percentage",
                    "impact_severity": "high/medium/low",
                    "preparedness": "prepared/vulnerable/unprepared"
                }
            ]
        }
        
        return await self.analyze_with_structure(prompt, schema)