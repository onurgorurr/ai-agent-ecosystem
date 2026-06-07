"""
Go-To-Market Strategy Agent - Creates comprehensive GTM plans
"""
from agents.base_agent import BaseAgent
from typing import Dict, List
from loguru import logger
import json


class GTMStrategyAgent(BaseAgent):
    """Develops comprehensive go-to-market strategies"""
    
    def __init__(self):
        super().__init__("GTM Strategy Agent")
        logger.info("GTM Strategy Agent initialized")
    
    async def create_gtm_strategy(self, opportunities: Dict, market_data: Dict) -> Dict:
        """
        Create comprehensive go-to-market strategy
        """
        logger.info("Creating GTM strategy")
        
        prompt = f"""
        Create a detailed go-to-market strategy based on:
        
        Opportunities: {json.dumps(opportunities, indent=2)}
        Market Data: {json.dumps(market_data, indent=2)}
        
        Include:
        1. Target market selection and beachhead strategy
        2. Positioning and messaging
        3. Channel strategy
        4. Marketing mix
        5. Sales strategy
        6. Launch plan and timeline
        7. Budget allocation
        8. Success metrics
        """
        
        schema = {
            "gtm_strategy": {
                "target_market": {
                    "primary_segment": "string",
                    "beachhead_market": "string",
                    "expansion_path": ["list"],
                    "total_addressable_market_description": "string"
                },
                "positioning": {
                    "value_proposition": "string",
                    "key_messages": ["list"],
                    "brand_promise": "string",
                    "differentiation_angle": "string",
                    "elevator_pitch": "string"
                },
                "channel_strategy": {
                    "primary_channels": [
                        {
                            "channel": "string",
                            "type": "direct/indirect/online/offline",
                            "priority": "primary/secondary/tertiary",
                            "expected_contribution_percent": "number",
                            "setup_time_months": "number"
                        }
                    ],
                    "channel_mix_rationale": "string"
                },
                "marketing_strategy": {
                    "digital_marketing": {
                        "channels": ["list"],
                        "budget_allocation_percent": "number",
                        "key_tactics": ["list"]
                    },
                    "content_strategy": {
                        "content_types": ["list"],
                        "publishing_frequency": "string",
                        "key_topics": ["list"]
                    },
                    "pr_strategy": {
                        "key_media_targets": ["list"],
                        "story_angles": ["list"]
                    }
                },
                "sales_strategy": {
                    "sales_model": "self_service/inside_sales/field_sales/channel_partners",
                    "sales_cycle_length_days": "number",
                    "average_deal_size_usd": "number",
                    "sales_team_structure": "string"
                },
                "launch_plan": {
                    "pre_launch_activities": [
                        {
                            "activity": "string",
                            "timeline": "string",
                            "owner": "string"
                        }
                    ],
                    "launch_event": "string",
                    "post_launch_activities": [
                        {
                            "activity": "string",
                            "timeline": "string"
                        }
                    ],
                    "launch_date_target": "string"
                },
                "budget_allocation": {
                    "total_budget_usd": "number",
                    "marketing_percent": "number",
                    "sales_percent": "number",
                    "product_percent": "number",
                    "operations_percent": "number"
                },
                "success_metrics": {
                    "month1_targets": {
                        "users": "number",
                        "revenue_usd": "number",
                        "conversion_rate_percent": "number"
                    },
                    "month3_targets": {
                        "users": "number",
                        "revenue_usd": "number",
                        "market_share_percent": "number"
                    },
                    "month6_targets": {
                        "users": "number",
                        "revenue_usd": "number",
                        "profitability": "boolean"
                    }
                }
            },
            "timeline": {
                "phase1_discovery_months_1_2": {
                    "activities": ["list"],
                    "milestones": ["list"]
                },
                "phase2_development_months_3_4": {
                    "activities": ["list"],
                    "milestones": ["list"]
                },
                "phase3_launch_month_5": {
                    "activities": ["list"],
                    "milestones": ["list"]
                },
                "phase4_scale_months_6_12": {
                    "activities": ["list"],
                    "milestones": ["list"]
                }
            },
            "risk_mitigation": [
                {
                    "risk": "string",
                    "mitigation_strategy": "string",
                    "trigger_for_action": "string"
                }
            ]
        }
        
        return await self.analyze_with_structure(prompt, schema)
    
    async def create_marketing_plan(self, gtm_strategy: Dict, budget: float) -> Dict:
        """Create detailed marketing execution plan"""
        
        prompt = f"""
        Create a detailed marketing execution plan with a budget of ${budget}.
        Strategy: {json.dumps(gtm_strategy, indent=2)}
        
        Include specific campaigns, channels, content calendar, and KPIs.
        """
        
        schema = {
            "marketing_plan": {
                "budget_breakdown": [
                    {
                        "channel": "string",
                        "budget_usd": "number",
                        "expected_roi": "number",
                        "kpis": ["list"]
                    }
                ],
                "campaigns": [
                    {
                        "campaign_name": "string",
                        "objective": "string",
                        "target_audience": "string",
                        "channels": ["list"],
                        "budget_usd": "number",
                        "timeline": "string",
                        "success_metrics": ["list"]
                    }
                ],
                "content_calendar": [
                    {
                        "week": "number",
                        "content_type": "string",
                        "topic": "string",
                        "channel": "string",
                        "goal": "string"
                    }
                ],
                "kpi_dashboard": {
                    "leading_indicators": ["list"],
                    "lagging_indicators": ["list"],
                    "review_cadence": "string"
                }
            }
        }
        
        return await self.analyze_with_structure(prompt, schema)
    
    async def analyze_market_entry(self, market: str, mode: str) -> Dict:
        """Analyze specific market entry strategy"""
        
        prompt = f"""
        Analyze market entry strategy for {market} using {mode} entry mode.
        Consider organic growth, partnerships, acquisitions, and joint ventures.
        """
        
        schema = {
            "entry_analysis": {
                "recommended_mode": "organic/partnership/acquisition/joint_venture",
                "rationale": "string",
                "pros": ["list"],
                "cons": ["list"]
            },
            "implementation": {
                "timeline_months": "number",
                "key_steps": ["list"],
                "resources_required": {
                    "team": "number",
                    "budget_usd": "number",
                    "partners": ["list"]
                }
            },
            "success_factors": ["list"],
            "pitfalls_to_avoid": ["list"]
        }
        
        return await self.analyze_with_structure(prompt, schema)