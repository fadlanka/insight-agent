from langchain_ollama import OllamaLLM
import json

llm = OllamaLLM(model="llama3")

def interpret_log(message: str) -> dict:
    prompt = f"""
You are a personal logging assistant.

Your task:
Classify the user message into ONE category ONLY from:
- mood
- ibadah
- keuangan
- kesehatan
- aktivitas
- other

IMPORTANT RULES:
- Mentions of prayer (sholat, solat, salat, asar, subuh, maghrib, isya, dzuhur) MUST be categorized as "ibadah".
- Mentions of feelings (bad mood, capek, sedih, stres) MUST be "mood".
- If unsure, choose the closest category, NOT "other".

From the message, return JSON with:
- category
- content (short clean summary, max 5 words)
- raw_text (original message)

User message:
"{message}"

Return ONLY valid JSON.
"""

    response = llm.invoke(prompt)

    try:
        return json.loads(response)
    except Exception:
        return {
            "category": "other",
            "content": message,
            "raw_text": message
        }
