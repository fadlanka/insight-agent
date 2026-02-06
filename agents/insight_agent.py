from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3")

def generate_insight(context: str, question: str) -> str:
    prompt = f"""
You are a personal insight agent.

Rules:
- Be honest and practical
- Do not judge
- Do not invent data
- Base answers only on context

Context:
{context}

Question:
{question}

Answer:
"""
    return llm.invoke(prompt)
