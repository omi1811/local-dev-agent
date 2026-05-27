from pathlib import Path
from typing import Dict
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

supported_extensions = {
    ".py", ".js", ".java", ".txt", ".md", ".dockerfile", ".yaml", ".yml", ".json", ".xml", ".html", ".css"
    }

IGNORE_DIRS = {
    ".venv", ".venv1", "__pycache__",".git","node_modules",".idea",".vscode", "dist","build"
    }
def load_repository(repo_path: str) -> dict[str, str]:
    repo_files = {}
    repo_root = Path(repo_path).resolve()
    logger.info(f"Loading repository from: {repo_root}")


    for file_path in repo_root.rglob("*"):
        if any(ignore_dir in file_path.parts for ignore_dir in IGNORE_DIRS):
            continue

        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:   
            try:
                if file_path.stat().st_size > 5 * 1024 * 1024:  # Skip files larger than 5MB
                    logger.warning(f"Skipping large file: {file_path} ({file_path.stat().st_size} bytes)")
                    continue

                relative_path = file_path.relative_to(repo_root)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    repo_files[str(relative_path)] = content

            except Exception as e:
                logger.error(f"Error reading {file_path}: {e}")


    logger.info(f"Finished loading repository. Total files loaded: {len(repo_files)}")
    return repo_files