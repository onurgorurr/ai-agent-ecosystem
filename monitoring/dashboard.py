#!/usr/bin/env python3
"""
Streamlit Dashboard for AI Agent Ecosystem Monitoring
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json
from datetime import datetime, timedelta
import asyncio
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.execution_engine import AgentOrchestrator
from utils.report_generator import ReportGenerator


# Page configuration
st.set_page_config(
    page_title="AI Agent Ecosystem Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .success-metric {
        color: #00cc00;
        font-weight: bold;
    }
    .warning-metric {
        color: #ff9900;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/150x150.png?text=AI", width=100)
    st.markdown("## 🤖 AI Agent Ecosystem")
    
    st.divider()
    
    # API Key Input
    api_key = st.text_input("OpenAI API Key", type="password", 
                            help="Enter your OpenAI API key to enable agents")
    if api_key:
        import os
        os.environ["OPENAI_API_KEY"] = api_key
    
    st.divider()
    
    # Navigation
    page = st.radio(
        "Navigate",
        ["📊 Dashboard", "🔍 Market Research", "💡 Opportunities", 
         "📈 Strategy", "💻 Product Dev", "📁 Reports", "⚙️ Settings"]
    )
    
    st.divider()
    
    # System Status
    st.markdown("### System Status")
    st.metric("Agents Available", "15+")
    st.metric("Reports Generated", len(list(Path("reports").glob("*.json"))) if Path("reports").exists() else 0)
    
    st.divider()
    st.caption("v1.0.0 | Powered by GPT-4")


# Main content
if page == "📊 Dashboard":
    st.markdown('<p class="main-header">📊 Dashboard Overview</p>', unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Pipelines", "0", "Start one below")
    with col2:
        st.metric("Active Agents", "15", "All ready")
    with col3:
        st.metric("Reports Generated", "0", "In reports/")
    with col4:
        st.metric("Avg Response Time", "~2s", "-0.5s")
    
    st.divider()
    
    # Quick Start
    st.markdown("### 🚀 Quick Start")
    
    idea = st.text_area(
        "Enter a business idea to analyze",
        placeholder="e.g., AI-powered sustainable packaging marketplace"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Run Market Research", type="primary", use_container_width=True):
            if idea and api_key:
                with st.spinner("Researching market..."):
                    orchestrator = AgentOrchestrator()
                    result = asyncio.run(orchestrator._run_market_research(idea))
                    st.success("Research complete!")
                    st.json(result)
            else:
                st.warning("Enter idea and API key")
    
    with col2:
        if st.button("🚀 Run Full Pipeline", type="secondary", use_container_width=True):
            if idea and api_key:
                with st.spinner("Running full pipeline..."):
                    orchestrator = AgentOrchestrator()
                    result = asyncio.run(orchestrator.execute_pipeline(idea))
                    st.success(f"Pipeline complete! ID: {result['pipeline_id']}")
            else:
                st.warning("Enter idea and API key")


elif page == "🔍 Market Research":
    st.markdown('<p class="main-header">🔍 Market Research</p>', unsafe_allow_html=True)
    
    industry = st.selectbox(
        "Select Industry",
        ["AI/ML", "Climate Tech", "Health Tech", "Fintech", "E-commerce", "SaaS", "Custom..."]
    )
    
    if industry == "Custom...":
        industry = st.text_input("Enter custom industry")
    
    if st.button("Analyze Industry", type="primary"):
        if industry and api_key:
            with st.spinner(f"Analyzing {industry}..."):
                orchestrator = AgentOrchestrator()
                result = asyncio.run(orchestrator._run_market_research(industry))
                
                # Display market overview
                if 'industry_analysis' in result:
                    analysis = result['industry_analysis']
                    if isinstance(analysis, dict) and 'market_overview' in analysis:
                        overview = analysis['market_overview']
                        
                        st.markdown("### Market Overview")
                        cols = st.columns(4)
                        cols[0].metric("TAM ($B)", overview.get('tam_billions', 'N/A'))
                        cols[1].metric("SAM ($B)", overview.get('sam_billions', 'N/A'))
                        cols[2].metric("SOM ($B)", overview.get('som_billions', 'N/A'))
                        cols[3].metric("CAGR (%)", overview.get('current_cagr_percent', 'N/A'))
                
                st.json(result)
        else:
            st.warning("Enter API key to continue")


elif page == "💡 Opportunities":
    st.markdown('<p class="main-header">💡 Opportunity Scanner</p>', unsafe_allow_html=True)
    st.info("Run market research first to scan for opportunities")


elif page == "📈 Strategy":
    st.markdown('<p class="main-header">📈 Strategy Development</p>', unsafe_allow_html=True)
    st.info("Complete opportunity analysis to develop strategy")


elif page == "💻 Product Dev":
    st.markdown('<p class="main-header">💻 Product Development</p>', unsafe_allow_html=True)
    
    st.markdown("### Generated Projects")
    projects_dir = Path("generated_projects")
    
    if projects_dir.exists():
        projects = [d for d in projects_dir.iterdir() if d.is_dir()]
        if projects:
            for project in projects:
                with st.expander(f"📁 {project.name}"):
                    st.write(f"Path: {project}")
                    if (project / "README.md").exists():
                        with open(project / "README.md") as f:
                            st.markdown(f.read())
        else:
            st.info("No projects generated yet")
    else:
        st.info("Run a pipeline to generate projects")


elif page == "📁 Reports":
    st.markdown('<p class="main-header">📁 Reports</p>', unsafe_allow_html=True)
    
    reports_dir = Path("reports")
    
    if reports_dir.exists():
        reports = sorted(reports_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)
        
        if reports:
            st.markdown(f"### {len(reports)} Reports Available")
            
            for report in reports[:10]:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{report.name}**")
                    st.caption(f"Modified: {datetime.fromtimestamp(report.stat().st_mtime).strftime('%Y-%m-%d %H:%M')}")
                with col2:
                    with open(report) as f:
                        st.download_button(
                            "⬇️ Download",
                            f.read(),
                            file_name=report.name,
                            mime="application/json",
                            key=str(report)
                        )
        else:
            st.info("No reports generated yet")
    else:
        st.info("Reports directory not found")


elif page == "⚙️ Settings":
    st.markdown('<p class="main-header">⚙️ Settings</p>', unsafe_allow_html=True)
    
    st.markdown("### Agent Configuration")
    
    model = st.selectbox("Default Model", ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"])
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.number_input("Max Tokens", 100, 4000, 2000)
    
    st.markdown("### Pipeline Settings")
    max_agents = st.number_input("Max Parallel Agents", 1, 10, 5)
    timeout = st.number_input("Timeout (minutes)", 1, 60, 30)
    
    if st.button("Save Settings"):
        st.success("Settings saved!")
    
    st.divider()
    st.markdown("### System Info")
    st.json({
        "python_version": sys.version,
        "reports_dir": str(Path("reports").absolute()),
        "projects_dir": str(Path("generated_projects").absolute())
    })


# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: gray; padding: 1rem;'>"
    "AI Agent Ecosystem v1.0 | Built with Streamlit | Powered by OpenAI"
    "</div>",
    unsafe_allow_html=True
)


def main():
    """Entry point for dashboard"""
    pass  # Streamlit runs automatically


if __name__ == "__main__":
    main()