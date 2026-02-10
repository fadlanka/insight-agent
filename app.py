from router.intent_router import route_intent
from retrievers.daily_retriever import get_daily_retriever
from retrievers.wishlist_retriever import get_wishlist_retriever
from agents.insight_agent import generate_insight
from router.log_interpreter import interpret_log
from api.api_client import post_daily_log, post_wishlist
from router.wishlist_interpreter import interpret_wishlist
from agents.wishlist_response_agent import generate_wishlist_response
from agents.log_response_agent import generate_log_response
from ingestions.auto_ingest import ingest_daily, ingest_wishlist
from mcp.policy import MCPPolicy
import shlex

mcp = MCPPolicy()


def is_daily_log_command(text: str) -> bool:
    return text.startswith("/log")

def is_wishlist_command(text: str) -> bool:
    return text.startswith("/wishlist")


def main():
    question = input("You: ")

    # === COMMAND MODE (WRITE) ===
    if question.startswith("/log"):
        if not mcp.allow_write(question):
            confirm = input("AI: Aku perlu izin sebelum mencatat ini. Lanjutkan? (y/n) ")
            if not mcp.allow_write(question, confirmed=confirm.strip().lower() in ["y", "ya", "yes"]):
                print("AI: Oke, tidak disimpan.")
                return
        message = question.replace("/log", "").strip()

        interpreted = interpret_log(message)
        result = post_daily_log(interpreted)

        # === AUTO INGEST ===
        ingest_daily()
        print("AI: Data dicatat dan diindeks ulang 🔄")
        response = generate_log_response(
            interpreted["category"],
            interpreted["content"]
        )

        print("AI:", response)
        print(result)
        return



    if question.startswith("/wishlist"):
        if not mcp.allow_write(question):
            confirm = input("AI: Aku perlu izin sebelum mencatat ini. Lanjutkan? (y/n) ")
            if not mcp.allow_write(question, confirmed=confirm.strip().lower() in ["y", "ya", "yes"]):
                print("AI: Oke, tidak disimpan.")
                return
        message = question.replace("/wishlist", "").strip()

        interpreted = interpret_wishlist(message)
        result = post_wishlist(interpreted)

        # === AUTO INGEST ===
        ingest_wishlist()
        print("AI: Data dicatat dan diindeks ulang 🔄")
        response = generate_wishlist_response(
            interpreted["event"],
            interpreted["item"],
            interpreted["content"]
        )

        print("AI:", response)
        print(result)
        return

    # === INSIGHT MODE (READ) ===
    intent = route_intent(question)

    context_parts = []

    if intent in ["daily_log", "both"]:
        retriever = get_daily_retriever()
        docs = retriever.invoke(question)
        context_parts.append(
            "DAILY LOG:\n" + "\n".join(d.page_content for d in docs)
        )

    if intent in ["wishlist", "both"]:
        retriever = get_wishlist_retriever()
        docs = retriever.invoke(question)
        context_parts.append(
            "WISHLIST:\n" + "\n".join(d.page_content for d in docs)
        )

    context = "\n\n".join(context_parts)
    answer = generate_insight(context, question)
    print("\nAI:", answer)


def parse_wishlist_command(text: str) -> dict:
    """
    Format:
    /wishlist item="Laptop kerja" harga=15000000 target=12 prioritas=tinggi alasan="produktif"
    """
    data = {}

    parts = shlex.split(text.replace("/wishlist", "").strip())
    for part in parts:
        if "=" in part:
            key, val = part.split("=", 1)
            data[key] = val.strip('"')

    return {
        "item": data.get("item", ""),
        "harga": int(data.get("harga", 0)),
        "target_bulan": int(data.get("target", 0)),
        "prioritas": data.get("prioritas", ""),
        "alasan": data.get("alasan", ""),
        "kebiasaan_terkait": data.get("kebiasaan", "")
    }



if __name__ == "__main__":
    main()
