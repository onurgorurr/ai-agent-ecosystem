# test_imports.py
import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent))

print("Testing imports...")

try:
    from config.settings import Settings
    print("✅ config.settings")
except Exception as e:
    print(f"❌ config.settings: {e}")

try:
    from agents.base_agent import BaseAgent
    print("✅ agents.base_agent")
except Exception as e:
    print(f"❌ agents.base_agent: {e}")

try:
    from agents import TrendAnalysisAgent
    print("✅ agents.TrendAnalysisAgent")
except Exception as e:
    print(f"❌ agents.TrendAnalysisAgent: {e}")

try:
    from orchestrator.execution_engine import AgentOrchestrator
    print("✅ orchestrator.execution_engine")
except Exception as e:
    print(f"❌ orchestrator.execution_engine: {e}")

print("\nTest complete!")