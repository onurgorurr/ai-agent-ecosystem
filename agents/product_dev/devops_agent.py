"""
DevOps Agent - Designs and manages infrastructure and deployment
"""
from agents.base_agent import BaseAgent
from typing import Dict, List
from loguru import logger
import json


class DevOpsAgent(BaseAgent):
    """AI DevOps Engineer for infrastructure and deployment"""
    
    def __init__(self):
        super().__init__("DevOps Agent")
        logger.info("DevOps Agent initialized")
    
    async def setup_infrastructure(self, prd: Dict) -> Dict:
        """
        Design infrastructure based on product requirements
        """
        logger.info("Setting up infrastructure")
        
        prompt = f"""
        Design the infrastructure for this product:
        
        {json.dumps(prd, indent=2)}
        
        Include:
        1. Cloud architecture
        2. Container orchestration
        3. CI/CD pipeline
        4. Monitoring and observability
        5. Security architecture
        6. Scaling strategy
        7. Disaster recovery
        8. Cost optimization
        """
        
        schema = {
            "infrastructure_design": {
                "cloud_provider": "aws/gcp/azure/multi-cloud",
                "architecture_pattern": "microservices/monolithic/serverless/hybrid",
                "regions": ["list"],
                "high_availability": "boolean",
                "disaster_recovery": {
                    "rto_minutes": "number",
                    "rpo_minutes": "number",
                    "strategy": "active-passive/active-active/pilot-light"
                }
            },
            "kubernetes_setup": {
                "cluster_configuration": {
                    "node_pools": [
                        {
                            "name": "string",
                            "instance_type": "string",
                            "min_nodes": "number",
                            "max_nodes": "number",
                            "purpose": "string"
                        }
                    ],
                    "networking": "string",
                    "service_mesh": "string"
                },
                "deployments": [
                    {
                        "service": "string",
                        "replicas": "number",
                        "resource_limits": {
                            "cpu": "string",
                            "memory": "string"
                        }
                    }
                ]
            },
            "ci_cd_pipeline": {
                "tool": "github_actions/gitlab_ci/jenkins/argo_cd",
                "stages": [
                    {
                        "name": "string",
                        "actions": ["list"],
                        "approval_required": "boolean"
                    }
                ],
                "deployment_strategy": "blue_green/canary/rolling",
                "rollback_strategy": "string"
            },
            "monitoring_stack": {
                "metrics": {
                    "tool": "prometheus/datadog/new_relic",
                    "key_metrics": ["list"]
                },
                "logging": {
                    "tool": "elk/loki/cloudwatch",
                    "retention_days": "number"
                },
                "tracing": {
                    "tool": "jaeger/zipkin/x-ray",
                    "sampling_rate": "number"
                },
                "alerting": {
                    "tool": "pagerduty/opsgenie/slack",
                    "alert_rules": [
                        {
                            "condition": "string",
                            "severity": "critical/warning/info",
                            "notification_channel": "string"
                        }
                    ]
                }
            },
            "security": {
                "network_security": ["list"],
                "secrets_management": "vault/secrets_manager/sops",
                "compliance": ["list"],
                "vulnerability_scanning": "boolean"
            },
            "scaling_strategy": {
                "horizontal_scaling": {
                    "enabled": "boolean",
                    "triggers": ["list"]
                },
                "vertical_scaling": {
                    "enabled": "boolean",
                    "limits": "string"
                },
                "auto_scaling_rules": [
                    {
                        "metric": "string",
                        "threshold": "string",
                        "action": "string"
                    }
                ]
            },
            "cost_optimization": {
                "estimated_monthly_cost_usd": "number",
                "savings_opportunities": ["list"],
                "reserved_instances_recommendation": "string"
            }
        }
        
        return await self.analyze_with_structure(prompt, schema)
    
    async def generate_terraform(self, infrastructure: Dict) -> str:
        """Generate Infrastructure as Code"""
        
        prompt = f"""
        Generate Terraform code for this infrastructure:
        {json.dumps(infrastructure, indent=2)}
        
        Provide production-ready Terraform configurations.
        Include modules, variables, and outputs.
        """
        
        # This returns raw code, not JSON
        code = await self.think(f"""
        Generate Terraform code for:
        {json.dumps(infrastructure, indent=2)}
        
        Include:
        - Provider configuration
        - VPC and networking
        - Kubernetes cluster
        - Database instances
        - Monitoring setup
        - IAM roles and policies
        
        Provide complete, working Terraform code.
        """)
        
        return code
    
    async def generate_github_actions(self, pipeline_config: Dict) -> str:
        """Generate CI/CD pipeline configuration"""
        
        prompt = f"""
        Generate GitHub Actions workflow for this pipeline:
        {json.dumps(pipeline_config, indent=2)}
        
        Include:
        - Build steps
        - Test steps
        - Security scanning
        - Docker build and push
        - Deployment to Kubernetes
        - Environment promotion
        """
        
        code = await self.think(f"""
        Generate complete GitHub Actions workflow YAML for:
        {json.dumps(pipeline_config, indent=2)}
        Provide production-ready workflow configuration.
        """)
        
        return code
    
    async def audit_infrastructure(self, infrastructure: Dict) -> Dict:
        """Audit infrastructure for best practices and security"""
        
        prompt = f"""
        Audit this infrastructure for security, reliability, and cost:
        {json.dumps(infrastructure, indent=2)}
        
        Check against:
        - Well-Architected Framework
        - Security best practices
        - Cost optimization
        - Reliability
        """
        
        schema = {
            "audit_results": {
                "overall_score": "number 1-10",
                "security_score": "number 1-10",
                "reliability_score": "number 1-10",
                "cost_efficiency_score": "number 1-10"
            },
            "findings": [
                {
                    "severity": "critical/high/medium/low",
                    "category": "security/reliability/cost/performance",
                    "finding": "string",
                    "recommendation": "string",
                    "effort_to_fix": "low/medium/high"
                }
            ],
            "compliant_standards": ["list"],
            "improvement_plan": [
                {
                    "action": "string",
                    "priority": "high/medium/low",
                    "timeline": "string"
                }
            ]
        }
        
        return await self.analyze_with_structure(prompt, schema)