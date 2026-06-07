# setup_path.py
"""
Run this once to setup Python path correctly
"""
import sys
import site
from pathlib import Path

# Get project root
project_root = Path(__file__).resolve().parent

# Add to site-packages as .pth file
site_packages = Path(site.getsitepackages()[0])
pth_file = site_packages / "ai_agent_ecosystem.pth"

with open(pth_file, 'w') as f:
    f.write(str(project_root))

print(f"✅ Added {project_root} to Python path")
print(f"✅ Created {pth_file}")
print("\nNow restart VS Code and you won't have import errors!")