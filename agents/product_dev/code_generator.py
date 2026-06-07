from agents.base_agent import BaseAgent
from typing import Dict, List
from pathlib import Path
from loguru import logger
import json
import os

class CodeGenerationAgent(BaseAgent):
    """Agent that generates actual application code"""
    
    def __init__(self):
        super().__init__("Code Generation Agent", model="gpt-4-turbo-preview")
        self.output_dir = Path("generated_projects")
        self.output_dir.mkdir(exist_ok=True)
        logger.info("Code Generation Agent ready")
    
    async def generate_fullstack_app(self, prd: Dict) -> Dict:
        """Generate complete fullstack application"""
        
        logger.info("Generating fullstack application")
        
        project_name = prd.get("product_vision", {}).get("elevator_pitch", "generated_app")
        project_name = project_name.lower().replace(" ", "_")[:30]
        project_dir = self.output_dir / project_name
        project_dir.mkdir(exist_ok=True)
        
        # Generate all components
        backend = await self._generate_backend(prd, project_dir)
        frontend = await self._generate_frontend(prd, project_dir)
        database = await self._generate_database_schema(prd, project_dir)
        docker = await self._generate_docker_files(prd, project_dir)
        
        # Generate README
        readme = await self._generate_readme(prd, project_dir)
        
        return {
            "project_name": project_name,
            "project_path": str(project_dir),
            "components": {
                "backend": backend,
                "frontend": frontend,
                "database": database,
                "docker": docker,
                "readme": readme
            }
        }
    
    async def _generate_backend(self, prd: Dict, project_dir: Path) -> Dict:
        """Generate FastAPI backend"""
        
        backend_dir = project_dir / "backend"
        backend_dir.mkdir(exist_ok=True)
        
        # Generate main application
        main_py = await self.think(f"""
        Generate a complete FastAPI backend application with:
        - Main app configuration
        - CORS middleware
        - Database connection
        - Router includes
        - Error handlers
        - Logging configuration
        
        Based on these requirements:
        {json.dumps(prd.get('technical_requirements', {}), indent=2)}
        
        Provide complete, runnable Python code.
        """)
        
        # Write main.py
        with open(backend_dir / "main.py", "w") as f:
            f.write(main_py)
        
        # Generate models
        models = await self.think(f"""
        Generate SQLAlchemy database models for:
        {json.dumps(prd.get('features', []), indent=2)}
        
        Include:
        - All tables with relationships
        - Indexes
        - Constraints
        - Timestamps
        """)
        
        # Create models directory
        models_dir = backend_dir / "models"
        models_dir.mkdir(exist_ok=True)
        
        with open(models_dir / "models.py", "w") as f:
            f.write(models)
        
        # Generate API routes
        routes = await self.think(f"""
        Generate FastAPI route handlers for these features:
        {json.dumps(prd.get('features', []), indent=2)}
        
        Include:
        - CRUD operations
        - Input validation with Pydantic
        - Authentication decorators
        - Error handling
        - Pagination
        - Filtering and sorting
        """)
        
        routes_dir = backend_dir / "routes"
        routes_dir.mkdir(exist_ok=True)
        
        with open(routes_dir / "routes.py", "w") as f:
            f.write(routes)
        
        # Generate requirements
        with open(backend_dir / "requirements.txt", "w") as f:
            f.write("""fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
alembic==1.13.0
""")
        
        return {
            "main_app": str(backend_dir / "main.py"),
            "models": str(models_dir / "models.py"),
            "routes": str(routes_dir / "routes.py")
        }
    
    async def _generate_frontend(self, prd: Dict, project_dir: Path) -> Dict:
        """Generate React frontend"""
        
        frontend_dir = project_dir / "frontend"
        frontend_dir.mkdir(exist_ok=True)
        
        # Generate package.json
        package_json = {
            "name": project_dir.name,
            "version": "1.0.0",
            "private": True,
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "axios": "^1.6.0",
                "@mui/material": "^5.15.0",
                "react-router-dom": "^6.21.0"
            }
        }
        
        with open(frontend_dir / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)
        
        # Generate main App component
        app_jsx = await self.think(f"""
        Generate a React App.jsx component with:
        - React Router setup
        - Navigation bar
        - Theme provider
        - Authentication context
        - Error boundary
        
        Features to implement:
        {json.dumps(prd.get('features', []), indent=2)}
        """)
        
        src_dir = frontend_dir / "src"
        src_dir.mkdir(exist_ok=True)
        
        with open(src_dir / "App.jsx", "w") as f:
            f.write(app_jsx)
        
        return {
            "package_json": str(frontend_dir / "package.json"),
            "app_component": str(src_dir / "App.jsx")
        }
    
    async def _generate_database_schema(self, prd: Dict, project_dir: Path) -> Dict:
        """Generate database schema and migrations"""
        
        db_dir = project_dir / "database"
        db_dir.mkdir(exist_ok=True)
        
        schema_sql = await self.think(f"""
        Generate PostgreSQL database schema for:
        {json.dumps(prd.get('features', []), indent=2)}
        
        Include:
        - CREATE TABLE statements
        - Foreign keys
        - Indexes
        - Constraints
        - Comments
        - Seed data
        """)
        
        with open(db_dir / "schema.sql", "w") as f:
            f.write(schema_sql)
        
        return {"schema": str(db_dir / "schema.sql")}
    
    async def _generate_docker_files(self, prd: Dict, project_dir: Path) -> Dict:
        """Generate Docker and deployment files"""
        
        dockerfile = """FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        
        with open(project_dir / "Dockerfile", "w") as f:
            f.write(dockerfile)
        
        docker_compose = f"""version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/{project_dir.name}
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB={project_dir.name}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/schema.sql:/docker-entrypoint-initdb.d/schema.sql

volumes:
  postgres_data:
"""
        
        with open(project_dir / "docker-compose.yml", "w") as f:
            f.write(docker_compose)
        
        return {
            "dockerfile": str(project_dir / "Dockerfile"),
            "docker_compose": str(project_dir / "docker-compose.yml")
        }
    
    async def _generate_readme(self, prd: Dict, project_dir: Path) -> str:
        """Generate project README"""
        
        readme = await self.think(f"""
        Generate a comprehensive README.md for this project:
        {json.dumps(prd.get('product_vision', {}), indent=2)}
        
        Include:
        - Project description
        - Features
        - Tech stack
        - Setup instructions
        - API documentation overview
        - Deployment guide
        - Contributing guidelines
        """)
        
        with open(project_dir / "README.md", "w") as f:
            f.write(readme)
        
        return str(project_dir / "README.md")