"""
Coding Agent: MAker-Checker loop for code generation and review.
"""
import logging
from pathlib import Path
from unittest import result
from app.tools.file_writer import write_code_file
from urllib import request
from app.agents.model_router import ModelRouter
from app.rag.embedder import CPUEmbedder
from app.core.config import settings

logger = logging.getLogger(__name__)

class CodingAgent:
    def __init__(self, repo_path: str = "."):
        self.router = ModelRouter()
        # Convert to absolute path for consistency
        self.repo_path = Path(repo_path).resolve()
        self.rag = CPUEmbedder(db_path=str(self.repo_path / "chroma_db"))
    def _get_context(self, query: str) -> str:
        """Generate context for code generation."""
        results = self.rag.search(query, top_k = 3)
        if not results:
            logger.warning("No relevant code chunks found for query, proceeding with empty context.")
            return "No relevant code found in project."
        
        context_parts = []
        for doc, meta in results:
            context_parts.append(f"[File: {meta['file']} (Lines: {meta['start_line']}-{meta['end_line']})]\n{doc}")
        return "\n\n---\n\n".join(context_parts)
    def implement(self, request: str, max_iterations: int = None) -> dict:
        """ 
        Run maker-checker loop until code is approved.
        Returns: {"status": "success/partial", "code": "...", "iterations": N}
        """
        logger.info(f"Received implementation request: {request}")
        max_iter = max_iterations or settings.MAX_ITERATIONS
        current_code = ""

        MAKER_PROMPT = """You are a expert software developer.
        Write clean, production-ready code. Include type hints, error handling, and comments.
        Output ONLY the code block. No explanations.
        Use the context provided to inform your implementation, 
        but do not feel constrained by it if you have a better solution in mind.
        IMPORTANT: Output ONLY the code block. No explanations, no markdown fences, no text before or after.
        Start directly with: def or import or class"""

        CHECKER_SYSTEM = """You are a strict code reviewer. 
        Check for: bugs, missing error handling, style issues, security risks.
        Reply ONLY with: APPROVED or NEEDS_REVISION: [specific feedback like what needs to be fixed]"""

        for i in range(1, max_iter + 1):
            logger.info(f"--- Iteration {i} ---")
            context = self._get_context(request)
            logger.debug(f"Context for iteration {i}:\n{context}")
            
            # Step 1: Maker generates code
            maker_input = f"{MAKER_PROMPT}\n\nPROJECT CONTEXT:\n{context}\n\nUSER REQUEST:\n{request}"
            if current_code:
                maker_input += f"\n\nPREVIOUS CODE:\n{current_code}\nFix the issues mentioned in the review and improve the code."

            current_code = self.model_router.run_maker(MAKER_PROMPT, maker_input)
            logger.info(f"Maker generated code (iteration {i}):\n{current_code}")


            if  "```" in current_code:
                current_code = current_code.split("```")[1].split("```")[0].strip()
            else:
                lines =  current_code.split('\n')
                code_lines = []
                for line in lines:
                    if line.strip() and not line.strip().startswith("# REVIEWER"):
                        code_lines.append(line)
                    elif line.strip().startswith("# REVIEWER"):
                        break  # Stop at reviewer notes
                current_code = "\n".join(code_lines).strip()

            # Step 2: Checker reviews code
            logger.info(f"Checcker reviewing code")
            
            checker_input = f"{CHECKER_SYSTEM}\n\nCODE TO REVIEW:\n{current_code}"
            review_result = self.model_router.run_planner(checker_input, current_code)
            logger.info(f"Checker review result (iteration {i}): {review_result}")

            if review_result.strip().upper() == "APPROVED":
                logger.info(f"Code approved after {i} iterations.")
                return {"status": "success", "code": current_code, "iterations": i}
                

            feedback = review_result.replace("NEEDS_REVISION:", "").strip()
            logger.info(f"Code needs revision after iteration {i}. Feedback: {review_result}")
            maker_input += f"\n\nREVIEW FEEDBACK:\n{feedback}\nPlease revise the code accordingly."


        logger.warning(f"Max iterations reached. Returning last code version with partial status.")
        return {"status": "partial", "code": current_code, "iterations": max_iter}
    
    
    def implement_and_save(self, request: str, target_file: str, max_iterations: int = None) -> dict:
        """
        Generate code AND save it to a file.
        
        Args:
            request: What to implement
            target_file: Where to save the code (e.g., "app/utils/loader.py")
            max_iterations: Max maker-checker loops
            
        Returns:
            Same as implement(), plus "file_written": True/False
    """
        result = self.implement(request, max_iterations)
        
        if result["status"] in ["success", "partial"]:
            # Ensure target_file is absolute
            target_path = Path(target_file)
            if not target_path.is_absolute():
                target_path = self.repo_path / target_path
            result["file_written"] = write_code_file(str(target_path), result["code"], overwrite=True)
        else:
            result["file_written"] = False
        
        return result