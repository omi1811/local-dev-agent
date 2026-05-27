"""
Test the maker-checker loop on a simple request.
"""
import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agents.coding_agent import CodingAgent

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def test_simple_request():
    print("🚀 Testing CodingAgent with a simple request...\n")
    
    # Initialize agent (loads ChromaDB + model router)
    agent = CodingAgent(repo_path=".")
    
    # Simple request that should match your existing code
    request = "Create a function that loads a repository and returns a list of .py files only."
    
    result = agent.implement(request, max_iterations=2)
    
    print("\n" + "="*50)
    print(f"STATUS: {result['status']}")
    print(f"ITERATIONS: {result['iterations']}")
    print("GENERATED CODE:\n")
    print(result['code'])
    print("="*50)

if __name__ == "__main__":
    test_simple_request()