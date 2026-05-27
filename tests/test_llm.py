from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="qwen2.5-coder:7b"
)

response = llm.invoke(
    "Create FastAPI CRUD example"
)

print(response)