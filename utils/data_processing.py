"""
Data Processing Utilities
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from loguru import logger
import json
from pathlib import Path


class DataProcessor:
    """Process and transform data from various sources"""
    
    @staticmethod
    def flatten_dict(d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """Flatten nested dictionary"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(DataProcessor.flatten_dict(v, new_key, sep).items())
            elif isinstance(v, list):
                items.append((new_key, json.dumps(v)))
            else:
                items.append((new_key, v))
        return dict(items)
    
    @staticmethod
    def dict_to_dataframe(data: List[Dict]) -> pd.DataFrame:
        """Convert list of dictionaries to DataFrame"""
        if not data:
            return pd.DataFrame()
        
        # Flatten nested dictionaries
        flattened = [DataProcessor.flatten_dict(d) for d in data]
        return pd.DataFrame(flattened)
    
    @staticmethod
    def extract_key_metrics(data: Dict) -> Dict:
        """Extract key metrics from complex data"""
        metrics = {}
        
        # Market size
        if 'market_overview' in data:
            overview = data['market_overview']
            metrics['market_size_tam'] = overview.get('tam_billions')
            metrics['market_growth_cagr'] = overview.get('current_cagr_percent')
            metrics['market_maturity'] = overview.get('market_maturity')
        
        # Trends
        if 'trends' in data:
            metrics['num_trends'] = len(data['trends'])
            if data['trends']:
                metrics['top_trend'] = data['trends'][0].get('trend_name')
        
        return metrics
    
    @staticmethod
    def merge_market_data(*datasets: Dict) -> Dict:
        """Merge multiple market research datasets"""
        merged = {
            'market_overview': {},
            'trends': [],
            'competitors': [],
            'opportunities': [],
            'risks': []
        }
        
        for dataset in datasets:
            if 'market_overview' in dataset:
                merged['market_overview'].update(dataset['market_overview'])
            if 'trends' in dataset:
                merged['trends'].extend(dataset['trends'])
            if 'competitors' in dataset:
                merged['competitors'].extend(dataset.get('direct_competitors', []))
            if 'opportunities' in dataset:
                merged['opportunities'].extend(dataset.get('top_opportunities', []))
            if 'risk_factors' in dataset:
                merged['risks'].extend(dataset.get('risk_factors', []))
        
        return merged
    
    @staticmethod
    def calculate_opportunity_score(opportunity: Dict) -> float:
        """Calculate opportunity attractiveness score"""
        weights = {
            'market_size_billions': 0.25,
            'growth_rate_percent': 0.20,
            'competition_level': 0.15,
            'entry_barriers': 0.10,
            'revenue_potential': 0.15,
            'profit_margin_potential': 0.10,
            'feasibility_score': 0.05
        }
        
        score = 0
        for key, weight in weights.items():
            value = opportunity.get(key, 0)
            if isinstance(value, str):
                # Convert text to numeric
                value = {'low': 3, 'medium': 2, 'high': 1}.get(value, 1)
            score += float(value) * weight
        
        return round(score * 100, 2)
    
    @staticmethod
    def generate_summary_statistics(data: pd.DataFrame) -> Dict:
        """Generate summary statistics for DataFrame"""
        if data.empty:
            return {}
        
        stats = {
            'row_count': len(data),
            'column_count': len(data.columns),
            'numeric_columns': {},
            'categorical_columns': {}
        }
        
        for col in data.columns:
            if pd.api.types.is_numeric_dtype(data[col]):
                stats['numeric_columns'][col] = {
                    'mean': data[col].mean(),
                    'median': data[col].median(),
                    'std': data[col].std(),
                    'min': data[col].min(),
                    'max': data[col].max()
                }
            else:
                stats['categorical_columns'][col] = {
                    'unique_values': data[col].nunique(),
                    'top_values': data[col].value_counts().head(5).to_dict()
                }
        
        return stats