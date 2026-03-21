import os
from typing import Any

import httpx

BASE_URL = "https://api.groupme.com/v3"


class GroupMeClient:
    def __init__(self) -> None:
        self.token = os.environ["GROUPME_TOKEN"]

    async def _get(self, path: str, **params: Any) -> dict:
        params["token"] = self.token
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{BASE_URL}{path}", params=params)
            r.raise_for_status()
            return r.json()

    async def _post(self, path: str, json: dict | None = None, **params: Any) -> dict:
        params["token"] = self.token
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{BASE_URL}{path}", params=params, json=json)
            r.raise_for_status()
            return r.json()

    async def _delete(self, path: str, **params: Any) -> dict:
        params["token"] = self.token
        async with httpx.AsyncClient() as client:
            r = await client.delete(f"{BASE_URL}{path}", params=params)
            r.raise_for_status()
            return r.json()

    # ── Groups ───────────────────────────────────────────────────────────────

    async def list_groups(self, page: int = 1, per_page: int = 10, omit: str = "") -> dict:
        params: dict = {"page": page, "per_page": per_page}
        if omit:
            params["omit"] = omit
        return await self._get("/groups", **params)

    async def list_former_groups(self) -> dict:
        return await self._get("/groups/former")

    async def get_group(self, group_id: str) -> dict:
        return await self._get(f"/groups/{group_id}")

    async def create_group(
        self,
        name: str,
        description: str = "",
        image_url: str = "",
        share: bool = False,
    ) -> dict:
        body: dict = {"name": name, "share": share}
        if description:
            body["description"] = description
        if image_url:
            body["image_url"] = image_url
        return await self._post("/groups", json={"group": body})

    async def update_group(
        self,
        group_id: str,
        name: str = "",
        description: str = "",
        image_url: str = "",
        share: bool | None = None,
        office_mode: bool | None = None,
    ) -> dict:
        body: dict = {}
        if name:
            body["name"] = name
        if description:
            body["description"] = description
        if image_url:
            body["image_url"] = image_url
        if share is not None:
            body["share"] = share
        if office_mode is not None:
            body["office_mode"] = office_mode
        return await self._post(f"/groups/{group_id}/update", json=body)

    async def destroy_group(self, group_id: str) -> dict:
        return await self._post(f"/groups/{group_id}/destroy")

    async def join_group(self, group_id: str, share_token: str) -> dict:
        return await self._post(f"/groups/{group_id}/join/{share_token}")

    async def rejoin_group(self, group_id: str) -> dict:
        return await self._post(f"/groups/{group_id}/rejoin", json={"group_id": group_id})

    # ── Members ──────────────────────────────────────────────────────────────

    async def add_members(self, group_id: str, members: list[dict]) -> dict:
        """members: list of {nickname, user_id?, phone_number?, email?, guid?}"""
        return await self._post(f"/groups/{group_id}/members/add", json={"members": members})

    async def get_member_results(self, group_id: str, results_id: str) -> dict:
        return await self._get(f"/groups/{group_id}/members/results/{results_id}")

    async def remove_member(self, group_id: str, membership_id: str) -> dict:
        return await self._post(f"/groups/{group_id}/members/{membership_id}/remove")

    async def update_membership(self, group_id: str, nickname: str) -> dict:
        return await self._post(
            f"/groups/{group_id}/memberships/update",
            json={"membership": {"nickname": nickname}},
        )

    # ── Messages ─────────────────────────────────────────────────────────────

    async def list_messages(
        self,
        group_id: str,
        before_id: str = "",
        since_id: str = "",
        after_id: str = "",
        limit: int = 20,
    ) -> dict:
        params: dict = {"limit": limit}
        if before_id:
            params["before_id"] = before_id
        if since_id:
            params["since_id"] = since_id
        if after_id:
            params["after_id"] = after_id
        return await self._get(f"/groups/{group_id}/messages", **params)

    async def send_message(
        self,
        group_id: str,
        text: str,
        source_guid: str,
        attachments: list[dict] | None = None,
    ) -> dict:
        msg: dict = {"source_guid": source_guid, "text": text}
        if attachments:
            msg["attachments"] = attachments
        return await self._post(f"/groups/{group_id}/messages", json={"message": msg})

    # ── Direct Messages ───────────────────────────────────────────────────────

    async def list_direct_messages(
        self,
        other_user_id: str,
        before_id: str = "",
        since_id: str = "",
    ) -> dict:
        params: dict = {"other_user_id": other_user_id}
        if before_id:
            params["before_id"] = before_id
        if since_id:
            params["since_id"] = since_id
        return await self._get("/direct_messages", **params)

    async def send_direct_message(
        self,
        recipient_id: str,
        text: str,
        source_guid: str,
        attachments: list[dict] | None = None,
    ) -> dict:
        msg: dict = {
            "source_guid": source_guid,
            "recipient_id": recipient_id,
            "text": text,
        }
        if attachments:
            msg["attachments"] = attachments
        return await self._post("/direct_messages", json={"direct_message": msg})

    # ── Chats ─────────────────────────────────────────────────────────────────

    async def list_chats(self, page: int = 1, per_page: int = 20) -> dict:
        return await self._get("/chats", page=page, per_page=per_page)

    # ── Likes ─────────────────────────────────────────────────────────────────

    async def like_message(self, conversation_id: str, message_id: str) -> dict:
        return await self._post(f"/messages/{conversation_id}/{message_id}/like")

    async def unlike_message(self, conversation_id: str, message_id: str) -> dict:
        return await self._post(f"/messages/{conversation_id}/{message_id}/unlike")

    # ── Bots ──────────────────────────────────────────────────────────────────

    async def create_bot(
        self,
        name: str,
        group_id: str,
        avatar_url: str = "",
        callback_url: str = "",
        dm_notification: bool = False,
    ) -> dict:
        bot: dict = {"name": name, "group_id": group_id, "dm_notification": dm_notification}
        if avatar_url:
            bot["avatar_url"] = avatar_url
        if callback_url:
            bot["callback_url"] = callback_url
        return await self._post("/bots", json={"bot": bot})

    async def post_as_bot(self, bot_id: str, text: str, picture_url: str = "") -> dict:
        body: dict = {"bot_id": bot_id, "text": text}
        if picture_url:
            body["picture_url"] = picture_url
        return await self._post("/bots/post", json=body)

    async def list_bots(self) -> dict:
        return await self._get("/bots")

    async def destroy_bot(self, bot_id: str) -> dict:
        return await self._post("/bots/destroy", json={"bot_id": bot_id})

    # ── Users ─────────────────────────────────────────────────────────────────

    async def get_me(self) -> dict:
        return await self._get("/users/me")

    async def update_user(
        self,
        avatar_url: str = "",
        name: str = "",
        email: str = "",
        zip_code: str = "",
    ) -> dict:
        body: dict = {}
        if avatar_url:
            body["avatar_url"] = avatar_url
        if name:
            body["name"] = name
        if email:
            body["email"] = email
        if zip_code:
            body["zip_code"] = zip_code
        return await self._post("/users/update", json=body)

    # ── Blocks ────────────────────────────────────────────────────────────────

    async def list_blocks(self, user_id: str) -> dict:
        return await self._get("/blocks", user=user_id)

    async def check_block(self, user_id: str, other_user_id: str) -> dict:
        return await self._get("/blocks/between", user=user_id, otherUser=other_user_id)

    async def create_block(self, user_id: str, other_user_id: str) -> dict:
        return await self._post("/blocks", user=user_id, otherUser=other_user_id)

    async def delete_block(self, user_id: str, other_user_id: str) -> dict:
        return await self._delete("/blocks", user=user_id, otherUser=other_user_id)
