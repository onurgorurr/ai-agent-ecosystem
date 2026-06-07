#!/usr/bin/env python3
"""
Streamlit dashboard for AI Agent Ecosystem
"""
import streamlit as st
import sys
from pathlib import Path
import asyncio
import json
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from orchestrator.execution_engine import AgentOrchestrator

st.set_page_config(
    page_title="AI Agent Ecosystem",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Agent Ecosystem Dashboard")
st.markdown("### Market Research & Product Development System")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    
    api_key = st.text_input("OpenAI API Key", type="password")
    if api_key:
        import os
        os.environ["OPENAI_API_KEY"] = api_key
    
    st.divider()
    
    mode = st.radio(
        "Select Mode",
        ["Market Research", "Opportunity Analysis", "Full Pipeline"]
    )
    
    st.divider()
    st.markdown("### About")
    st.info(
        "This system uses multiple AI agents to research markets, "
        "identify opportunities, and generate product code."
    )

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    idea = st.text_area(
        "Enter your business idea",
        placeholder="e.g., AI-powered sustainable packaging marketplace",
        height=100
    )
    
    if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
        if not idea:
            st.warning("Please enter a business idea")
        elif not api_key:
            st.warning("Please enter your OpenAI API key in the sidebar")
        else:
            with st.spinner("Running AI agents..."):
                orchestrator = AgentOrchestrator()
                
                if mode == "Market Research":
                    results = asyncio.run(orchestrator._run_market_research(idea))
                    
                    st.success("Market Research Complete!")
                    
                    # Display results
                    if 'industry_analysis' in results:
                        analysis = results['industry_analysis']
                        
                        if 'market_overview' in analysis:
                            overview = analysis['market_overview']
                            
                            st.subheader("Market Overview")
                            metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                            
                            with metrics_col1:
                                st.metric("TAM", f"${overview.get('tam_billions', 'N/A')}B")
                            with metrics_col2:
                                st.metric("CAGR", f"{overview.get('current_cagr_percent', 'N/A')}%")
                            with metrics_col3:
                                st.metric("Market Maturity", overview.get('market_maturity', 'N/A'))
                        
                        # Trends
                        if 'trends' in analysis:
                            st.subheader("Top Market Trends")
                            for trend in analysis['trends'][:5]:
                                with st.expander(f"📈 {trend.get('trend_name', 'Trend')}"):
                                    st.write(f"**Impact Score:** {trend.get('impact_score', 'N/A')}/10")
                                    st.write(f"**Time to Mainstream:** {trend.get('time_to_mainstream_months', 'N/A')} months")
                                    st.write(f"**Confidence:** {trend.get('confidence_level', 'N/A')}%")
                
                elif mode == "Full Pipeline":
                    results = asyncio.run(orchestrator.execute_pipeline(idea))
                    
                    st.success("Pipeline Complete!")
                    
                    # Show summary
                    st.subheader("Pipeline Results")
                    st.json(results.get('summary', {}))
                    
                    # Download report
                    st.download_button(
                        "📥 Download Full Report",
                        data=json.dumps(results, indent=2, default=str),
                        file_name=f"pipeline_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )

with col2:
    st.subheader("Recent Pipelines")
    
    reports_dir = Path("reports")
    if reports_dir.exists():
        reports = list(reports_dir.glob("*.json"))
        if reports:
            for report in sorted(reports, reverse=True)[:5]:
                st.text(f"📄 {report.name}")
        else:
            st.info("No reports yet")
    
    st.divider()
    
    st.subheader("Quick Stats")
    st.metric("Agents Available", "15+")
    st.metric("Market Coverage", "All Industries")
    st.metric("Output Formats", "JSON, Code, Docs")

# Footer
st.divider()
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "AI Agent Ecosystem v1.0 | Powered by GPT-4"
    "</div>",
    unsafe_allow_html=True
)