from app.rag.repo_loader import load_repository

files = load_repository(".")

print(f"Loaded {len(files)} files")

for file in files[:5]:
    print(file["path"])