import pytest
from unittest.mock import patch, MagicMock

from mcp.policy import MCPPolicy

def test_curhat_without_command_does_not_write():
    mcp = MCPPolicy()

    user_input = "saya lagi capek"

    with patch("api.api_client.post_daily_log") as mock_post:
        allowed = mcp.allow_write(user_input)

        assert allowed is False
        mock_post.assert_not_called()

def test_log_command_allows_write():
    mcp = MCPPolicy()

    user_input = "/log saya lagi capek"

    with patch("api.api_client.post_daily_log") as mock_post:
        if mcp.allow_write(user_input):
            mock_post({"category": "mood", "content": "capek", "raw_text": "saya lagi capek"})

        mock_post.assert_called_once()

def test_insight_blocked_without_context():
    mcp = MCPPolicy()

    context = ""

    allowed = mcp.allow_insight(context)
    assert allowed is False

def test_insight_allowed_with_context():
    mcp = MCPPolicy()

    context = "DAILY LOG:\nSaya sering bad mood"

    allowed = mcp.allow_insight(context)
    assert allowed is True

def test_guard_response_applied_in_flow():
    mcp = MCPPolicy()

    dangerous_response = "Kamu depresi dan seharusnya istirahat total."

    safe_response = mcp.guard_response(dangerous_response)

    assert "depresi" not in safe_response.lower()
    assert "seharusnya" not in safe_response.lower()

def test_full_log_flow_with_mcp():
    mcp = MCPPolicy()

    user_input = "/log saya lagi badmood"

    fake_interpretation = {
        "category": "mood",
        "content": "bad mood",
        "raw_text": "saya lagi badmood"
    }

    with patch("router.log_interpreter.interpret_log", return_value=fake_interpretation), \
         patch("api.api_client.post_daily_log") as mock_post:

        if mcp.allow_write(user_input):
            mock_post(fake_interpretation)

        mock_post.assert_called_once_with(fake_interpretation)
