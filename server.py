import uuid

from mcp.server.fastmcp import FastMCP

from client import GroupMeClient

mcp = FastMCP("GroupMe")
client = GroupMeClient()


# ── Groups ────────────────────────────────────────────────────────────────────


@mcp.tool()
async def list_groups(page: int = 1, per_page: int = 10, omit: str = "") -> dict:
    """List the authenticated user's active groups.

    Args:
        page: Page number for pagination.
        per_page: Number of groups per page (max 500).
        omit: Comma-separated list of fields to omit (e.g. "memberships").
    """
    return await client.list_groups(page=page, per_page=per_page, omit=omit)


@mcp.tool()
async def list_former_groups() -> dict:
    """List groups the authenticated user has previously left."""
    return await client.list_former_groups()


@mcp.tool()
async def get_group(group_id: str) -> dict:
    """Get details for a specific group.

    Args:
        group_id: The ID of the group.
    """
    return await client.get_group(group_id)


@mcp.tool()
async def create_group(
    name: str,
    description: str = "",
    image_url: str = "",
    share: bool = False,
) -> dict:
    """Create a new group.

    Args:
        name: Name of the group.
        description: Optional description.
        image_url: Optional avatar image URL.
        share: Whether to enable a share URL for the group.
    """
    return await client.create_group(
        name=name, description=description, image_url=image_url, share=share
    )


@mcp.tool()
async def update_group(
    group_id: str,
    name: str = "",
    description: str = "",
    image_url: str = "",
    share: bool | None = None,
    office_mode: bool | None = None,
) -> dict:
    """Update a group's settings.

    Args:
        group_id: The ID of the group.
        name: New name (leave blank to keep current).
        description: New description (leave blank to keep current).
        image_url: New avatar image URL (leave blank to keep current).
        share: Enable or disable the share URL.
        office_mode: Enable or disable office mode.
    """
    return await client.update_group(
        group_id=group_id,
        name=name,
        description=description,
        image_url=image_url,
        share=share,
        office_mode=office_mode,
    )


@mcp.tool()
async def destroy_group(group_id: str) -> dict:
    """Permanently delete a group. Only the group creator can do this.

    Args:
        group_id: The ID of the group to delete.
    """
    return await client.destroy_group(group_id)


@mcp.tool()
async def join_group(group_id: str, share_token: str) -> dict:
    """Join a group using its share token.

    Args:
        group_id: The ID of the group.
        share_token: The share token from the group's share URL.
    """
    return await client.join_group(group_id, share_token)


@mcp.tool()
async def rejoin_group(group_id: str) -> dict:
    """Rejoin a group you previously left.

    Args:
        group_id: The ID of the group to rejoin.
    """
    return await client.rejoin_group(group_id)


# ── Members ───────────────────────────────────────────────────────────────────


@mcp.tool()
async def add_members(group_id: str, members: list[dict]) -> dict:
    """Add one or more members to a group. Async operation - poll with get_member_results.

    Args:
        group_id: The ID of the group.
        members: List of member objects. Each must have "nickname" and at least one of:
                 "user_id", "phone_number", "email". Optionally include "guid" for tracking.
    """
    return await client.add_members(group_id, members)


@mcp.tool()
async def get_member_results(group_id: str, results_id: str) -> dict:
    """Poll the result of an add_members request.

    Args:
        group_id: The ID of the group.
        results_id: The GUID returned from add_members.
    """
    return await client.get_member_results(group_id, results_id)


@mcp.tool()
async def remove_member(group_id: str, membership_id: str) -> dict:
    """Remove a member from a group.

    Args:
        group_id: The ID of the group.
        membership_id: The membership ID of the member to remove.
    """
    return await client.remove_member(group_id, membership_id)


@mcp.tool()
async def update_membership(group_id: str, nickname: str) -> dict:
    """Update your nickname in a group.

    Args:
        group_id: The ID of the group.
        nickname: Your new nickname (1-50 characters).
    """
    return await client.update_membership(group_id, nickname)


# ── Messages ──────────────────────────────────────────────────────────────────


@mcp.tool()
async def list_messages(
    group_id: str,
    before_id: str = "",
    since_id: str = "",
    after_id: str = "",
    limit: int = 20,
) -> dict:
    """Retrieve messages from a group.

    Args:
        group_id: The ID of the group.
        before_id: Return messages created before this message ID.
        since_id: Return messages created after this message ID (may skip messages).
        after_id: Return messages created immediately after this message ID.
        limit: Number of messages to return (max 100, default 20).
    """
    return await client.list_messages(
        group_id=group_id,
        before_id=before_id,
        since_id=since_id,
        after_id=after_id,
        limit=limit,
    )


@mcp.tool()
async def send_message(
    group_id: str,
    text: str,
    source_guid: str = "",
    attachments: list[dict] | None = None,
) -> dict:
    """Send a message to a group.

    Args:
        group_id: The ID of the group.
        text: Message text (max 1000 characters).
        source_guid: Unique ID to prevent duplicate sends. Auto-generated if blank.
        attachments: Optional list of attachment objects (image, location, emoji, etc.).
    """
    if not source_guid:
        source_guid = str(uuid.uuid4())
    return await client.send_message(
        group_id=group_id,
        text=text,
        source_guid=source_guid,
        attachments=attachments,
    )


# ── Direct Messages ───────────────────────────────────────────────────────────


@mcp.tool()
async def list_direct_messages(
    other_user_id: str,
    before_id: str = "",
    since_id: str = "",
) -> dict:
    """List direct messages with another user.

    Args:
        other_user_id: The ID of the other user in the conversation.
        before_id: Return messages created before this message ID.
        since_id: Return messages created after this message ID.
    """
    return await client.list_direct_messages(
        other_user_id=other_user_id,
        before_id=before_id,
        since_id=since_id,
    )


@mcp.tool()
async def send_direct_message(
    recipient_id: str,
    text: str,
    source_guid: str = "",
    attachments: list[dict] | None = None,
) -> dict:
    """Send a direct message to another user.

    Args:
        recipient_id: The user ID of the recipient.
        text: Message text (max 1000 characters).
        source_guid: Unique ID to prevent duplicate sends. Auto-generated if blank.
        attachments: Optional list of attachment objects.
    """
    if not source_guid:
        source_guid = str(uuid.uuid4())
    return await client.send_direct_message(
        recipient_id=recipient_id,
        text=text,
        source_guid=source_guid,
        attachments=attachments,
    )


# ── Chats ─────────────────────────────────────────────────────────────────────


@mcp.tool()
async def list_chats(page: int = 1, per_page: int = 20) -> dict:
    """List the authenticated user's direct message conversations, sorted by most recent.

    Args:
        page: Page number for pagination.
        per_page: Number of chats per page.
    """
    return await client.list_chats(page=page, per_page=per_page)


# ── Likes ─────────────────────────────────────────────────────────────────────


@mcp.tool()
async def like_message(conversation_id: str, message_id: str) -> dict:
    """Like a message.

    Args:
        conversation_id: The group ID or direct message conversation ID.
        message_id: The ID of the message to like.
    """
    return await client.like_message(conversation_id, message_id)


@mcp.tool()
async def unlike_message(conversation_id: str, message_id: str) -> dict:
    """Unlike a previously liked message.

    Args:
        conversation_id: The group ID or direct message conversation ID.
        message_id: The ID of the message to unlike.
    """
    return await client.unlike_message(conversation_id, message_id)


# ── Bots ──────────────────────────────────────────────────────────────────────


@mcp.tool()
async def create_bot(
    name: str,
    group_id: str,
    avatar_url: str = "",
    callback_url: str = "",
    dm_notification: bool = False,
) -> dict:
    """Create a new bot in a group.

    Args:
        name: The bot's display name.
        group_id: The ID of the group the bot belongs to.
        avatar_url: Optional avatar image URL for the bot.
        callback_url: Optional URL to receive message callbacks.
        dm_notification: Whether the bot should receive DM notifications.
    """
    return await client.create_bot(
        name=name,
        group_id=group_id,
        avatar_url=avatar_url,
        callback_url=callback_url,
        dm_notification=dm_notification,
    )


@mcp.tool()
async def post_as_bot(bot_id: str, text: str, picture_url: str = "") -> dict:
    """Post a message as a bot.

    Args:
        bot_id: The ID of the bot.
        text: Message text.
        picture_url: Optional image URL to attach.
    """
    return await client.post_as_bot(bot_id=bot_id, text=text, picture_url=picture_url)


@mcp.tool()
async def list_bots() -> dict:
    """List all bots created by the authenticated user."""
    return await client.list_bots()


@mcp.tool()
async def destroy_bot(bot_id: str) -> dict:
    """Delete a bot.

    Args:
        bot_id: The ID of the bot to delete.
    """
    return await client.destroy_bot(bot_id)


# ── Users ─────────────────────────────────────────────────────────────────────


@mcp.tool()
async def get_me() -> dict:
    """Get the authenticated user's profile information."""
    return await client.get_me()


@mcp.tool()
async def update_user(
    avatar_url: str = "",
    name: str = "",
    email: str = "",
    zip_code: str = "",
) -> dict:
    """Update the authenticated user's profile.

    Args:
        avatar_url: New avatar image URL.
        name: New display name.
        email: New email address.
        zip_code: New zip code.
    """
    return await client.update_user(
        avatar_url=avatar_url,
        name=name,
        email=email,
        zip_code=zip_code,
    )


# ── Blocks ────────────────────────────────────────────────────────────────────


@mcp.tool()
async def list_blocks(user_id: str) -> dict:
    """List all users blocked by a given user.

    Args:
        user_id: The ID of the user whose block list to retrieve.
    """
    return await client.list_blocks(user_id)


@mcp.tool()
async def check_block(user_id: str, other_user_id: str) -> dict:
    """Check if a block exists between two users.

    Args:
        user_id: The ID of the first user.
        other_user_id: The ID of the second user.
    """
    return await client.check_block(user_id, other_user_id)


@mcp.tool()
async def create_block(user_id: str, other_user_id: str) -> dict:
    """Block a user.

    Args:
        user_id: The ID of the user doing the blocking.
        other_user_id: The ID of the user to block.
    """
    return await client.create_block(user_id, other_user_id)


@mcp.tool()
async def delete_block(user_id: str, other_user_id: str) -> dict:
    """Unblock a user.

    Args:
        user_id: The ID of the user doing the unblocking.
        other_user_id: The ID of the user to unblock.
    """
    return await client.delete_block(user_id, other_user_id)
