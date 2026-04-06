# GroupMe MCP — Tool Reference

## Groups

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `list_groups` | List the authenticated user's active groups | `page=1`, `per_page=10` (max 500), `omit=""` |
| `list_former_groups` | List groups the user has previously left | — |
| `get_group` | Get details for a specific group | `group_id` |
| `create_group` | Create a new group | `name` (required), `description`, `image_url`, `share` |
| `update_group` | Update a group's settings | `group_id` (required), `name`, `description`, `image_url`, `share`, `office_mode` |
| `destroy_group` | Permanently delete a group (creator only) | `group_id` |
| `join_group` | Join a group via share token | `group_id`, `share_token` |
| `rejoin_group` | Rejoin a group you previously left | `group_id` |

## Members

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `add_members` | Add members to a group (async — poll with `get_member_results`) | `group_id`, `members` (list of `{nickname, user_id\|phone_number\|email}`) |
| `get_member_results` | Poll the result of an `add_members` request | `group_id`, `results_id` |
| `remove_member` | Remove a member from a group | `group_id`, `membership_id` |
| `update_membership` | Update your own nickname in a group | `group_id`, `nickname` |

## Messages

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `list_messages` | Retrieve messages from a group | `group_id`, `limit=20` (max 100), `before_id`, `since_id`, `after_id` |
| `send_message` | Send a message to a group | `group_id`, `text` (max 1000 chars), `attachments` (optional) |

`source_guid` is auto-generated if omitted — always omit it.

Pagination: pass the oldest returned message's `id` as `before_id` to load earlier messages.

## Direct Messages

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `list_direct_messages` | List DMs with another user | `other_user_id`, `before_id`, `since_id` |
| `send_direct_message` | Send a DM to a user | `recipient_id`, `text` (max 1000 chars), `attachments` (optional) |

## Chats

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `list_chats` | List DM conversations sorted by most recent | `page=1`, `per_page=20` |

Each chat includes `other_user.id` and `other_user.name` — use this to resolve DM recipient names to IDs.

## Likes

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `like_message` | Like a message | `conversation_id` (group ID), `message_id` |
| `unlike_message` | Unlike a message | `conversation_id` (group ID), `message_id` |

## Bots

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `create_bot` | Create a bot in a group | `name`, `group_id`, `avatar_url`, `callback_url`, `dm_notification` |
| `post_as_bot` | Post a message as a bot | `bot_id`, `text`, `picture_url` |
| `list_bots` | List all bots owned by the authenticated user | — |
| `destroy_bot` | Delete a bot | `bot_id` |

Bots post under their own name, not the user's. They cannot read messages.

## Users

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `get_me` | Get the authenticated user's profile | — |
| `update_user` | Update the authenticated user's profile | `avatar_url`, `name`, `email`, `zip_code` |

## Blocks

| Tool | Description | Key parameters |
|------|-------------|----------------|
| `list_blocks` | List all users blocked by a given user | `user_id` |
| `check_block` | Check if a block exists between two users | `user_id`, `other_user_id` |
| `create_block` | Block a user | `user_id`, `other_user_id` |
| `delete_block` | Unblock a user | `user_id`, `other_user_id` |
