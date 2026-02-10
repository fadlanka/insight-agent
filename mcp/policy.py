class MCPPolicy:

    def allow_write(self, command: str, confirmed: bool = False) -> bool:
        if not command:
            return False

        cmd = command.strip().lower()

        if cmd.startswith("/log") or cmd.startswith("/wishlist"):
            return True

        if confirmed:
            return True

        return False

    def allow_insight(self, context: str) -> bool:
        return bool(context and context.strip())

    def guard_response(self, response: str) -> str:
        banned_phrases = [
            "kamu depresi",
            "kamu pasti",
            "seharusnya kamu",
        ]
        for phrase in banned_phrases:
            if phrase in response.lower():
                return "Aku mungkin belum punya cukup konteks untuk menyimpulkan sejauh itu."
        return response
