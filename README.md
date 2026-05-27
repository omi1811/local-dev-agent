# 🤖 Local AI Coding Agent

> A fully local, open-source AI coding assistant that reads your codebase, writes production-ready code, and reviews its own work. Runs on your machine with **zero API costs** and optimized for **low VRAM (4GB+)**.

---

## 📖 Overview

This project is a **learning-focused, production-structured AI coding agent** built from scratch. Instead of relying on cloud APIs, it uses open-source local models, vector search (RAG), and an autonomous maker-checker workflow to help you generate, refine, and save code directly in your projects.

Designed for beginners who want to understand **how modern AI coding tools actually work under the hood**, while remaining practical enough for daily development.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🏠 **100% Local** | No internet, no API keys, no monthly fees. Runs entirely on your machine. |
| 🧠 **Repository-Aware RAG** | Automatically reads your project, chunks code, and retrieves relevant context before generating. |
| 🔄 **Maker-Checker Loop** | One model writes code, another reviews it. Loops until approved or max iterations reached. |
|  **Low VRAM Optimized** | Works on 4GB VRAM or CPU-only. Models load sequentially to prevent OOM crashes. |
| 🌍 **Run Anywhere** | CLI accepts `--repo` and `--output` flags. Point it at any project on your machine. |
| 🔍 **Dry-Run Mode** | Preview generated code before saving to disk. |
|  **Modular Architecture** | Clean separation: RAG → Agent → Tools → CLI. Easy to extend or replace components. |

---

## ️ Tech Stack

| Component | Technology |
|-----------|------------|
| **LLM Runtime** | Ollama |
| **Coder Model** | `qwen2.5-coder:3b` |
| **Reviewer Model** | `phi3:mini` |
| **Vector Database** | ChromaDB |
| **Embeddings** | `sentence-transformers` (all-MiniLM-L6-v2) |
| **Backend/CLI** | Python 3.10+, `argparse`, `requests`, `pydantic` |
| **File I/O** | `pathlib`, safe overwrite protection |

---

## 🚀 Quick Start

### 1️⃣ Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed & running
- 4GB+ RAM/VRAM (CPU fallback supported)
- Git

### 2️ Installation
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/local-coding-agent.git
cd local-coding-agent

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull local models (runs once)
ollama pull qwen2.5-coder:3b
ollama pull phi3:mini
```

### 3️⃣ First Run
```bash
python cli.py --repo /path/to/your/project "Create a user login function"
```
> 💡 **Note:** First run downloads embeddings & builds the vector index. This takes 1-2 minutes. Subsequent runs are much faster.

---

##  Usage Guide

### Basic Commands
```bash
# Run in current directory
python cli.py "Add database connection pool"

# Target a specific project
python cli.py --repo ~/my-flask-app "Create JWT authentication middleware"

# Save to a different folder
python cli.py -r ~/backend -o ./generated "Build CSV parser utility"

# Preview without saving
python cli.py --repo . --dry-run "Create email validation function"
```

### CLI Arguments
| Flag | Description | Default |
|------|-------------|---------|
| `request` | What you want the AI to create | (required) |
| `-r, --repo PATH` | Target repository path | `.` |
| `-o, --output PATH` | Output directory for generated files | Same as `--repo` |
| `-m, --max-iterations N` | Max maker-checker refinement loops | `2` |
| `--dry-run` | Generate code but don't write to disk | `False` |

---

## 🧠 How It Works

```
User Request
     ↓
📚 RAG Engine (CPU)
   ├─ Loads project files
   ├─ Chunks code intelligently
   ─ Searches for relevant context
     ↓
 Maker-Checker Loop
   ├─ MAKER (Qwen2.5-Coder) writes code using context
   ├─ CHECKER (Phi-3-mini) reviews for bugs/style
   └─ Loops until APPROVED or max iterations
     ↓
 File Writer
   ├─ Validates path & permissions
   ├─ Creates directories if needed
   └─ Saves clean, reviewed code
```

### Why This Architecture?
- **RAG prevents hallucination**: The AI only generates code relevant to YOUR project structure.
- **Maker-Checker improves quality**: Self-review catches missing error handling, style issues, and security risks.
- **Sequential model loading**: Respects 4GB VRAM limits by loading one model at a time.
- **CPU embeddings**: Zero GPU memory usage for vector search.

---

## ⚙️ Configuration

### `.env` File (Optional Overrides)
```env
OLLAMA_BASE_URL=http://localhost:11434
CODER_MODEL=qwen2.5-coder:3b
PLANNER_MODEL=phi3:mini
EMBEDDING_MODEL=all-MiniLM-L6-v2
MAX_ITERATIONS=2
TEMPERATURE_CODER=0.3
TEMPERATURE_PLANNER=0.2
```

### Environment Variables
```bash
export OLLAMA_NUM_GPU=0  # Force CPU-only mode
export OLLAMA_KEEP_ALIVE=30s  # Faster VRAM cleanup
```

---

##  Troubleshooting

| Issue | Solution |
|-------|----------|
| `Ollama not running` | Start with `ollama serve` (usually auto-starts) |
| `Model not found` | Run `ollama pull qwen2.5-coder:3b phi3:mini` |
| `Permission denied` | Ensure output directory is writable: `chmod -R u+w /path` |
| `Slow generation` | Normal on CPU. Expect 1-3 min per request. |
| `Hallucinated imports` | Add more project files to RAG index or increase `top_k` |
| `VRAM OOM` | Close GPU apps, set `OLLAMA_KEEP_ALIVE=30s`, or switch to CPU |

---

##  Credits & Inspiration

- [Ollama](https://ollama.com) for local LLM runtime
- [ChromaDB](https://www.trychroma.com) for lightweight vector search
- [Qwen2.5-Coder](https://huggingface.co/Qwen/Qwen2.5-Coder) & [Phi-3](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) models


---