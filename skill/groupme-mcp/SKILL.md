---
name: groupme-mcp
description: Manages GroupMe groups, messages, and direct messages using the GroupMe MCP server. Use when the user wants to send a message, check group chats, read messages, add or remove members, manage bots, block users, or do anything in GroupMe. Triggers on phrases like "message [group]", "dm [person]", "what's happening in [group]", "post to GroupMe", "add [person] to [group]", "check my GroupMe", "send to my group".
license: MIT
metadata:
  author: Kaleb Smith
  mcp-server: groupme-mcp
---

# GroupMe MCP

## Instructions

The GroupMe MCP server exposes tools for reading and writing GroupMe data. All tools require a valid `GROUPME_TOKEN` set in the environment. For a full list of available tools and their parameters, consult `references/tools.md`.

### Step 1: Resolve names to IDs

Users refer to groups and people by name, not ID. Always resolve names before acting.

**Finding a group:**
1. Call `list_groups` (default returns 10 groups; increase `per_page` up to 500 if needed).
2. Match the requested group name case-insensitively against each group's `name` field.
3. If multiple groups match, list them and ask the user which one.
4. Use the matched group's `id` for subsequent calls.

**Finding a DM recipient:**
1. Call `list_chats` to list recent direct message conversations.
2. Each chat includes `other_user.name` and `other_user.id` — match on name.
3. If the person has no recent chat, ask the user for their GroupMe user ID directly.

### Step 2: Common workflows

**Send a group message**
```
list_groups → match name → send_message(group_id, text)
```
Always omit `source_guid` — it's auto-generated server-side to prevent duplicate sends.

**Read recent messages**
```
list_groups → match name → list_messages(group_id, limit=20)
```
To paginate backward, take the oldest message's `id` and pass it as `before_id` in the next call.

**Send a direct message**
```
list_chats → match name → send_direct_message(recipient_id, text)
```

**Add a member to a group**
```
add_members(group_id, members) → returns results_id
get_member_results(group_id, results_id) → poll until members array is present
```
`add_members` is asynchronous. The response contains a `results_id` GUID — call `get_member_results` to poll for completion. Retry after a short delay if the results are not yet available.

**Post as a bot**
```
list_bots → match name → post_as_bot(bot_id, text)
```
`post_as_bot` posts under the bot's name, not the user's. Bots cannot read messages.

**Like or unlike a message**
```
list_messages → find message_id → like_message(conversation_id, message_id)
```
`conversation_id` is the group ID for group messages.

### Step 3: Confirmation before writes

Before sending any message, adding/removing members, or deleting groups/bots, confirm the target with the user if there is any ambiguity (e.g. multiple groups with similar names, or an action that cannot be undone like `destroy_group`).

## Common Issues

### MCP connection error
**Cause:** MCP server not running or `GROUPME_TOKEN` not set.
**Solution:** Verify the server is connected in Settings > Extensions. Confirm the token is set in the server's environment config.

### Group not found after list_groups
**Cause:** Group may be on a later page, or the user left the group.
**Solution:** Increase `per_page` (up to 500) or call `list_former_groups` to check groups the user has left.

### add_members returns no results yet
**Cause:** GroupMe processes member additions asynchronously.
**Solution:** Wait briefly and retry `get_member_results`. The response will include a `members` array once complete.

### Duplicate message sent
**Cause:** Should not happen — `source_guid` is auto-generated. If it does occur, check that `source_guid` was not manually passed with a repeated value.
