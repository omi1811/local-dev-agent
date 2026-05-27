"""
Start code chunking for RAG.
Split the input text into smaller chunks for better processing and retrieval.
"""

from email.mime import text
from typing import List, Dict
from pathlib import Path
import logging


logger = logging.getLogger(__name__)

class CodeChunker:
    """
    Splits code files into chunks for embedding.
    Respects code structure (functions, classes).
    """
    
    def __init__(self, chunk_size: int = 600, overlap: int = 100):
        """
        Args:
            chunk_size: Maximum characters per chunk
            overlap: Overlap between chunks (preserves context)
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        

    def chunk_files(self, files: Dict[str, str]) -> List[str]:
        """
        Chunk multiple files.
        
        Args:
            files: Dict of {filepath: content}
            
        Returns:
            List of chunk dicts with metadata
        """
        all_chunks = []
        for file_path, content in files.items():
            chunks = self.chunk_code(file_path, content)
            all_chunks.extend(chunks)

        logger.info(f"Total chunks created: {len(all_chunks)} from {len(files)} files")
        return all_chunks

    def chunk_code(self,file_path: str, content: str) -> List[str]:
        """
        Chunk a single code file.

        Args:
            file_path: Path to the code file
            code: Content of the code file

        Returns:
            List of chunk strings
        """
        ext = Path(file_path).suffix.lower()
        chunks = []
        separators = self._get_separators(ext)
        
        current_chunk = ""
        current_line = 0

        lines = content.split('\n')
        for i, line in enumerate(lines):
            # Check if adding this line exceeds chunk size
            if len(current_chunk) + len(line) > self.chunk_size and current_chunk:
                # Save current chunk with metadata
                chunks.append({
                    "text": current_chunk.strip(),
                    "metadata": {
                        "file": file_path,
                        "start_line": current_line,
                        "end_line": i,
                        "language": ext
                    }
                })
                #store overlap lines for next chunk
                overlap_lines = current_chunk.split('\n')[-3:]
                current_chunk = '\n'.join(overlap_lines) + '\n'
                current_line = i - 3
                
            
            current_chunk = line + '\n'

        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "metadata": {
                    "file": file_path,
                    "start_line": current_line,
                    "end_line": len(lines),
                    "language": ext
                }
            })
        return chunks   
    def _get_separators(self, ext: str) -> List[str]:
        """Get code-aware separators by language"""
        separators = {
            ".py": ["\n\nclass ", "\n\ndef ", "\n\nasync def ", "\n\n"],
            ".js": ["\n\nfunction ", "\n\nclass ", "\n\nconst ", "\n\n"],
            ".ts": ["\n\nfunction ", "\n\nclass ", "\n\nconst ", "\n\n"],
            ".java": ["\n\npublic class ", "\n\nprivate ", "\n\npublic "],
        }
        return separators.get(ext, ["\n\n", "\n", ". ", " "])