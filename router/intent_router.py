from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3")

def route_intent(question: str) -> str:
    prompt = f"""
Classify the intent of the user message.

Options:
- daily_log
- wishlist
- both

Message:
{question}

Return only one word.
"""
    return llm.invoke(prompt).strip().lower()
