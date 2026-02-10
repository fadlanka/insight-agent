import pytest
from mcp.policy import MCPPolicy

mcp = MCPPolicy()

def test_allow_write_with_log_command():
    assert mcp.allow_write("/log saya lagi capek") is True

def test_allow_write_with_wishlist_command():
    assert mcp.allow_write("/wishlist pengen beli laptop") is True

def test_disallow_write_without_command_and_confirmation():
    assert mcp.allow_write("saya lagi capek") is False

def test_allow_write_with_confirmation():
    assert mcp.allow_write("saya lagi capek", confirmed=True) is True

def test_allow_insight_with_context():
    context = "DAILY LOG:\nSaya sering bad mood karena tidur kurang"
    assert mcp.allow_insight(context) is True

def test_disallow_insight_without_context():
    assert mcp.allow_insight("") is False
    assert mcp.allow_insight("   ") is False
    assert mcp.allow_insight(None) is False

def test_guard_response_blocks_diagnosis():
    response = "Kamu depresi dan harus istirahat."
    guarded = mcp.guard_response(response)

    assert "depresi" not in guarded.lower()

def test_guard_response_allows_safe_reflection():
    response = "Sepertinya kamu lagi capek. Mau cerita lebih lanjut?"
    guarded = mcp.guard_response(response)

    assert guarded == response
