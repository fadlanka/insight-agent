from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3")

def generate_wishlist_response(event: str, item: str, content: str) -> str:
    prompt = f"""
You are a thoughtful personal companion.

The user just expressed something about their wishlist.

Event: {event}
Item: {item}
Content: {content}

Respond in Indonesian:
- acknowledge what they said
- ask ONE reflective follow-up question if appropriate
- keep it short (1–2 sentences)
- no financial advice unless asked

Response:
"""
    return llm.invoke(prompt)
