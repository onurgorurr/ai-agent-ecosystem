"""
Consumer Insight Agent - Analyzes consumer behavior, preferences, and market trends
"""
from agents.base_agent import BaseAgent
from typing import Dict, List, Optional
from loguru import logger
import json


class ConsumerInsightAgent(BaseAgent):
    """Deep consumer behavior analysis and insight generation"""
    
    def __init__(self):
        super().__init__("Consumer Insight Agent")
        logger.info("Consumer Insight Agent initialized")
    
    async def analyze_consumers(self, market: str) -> Dict:
        """
        Comprehensive consumer analysis for a given market
        """
        logger.info(f"Analyzing consumer behavior in: {market}")
        
        prompt = f"""
        Perform a detailed consumer analysis for the {market} market.
        
        Analyze:
        1. Target Demographics
           - Age groups
           - Income levels
           - Education
           - Geographic distribution
        
        2. Psychographics
           - Values and beliefs
           - Lifestyle preferences
           - Buying motivations
           - Brand perceptions
        
        3. Behavioral Patterns
           - Purchase frequency
           - Channel preferences
           - Decision-making process
           - Brand loyalty factors
        
        4. Pain Points & Unmet Needs
           - Current frustrations
           - Desired solutions
           - Willingness to switch
           - Price sensitivity
        
        5. Technology Adoption
           - Digital literacy
           - Preferred platforms
           - Tech pain points
           - Innovation receptiveness
        """
        
        schema = {
            "target_segments": [
                {
                    "segment_name": "string",
                    "size_millions": "number",
                    "age_range": "string",
                    "income_level": "string",
                    "education": "string",
                    "geography": "string",
                    "buying_behavior": "string"
                }
            ],
            "pain_points": [
                {
                    "pain_point": "string",
                    "severity": "critical/high/medium/low",
                    "frequency": "daily/weekly/monthly",
                    "current_solutions": ["list"],
                    "willingness_to_pay_solution": "number USD"
                }
            ],
            "buying_behaviors": {
                "purchase_triggers": ["list"],
                "decision_factors": ["list"],
                "information_sources": ["list"],
                "purchase_channels": ["list"],
                "average_consideration_time_days": "number"
            },
            "preferences": {
                "price_sensitivity": "low/medium/high",
                "brand_loyalty": "low/medium/high",
                "feature_priorities": ["list"],
                "customer_service_expectations": ["list"]
            },
            "technology_adoption": {
                "digital_literacy_level": "low/medium/high",
                "preferred_platforms": ["list"],
                "tech_pain_points": ["list"],
                "innovation_receptiveness": "early_adopter/mainstream/laggard"
            },
            "personas": [
                {
                    "name": "string",
                    "description": "string",
                    "goals": ["list"],
                    "frustrations": ["list"],
                    "quote": "string",
                    "market_size_percentage": "number"
                }
            ]
        }
        
        return await self.analyze_with_structure(prompt, schema)
    
    async def create_detailed_personas(self, market_data: Dict) -> List[Dict]:
        """Create detailed user personas based on market data"""
        
        prompt = f"""
        Create 5 detailed user personas based on this market data:
        {json.dumps(market_data, indent=2)}
        
        For each persona, create a vivid, realistic profile that includes:
        - Fictional name and photo description
        - Demographics
        - Job and career
        - Daily routine
        - Goals and motivations
        - Pain points and frustrations
        - Technology usage
        - Buying preferences
        - Quote that captures their essence
        """
        
        schema = {
            "personas": [
                {
                    "name": "string",
                    "age": "number",
                    "occupation": "string",
                    "location": "string",
                    "income_bracket": "string",
                    "education": "string",
                    "family_status": "string",
                    "goals": ["list"],
                    "frustrations": ["list"],
                    "daily_routine": "string",
                    "technology_usage": {
                        "devices": ["list"],
                        "apps": ["list"],
                        "daily_screen_time_hours": "number"
                    },
                    "buying_preferences": {
                        "research_method": "string",
                        "purchase_channel": "string",
                        "price_sensitivity": "low/medium/high",
                        "brand_importance": "low/medium/high"
                    },
                    "personality_traits": ["list"],
                    "quote": "string",
                    "image_description": "string"
                }
            ]
        }
        
        result = await self.analyze_with_structure(prompt, schema)
        return result.get("personas", [])
    
    async def analyze_sentiment(self, topic: str) -> Dict:
        """Analyze consumer sentiment around a topic"""
        
        prompt = f"""
        Analyze current consumer sentiment regarding {topic}.
        Include social media sentiment, review analysis, and trend direction.
        """
        
        schema = {
            "overall_sentiment": {
                "score": "number -1 to 1",
                "label": "very_negative/negative/neutral/positive/very_positive",
                "trend": "improving/stable/declining",
                "confidence": "percentage"
            },
            "sentiment_breakdown": {
                "positive_percentage": "number",
                "neutral_percentage": "number",
                "negative_percentage": "number"
            },
            "key_themes": [
                {
                    "theme": "string",
                    "sentiment": "positive/negative/neutral",
                    "frequency": "percentage",
                    "example_quote": "string"
                }
            ],
            "influencers": [
                {
                    "source": "string",
                    "influence_level": "high/medium/low",
                    "stance": "string"
                }
            ]
        }
        
        return await self.analyze_with_structure(prompt, schema)
    
    async def predict_behavior(self, segment_data: Dict) -> Dict:
        """Predict future consumer behavior patterns"""
        
        prompt = f"""
        Based on this consumer segment data, predict future behavior patterns
        for the next 12-24 months:
        {json.dumps(segment_data, indent=2)}
        
        Consider:
        - Economic trends
        - Technology adoption curves
        - Social changes
        - Competitive dynamics
        """
        
        schema = {
            "predictions": [
                {
                    "behavior": "string",
                    "likelihood": "percentage",
                    "timeframe_months": "number",
                    "impact_level": "high/medium/low",
                    "confidence": "percentage",
                    "driving_factors": ["list"]
                }
            ],
            "key_shifts": [
                {
                    "shift": "string",
                    "current_state": "string",
                    "predicted_state": "string",
                    "velocity": "slow/moderate/fast"
                }
            ]
        }
        
        return await self.analyze_with_structure(prompt, schema)