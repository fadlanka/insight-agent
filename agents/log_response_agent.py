from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3")

def generate_log_response(category: str, content: str) -> str:
    prompt = f"""
You are a calm personal companion.

The user just logged something related to:
Category: {category}
Content: {content}

Respond naturally in Indonesian:
- Acknowledge the log
- Ask ONE gentle follow-up question if appropriate
- Do not give advice unless asked
- Be short (1–2 sentences)

Response:
"""
    return llm.invoke(prompt)