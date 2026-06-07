from setuptools import setup, find_packages

setup(
    name="ai-agent-ecosystem",
    version="1.0.0",
    description="Multi-agent AI system for market research and product development",
    author="AI Agent Team",
    packages=find_packages(),
    install_requires=[
        "openai>=1.12.0",
        "anthropic>=0.18.0",
        "langchain>=0.1.0",
        "pandas>=2.1.0",
        "fastapi>=0.104.0",
        "streamlit>=1.29.0",
    ],
    python_requires=">=3.10",
)