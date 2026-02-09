from langchain_ollama import OllamaLLM
import json

llm = OllamaLLM(model="llama3")

def interpret_wishlist(message: str) -> dict:
    prompt = f"""
You are a wishlist interpretation assistant.

From the user message, infer:
- event (desire, doubt, evaluation, update, cancel, other)
- item (if mentioned, else "unknown")
- content (short summary, max 6 words)
- raw_text (original message)

IMPORTANT RULES:
- Wanting or thinking of buying = desire
- Saying expensive, berat, ga realistis = doubt
- Assessing feasibility = evaluation

User message:
"{message}"

Return ONLY valid JSON.
"""

    response = llm.invoke(prompt)

    try:
        return json.loads(response)
    except:
        return {
            "event": "other",
            "item": "unknown",
            "content": message,
            "raw_text": message
        }
