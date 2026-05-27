from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def write_code_file(file_path : str, content: str, overwrite: False) -> bool:
    """
    Write generated code to a file.
    
    Args:
        file_path: Where to save the file (relative to project root)
        content: The code to write
        overwrite: If False, won't overwrite existing files
        
    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(file_path)

        if path.exists() and not overwrite:
            logger.warning(f"File {file_path} already exists and overwrite is False. Skipping write.")
            return False

        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w") as f:
            f.write(content)
        logger.info(f"Code written to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error writing code to {file_path}: {e}")
        return False