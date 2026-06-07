import asyncio
from typing import Dict, List
from datetime import datetime
from pathlib import Path
import json
from loguru import logger

from agents import (
    TrendAnalysisAgent,
    CompetitorAnalysisAgent,
    ConsumerInsightAgent,
    TechnologyScoutAgent,
    OpportunityScannerAgent,
    BusinessModelAgent,
    GTMStrategyAgent,
    ProductManagerAgent,
    CodeGenerationAgent,
    QAEngineerAgent,
    DevOpsAgent
)

class AgentOrchestrator:
    """Main orchestrator for all AI agents"""
    
    def __init__(self):
        logger.info("Initializing Agent Orchestrator")
        
        # Store agent classes (lazy-load on demand)
        self._agent_classes = {
            'trend_analyzer': TrendAnalysisAgent,
            'competitor_analyzer': CompetitorAnalysisAgent,
            'consumer_insight': ConsumerInsightAgent,
            'technology_scout': TechnologyScoutAgent,
            'opportunity_scanner': OpportunityScannerAgent,
            'business_model': BusinessModelAgent,
            'gtm_strategy': GTMStrategyAgent,
            'product_manager': ProductManagerAgent,
            'code_generator': CodeGenerationAgent,
            'qa_engineer': QAEngineerAgent,
            'devops_agent': DevOpsAgent
        }
        self.agents = {}  # Will be populated on-demand
        
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
        
        logger.info(f"Orchestrator ready with {len(self._agent_classes)} agents (lazy-loaded)")
    
    def _get_agent(self, agent_key: str):
        """Lazy-load agent on first use"""
        if agent_key not in self.agents:
            logger.debug(f"Initializing agent: {agent_key}")
            self.agents[agent_key] = self._agent_classes[agent_key]()
        return self.agents[agent_key]
    
    async def execute_pipeline(self, business_idea: str) -> Dict:
        """Execute complete pipeline"""
        
        pipeline_id = f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        logger.info(f"Starting pipeline {pipeline_id}: {business_idea}")
        
        results = {
            'pipeline_id': pipeline_id,
            'business_idea': business_idea,
            'timestamp': datetime.now().isoformat(),
            'phases': {}
        }
        
        # Phase 1: Market Research
        logger.info("Phase 1: Market Research")
        market_data = await self._run_market_research(business_idea)
        results['phases']['market_research'] = market_data
        
        # Phase 2: Opportunity Identification
        logger.info("Phase 2: Opportunity Identification")
        opportunities = await self._identify_opportunities(market_data)
        results['phases']['opportunities'] = opportunities
        
        # Phase 3: Strategy Development
        logger.info("Phase 3: Strategy Development")
        strategy = await self._develop_strategy(opportunities, market_data)
        results['phases']['strategy'] = strategy
        
        # Phase 4: Product Development
        logger.info("Phase 4: Product Development")
        product = await self._develop_product(strategy)
        results['phases']['product'] = product
        
        # Generate report
        report = self._generate_report(results)
        
        # Save results
        self._save_results(pipeline_id, results)
        
        logger.info(f"Pipeline {pipeline_id} complete")
        return report
    
    async def _run_market_research(self, idea: str) -> Dict:
        """Execute market research phase"""
        
        # Run research agents in parallel
        tasks = [
            self._get_agent('trend_analyzer').analyze_industry(idea),
            self._get_agent('competitor_analyzer').analyze_competitors(idea),
            self._get_agent('consumer_insight').analyze_consumers(idea),
            self._get_agent('technology_scout').scout_technology(idea)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Better error handling
        return {
            'industry_analysis': results[0] if not isinstance(results[0], Exception) else {"error": str(results[0]), "status": "failed"},
            'competitive_landscape': results[1] if not isinstance(results[1], Exception) else {"error": str(results[1]), "status": "failed"},
            'consumer_insights': results[2] if not isinstance(results[2], Exception) else {"error": str(results[2]), "status": "failed"},
            'technology_assessment': results[3] if not isinstance(results[3], Exception) else {"error": str(results[3]), "status": "failed"}
        }
    
    async def _identify_opportunities(self, market_data: Dict) -> Dict:
        """Identify business opportunities"""
        
        return await self._get_agent('opportunity_scanner').scan_opportunities(market_data)
    
    async def _develop_strategy(self, opportunities: Dict, market_data: Dict) -> Dict:
        """Develop business strategy"""
        
        # Run strategy agents in parallel
        tasks = [
            self._get_agent('business_model').design_business_model(opportunities),
            self._get_agent('gtm_strategy').create_gtm_strategy(opportunities, market_data)
        ]
        
        results = await asyncio.gather(*tasks)
        
        return {
            'business_model': results[0],
            'gtm_strategy': results[1]
        }
    
    async def _develop_product(self, strategy: Dict) -> Dict:
        """Execute product development phase"""
        
        # Create PRD
        prd = await self._get_agent('product_manager').create_prd(strategy)
        
        # Generate code
        codebase = await self._get_agent('code_generator').generate_fullstack_app(prd)
        
        # QA analysis
        qa_plan = await self._get_agent('qa_engineer').create_test_plan(prd)
        
        # DevOps setup
        devops = await self._get_agent('devops_agent').setup_infrastructure(prd)
        
        return {
            'prd': prd,
            'codebase': codebase,
            'qa_plan': qa_plan,
            'devops_setup': devops,
            'status': 'ready_for_deployment'
        }
    
    def _generate_report(self, results: Dict) -> Dict:
        """Generate comprehensive report"""
        
        return {
            'pipeline_id': results['pipeline_id'],
            'business_idea': results['business_idea'],
            'execution_time': results['timestamp'],
            'summary': self._create_summary(results),
            'detailed_results': results['phases'],
            'next_steps': self._generate_next_steps(results)
        }
    
    def _create_summary(self, results: Dict) -> Dict:
        """Create executive summary"""
        return {
            'market_size': 'Analyzed',
            'top_opportunities': 'Identified',
            'strategy': 'Developed',
            'product_status': 'MVP Generated',
            'codebase': 'Ready for review'
        }
    
    def _generate_next_steps(self, results: Dict) -> List[str]:
        """Generate next steps"""
        return [
            "1. Review market research findings",
            "2. Validate top business opportunities",
            "3. Approve product requirements document",
            "4. Review generated codebase",
            "5. Set up development environment",
            "6. Begin MVP development",
            "7. Plan pilot program"
        ]
    
    def _save_results(self, pipeline_id: str, results: Dict):
        """Save pipeline results to file"""
        
        report_path = self.reports_dir / f"{pipeline_id}.json"
        
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Results saved to {report_path}")