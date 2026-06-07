"""
Report Generator Utilities
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import jinja2
from loguru import logger


class ReportGenerator:
    """Generate formatted reports from agent outputs"""
    
    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(exist_ok=True)
        
        # Initialize Jinja2 environment
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.template_dir)),
            autoescape=True
        )
    
    def generate_json_report(self, data: Dict, output_path: Path) -> Path:
        """
        Generate JSON report
        
        Args:
            data: Report data
            output_path: Output file path
            
        Returns:
            Path to generated report
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        logger.info(f"JSON report saved: {output_path}")
        return output_path
    
    def generate_html_report(self, data: Dict, template_name: str, output_path: Path) -> Path:
        """
        Generate HTML report using template
        
        Args:
            data: Report data
            template_name: Name of Jinja2 template
            output_path: Output file path
            
        Returns:
            Path to generated report
        """
        template = self.env.get_template(template_name)
        html_content = template.render(**data, generated_at=datetime.now())
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        logger.info(f"HTML report saved: {output_path}")
        return output_path
    
    def generate_executive_summary(self, pipeline_results: Dict) -> str:
        """
        Generate executive summary from pipeline results
        
        Args:
            pipeline_results: Complete pipeline results
            
        Returns:
            Executive summary text
        """
        summary_parts = []
        
        summary_parts.append("=" * 60)
        summary_parts.append("EXECUTIVE SUMMARY")
        summary_parts.append("=" * 60)
        summary_parts.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary_parts.append(f"Pipeline ID: {pipeline_results.get('pipeline_id', 'N/A')}")
        summary_parts.append("")
        
        # Business Idea
        summary_parts.append(f"Business Idea: {pipeline_results.get('business_idea', 'N/A')}")
        summary_parts.append("")
        
        # Market Research Summary
        if 'phases' in pipeline_results and 'market_research' in pipeline_results['phases']:
            mr = pipeline_results['phases']['market_research']
            summary_parts.append("MARKET RESEARCH")
            summary_parts.append("-" * 40)
            
            if 'industry_analysis' in mr:
                analysis = mr['industry_analysis']
                if isinstance(analysis, dict):
                    if 'market_overview' in analysis:
                        overview = analysis['market_overview']
                        summary_parts.append(f"Market Size: ${overview.get('tam_billions', 'N/A')}B")
                        summary_parts.append(f"Growth Rate: {overview.get('current_cagr_percent', 'N/A')}%")
                        summary_parts.append(f"Market Maturity: {overview.get('market_maturity', 'N/A')}")
            
            summary_parts.append("")
        
        # Opportunities
        if 'phases' in pipeline_results and 'opportunities' in pipeline_results['phases']:
            opps = pipeline_results['phases']['opportunities']
            summary_parts.append("TOP OPPORTUNITIES")
            summary_parts.append("-" * 40)
            
            if isinstance(opps, dict) and 'top_opportunities' in opps:
                for i, opp in enumerate(opps['top_opportunities'][:3], 1):
                    summary_parts.append(f"{i}. {opp.get('opportunity_name', 'N/A')}")
                    summary_parts.append(f"   Market Size: ${opp.get('market_size_billions', 'N/A')}B")
            
            summary_parts.append("")
        
        # Strategy
        if 'phases' in pipeline_results and 'strategy' in pipeline_results['phases']:
            strategy = pipeline_results['phases']['strategy']
            summary_parts.append("RECOMMENDED STRATEGY")
            summary_parts.append("-" * 40)
            
            if 'business_model' in strategy and isinstance(strategy['business_model'], dict):
                bm = strategy['business_model']
                if 'business_model' in bm:
                    summary_parts.append(f"Model: {bm['business_model'].get('type', 'N/A')}")
            
            summary_parts.append("")
        
        # Product Status
        if 'phases' in pipeline_results and 'product' in pipeline_results['phases']:
            product = pipeline_results['phases']['product']
            summary_parts.append("PRODUCT STATUS")
            summary_parts.append("-" * 40)
            summary_parts.append(f"Status: {product.get('status', 'N/A')}")
            summary_parts.append("")
        
        # Next Steps
        summary_parts.append("NEXT STEPS")
        summary_parts.append("-" * 40)
        for step in pipeline_results.get('next_steps', []):
            summary_parts.append(f"• {step}")
        
        summary_parts.append("")
        summary_parts.append("=" * 60)
        
        return "\n".join(summary_parts)
    
    def generate_comparative_report(self, reports: List[Dict]) -> Dict:
        """
        Generate comparative analysis from multiple reports
        
        Args:
            reports: List of report dictionaries
            
        Returns:
            Comparative analysis dictionary
        """
        comparison = {
            'report_count': len(reports),
            'generated_at': datetime.now().isoformat(),
            'market_sizes': [],
            'growth_rates': [],
            'top_opportunities': [],
            'common_trends': []
        }
        
        for report in reports:
            if 'phases' in report:
                mr = report['phases'].get('market_research', {})
                if 'industry_analysis' in mr:
                    analysis = mr['industry_analysis']
                    if isinstance(analysis, dict):
                        overview = analysis.get('market_overview', {})
                        comparison['market_sizes'].append({
                            'report': report.get('pipeline_id'),
                            'tam': overview.get('tam_billions'),
                            'cagr': overview.get('current_cagr_percent')
                        })
        
        return comparison
    
    def save_report(self, data: Dict, report_type: str = "json") -> Path:
        """
        Save report to default location
        
        Args:
            data: Report data
            report_type: Type of report (json/html)
            
        Returns:
            Path to saved report
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_id = data.get('pipeline_id', f"report_{timestamp}")
        
        if report_type == "html":
            output_path = Path("reports") / f"{report_id}.html"
            return self.generate_html_report(data, "report_template.html", output_path)
        else:
            output_path = Path("reports") / f"{report_id}.json"
            return self.generate_json_report(data, output_path)