import os

import pytest
from pytest_httpx import HTTPXMock

os.environ.setdefault("GROUPME_TOKEN", "test-token")

from client import BASE_URL
from client import GroupMeClient

TOKEN = "test-token"
BASE = BASE_URL


@pytest.fixture
def client():
    return GroupMeClient()


# ── Groups ────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_groups(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {"groups": []}})
    result = await client.list_groups(page=2, per_page=5)
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/groups"
    assert request.url.params["page"] == "2"
    assert request.url.params["per_page"] == "5"
    assert request.url.params["token"] == TOKEN
    assert result == {"response": {"groups": []}}


@pytest.mark.asyncio
async def test_list_former_groups(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": []})
    await client.list_former_groups()
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/groups/former"


@pytest.mark.asyncio
async def test_get_group(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {"id": "123"}})
    result = await client.get_group("123")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/groups/123"
    assert result["response"]["id"] == "123"


@pytest.mark.asyncio
async def test_create_group(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {"id": "456", "name": "My Group"}})
    await client.create_group(name="My Group", description="desc", share=True)
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/groups"
    import json

    body = json.loads(request.content)
    assert body["group"]["name"] == "My Group"
    assert body["group"]["description"] == "desc"
    assert body["group"]["share"] is True


@pytest.mark.asyncio
async def test_update_group(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {}})
    await client.update_group("123", name="New Name")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/groups/123/update"
    import json

    body = json.loads(request.content)
    assert body["name"] == "New Name"


@pytest.mark.asyncio
async def test_destroy_group(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {}})
    await client.destroy_group("123")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/groups/123/destroy"
    assert request.method == "POST"


@pytest.mark.asyncio
async def test_join_group(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {}})
    await client.join_group("123", "abc-share-token")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/groups/123/join/abc-share-token"


@pytest.mark.asyncio
async def test_rejoin_group(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {}})
    await client.rejoin_group("123")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/groups/123/rejoin"


# ── Members ───────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_add_members(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {"results_id": "abc"}})
    members = [{"nickname": "Alice", "user_id": "999"}]
    result = await client.add_members("123", members)
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/groups/123/members/add"
    import json

    body = json.loads(request.content)
    assert body["members"] == members
    assert result["response"]["results_id"] == "abc"


@pytest.mark.asyncio
async def test_get_member_results(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {"members": []}})
    await client.get_member_results("123", "result-guid")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/groups/123/members/results/result-guid"


@pytest.mark.asyncio
async def test_remove_member(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {}})
    await client.remove_member("123", "membership-456")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/groups/123/members/membership-456/remove"


@pytest.mark.asyncio
async def test_update_membership(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {}})
    await client.update_membership("123", "NewNick")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/groups/123/memberships/update"
    import json

    body = json.loads(request.content)
    assert body["membership"]["nickname"] == "NewNick"


# ── Messages ──────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_messages(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {"messages": []}})
    await client.list_messages("123", before_id="msg1", limit=50)
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/groups/123/messages"
    assert request.url.params["before_id"] == "msg1"
    assert request.url.params["limit"] == "50"


@pytest.mark.asyncio
async def test_list_messages_no_optional_params(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {"messages": []}})
    await client.list_messages("123")
    request = httpx_mock.get_requests()[0]
    assert "before_id" not in request.url.params
    assert "since_id" not in request.url.params
    assert "after_id" not in request.url.params


@pytest.mark.asyncio
async def test_send_message(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=201, json={"response": {"message": {}}})
    await client.send_message("123", "Hello!", "guid-1")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/groups/123/messages"
    assert request.method == "POST"
    import json

    body = json.loads(request.content)
    assert body["message"]["text"] == "Hello!"
    assert body["message"]["source_guid"] == "guid-1"


# ── Direct Messages ───────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_direct_messages(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {"direct_messages": []}})
    await client.list_direct_messages("user-999", since_id="msg2")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/direct_messages"
    assert request.url.params["other_user_id"] == "user-999"
    assert request.url.params["since_id"] == "msg2"


@pytest.mark.asyncio
async def test_send_direct_message(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=201, json={"response": {"direct_message": {}}})
    await client.send_direct_message("user-999", "Hey!", "guid-2")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/direct_messages"
    import json

    body = json.loads(request.content)
    assert body["direct_message"]["recipient_id"] == "user-999"
    assert body["direct_message"]["text"] == "Hey!"


# ── Chats ─────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_chats(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": []})
    await client.list_chats(page=2, per_page=10)
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/chats"
    assert request.url.params["page"] == "2"
    assert request.url.params["per_page"] == "10"


# ── Likes ─────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_like_message(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {}})
    await client.like_message("conv-1", "msg-1")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/messages/conv-1/msg-1/like"
    assert request.method == "POST"


@pytest.mark.asyncio
async def test_unlike_message(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {}})
    await client.unlike_message("conv-1", "msg-1")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/messages/conv-1/msg-1/unlike"


# ── Bots ──────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_create_bot(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=201, json={"response": {"bot": {"bot_id": "bot-1"}}})
    result = await client.create_bot(
        "MyBot", "group-1", avatar_url="http://img", callback_url="http://cb"
    )
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/bots"
    import json

    body = json.loads(request.content)
    assert body["bot"]["name"] == "MyBot"
    assert body["bot"]["group_id"] == "group-1"
    assert body["bot"]["avatar_url"] == "http://img"
    assert body["bot"]["callback_url"] == "http://cb"
    assert result["response"]["bot"]["bot_id"] == "bot-1"


@pytest.mark.asyncio
async def test_post_as_bot(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=201, json={"response": {}})
    await client.post_as_bot("bot-1", "Hello from bot!", picture_url="http://pic")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/bots/post"
    import json

    body = json.loads(request.content)
    assert body["bot_id"] == "bot-1"
    assert body["text"] == "Hello from bot!"
    assert body["picture_url"] == "http://pic"


@pytest.mark.asyncio
async def test_list_bots(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": []})
    await client.list_bots()
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/bots"
    assert request.method == "GET"


@pytest.mark.asyncio
async def test_destroy_bot(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {}})
    await client.destroy_bot("bot-1")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/bots/destroy"
    import json

    body = json.loads(request.content)
    assert body["bot_id"] == "bot-1"


# ── Users ─────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_me(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {"id": "me-1", "name": "Kaleb"}})
    result = await client.get_me()
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/users/me"
    assert request.url.params["token"] == TOKEN
    assert result["response"]["name"] == "Kaleb"


@pytest.mark.asyncio
async def test_update_user(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {}})
    await client.update_user(name="New Name", email="new@example.com")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/users/update"
    import json

    body = json.loads(request.content)
    assert body["name"] == "New Name"
    assert body["email"] == "new@example.com"
    assert "avatar_url" not in body  # blank fields should be omitted


# ── Blocks ────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_blocks(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {"blocks": []}})
    await client.list_blocks("user-1")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/blocks"
    assert request.url.params["user"] == "user-1"


@pytest.mark.asyncio
async def test_check_block(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {"between": False}})
    result = await client.check_block("user-1", "user-2")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/blocks/between"
    assert request.url.params["user"] == "user-1"
    assert request.url.params["otherUser"] == "user-2"
    assert result["response"]["between"] is False


@pytest.mark.asyncio
async def test_create_block(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(status_code=201, json={"response": {}})
    await client.create_block("user-1", "user-2")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/blocks"
    assert request.method == "POST"
    assert request.url.params["user"] == "user-1"
    assert request.url.params["otherUser"] == "user-2"


@pytest.mark.asyncio
async def test_delete_block(client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(json={"response": {}})
    await client.delete_block("user-1", "user-2")
    request = httpx_mock.get_requests()[0]
    assert request.url.path == "/v3/blocks"
    assert request.method == "DELETE"
    assert request.url.params["user"] == "user-1"
    assert request.url.params["otherUser"] == "user-2"
