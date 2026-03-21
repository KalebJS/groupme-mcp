import os

import pytest

os.environ.setdefault("GROUPME_TOKEN", "test-token")

from groupme_mcp.server import mcp

EXPECTED_TOOLS = {
    # Groups
    "list_groups",
    "list_former_groups",
    "get_group",
    "create_group",
    "update_group",
    "destroy_group",
    "join_group",
    "rejoin_group",
    # Members
    "add_members",
    "get_member_results",
    "remove_member",
    "update_membership",
    # Messages
    "list_messages",
    "send_message",
    # Direct messages
    "list_direct_messages",
    "send_direct_message",
    # Chats
    "list_chats",
    # Likes
    "like_message",
    "unlike_message",
    # Bots
    "create_bot",
    "post_as_bot",
    "list_bots",
    "destroy_bot",
    # Users
    "get_me",
    "update_user",
    # Blocks
    "list_blocks",
    "check_block",
    "create_block",
    "delete_block",
}


def test_all_tools_registered():
    registered = {t.name for t in mcp._tool_manager.list_tools()}
    assert registered == EXPECTED_TOOLS


def test_tools_have_descriptions():
    for tool in mcp._tool_manager.list_tools():
        assert tool.description, f"Tool '{tool.name}' is missing a description"


@pytest.mark.asyncio
async def test_send_message_autogenerates_guid(httpx_mock):
    from groupme_mcp.server import send_message

    httpx_mock.add_response(status_code=201, json={"response": {"message": {"id": "1"}}})
    await send_message(group_id="123", text="hi")
    import json

    request = httpx_mock.get_requests()[0]
    body = json.loads(request.content)
    assert body["message"]["source_guid"]  # should be auto-generated


@pytest.mark.asyncio
async def test_send_direct_message_autogenerates_guid(httpx_mock):
    from groupme_mcp.server import send_direct_message

    httpx_mock.add_response(status_code=201, json={"response": {"direct_message": {"id": "1"}}})
    await send_direct_message(recipient_id="user-1", text="hey")
    import json

    request = httpx_mock.get_requests()[0]
    body = json.loads(request.content)
    assert body["direct_message"]["source_guid"]
