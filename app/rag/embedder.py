"""
CPU-based embeddings with ChromaDB.
No GPU required for vector search.
"""

import chromadb
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Sequence, Tuple, Union
import logging

logger = logging.getLogger(__name__)

class CPUEmbedder:
    def __init__(self, db_path: str = "./chroma_db"):
        logger.info("loading CPU embedder with model all-MiniLM-L6-v2")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="code_embeddings", metadata = {"hnsw:space": "cosine"})
        logger.info("✅ CPU embedder ready")

    def embed(self, chunks: Union[str, Sequence[str]]) -> List[List[float]]:
        """
        Embed a list of code chunks.

        Args:
            chunks: List of code chunk strings

        Returns:
            Embedded vector (list of floats)
        """
        if isinstance(chunks, str):
            chunks = [chunks]
        return self.model.encode(chunks, show_progress_bar=False).tolist()
    
    def add_chunks(self, chunks: List[Dict]):
        """
        Add code chunks to database.
        
        Args:
            chunks: List of chunk dicts from CodeChunker
        """
        if not chunks:
            logger.warning("⚠️ No chunks to add")
            return
        
        # Prepare data
        ids = [f"{c['metadata']['file']}:{c['metadata']['start_line']}" for c in chunks]
        documents = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        
        # Generate embeddings
        logger.info(f"📊 Generating embeddings for {len(chunks)} chunks...")
        embeddings = self.embed(documents)
        
        # Add to ChromaDB
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )
        logger.info(f"✅ Added {len(chunks)} chunks to ChromaDB")


    def search(self, query: str, top_k: int = 3) -> List[Tuple[str, Dict]]:
        """
        Search for relevant code chunks.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of (document, metadata) tuples
        """
        # Generate query embedding
        query_embedding = self.embed(query)[0]
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas"]
        )
        
        # Format results
        return list(zip(results['documents'][0], results['metadatas'][0]))


Embedder = CPUEmbedder
    


