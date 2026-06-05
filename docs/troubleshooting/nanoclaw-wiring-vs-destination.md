# Troubleshooting: Replies going to wrong channel (wiring vs destination)

## Symptom

Messages sent via CLI (or any channel) are routed to the agent correctly, but the
agent's replies appear in a different channel — e.g. you message via CLI and the reply
shows up in Telegram instead.

## What's happening

NanoClaw has two separate routing concepts that must both be configured:

| Concept | Direction | Controls |
|---------|-----------|----------|
| **Wiring** (`messaging_group_agents`) | Inbound → Agent | Which agent receives a channel's messages |
| **Destination** (`agent_destinations`) | Agent → Outbound | Where the agent is allowed to SEND replies |

A wiring routes messages IN. A destination routes replies OUT. They are independent.

When you add a new channel (e.g. CLI), creating the wiring gives the agent a new inbound
path but does NOT automatically give it a new outbound destination. The agent will
continue using whatever destinations it already had — typically the first channel that was
wired (Telegram in this setup).

## How to confirm

```bash
# Check wirings (inbound paths)
sqlite3 data/v2.db "SELECT mg.channel_type, mg.platform_id, w.agent_group_id
  FROM messaging_group_agents w
  JOIN messaging_groups mg ON mg.id = w.messaging_group_id;"

# Check destinations (outbound paths)
sqlite3 data/v2.db "SELECT local_name, target_type, target_id FROM agent_destinations
  WHERE agent_group_id = '<ag-id>';"

# Check what's in the session's destinations (what the running agent sees)
sqlite3 data/v2-sessions/<ag-id>/<sess-id>/inbound.db "SELECT * FROM destinations;"
```

## Fix

Add a destination for the new channel:

```bash
# Find the messaging group ID for the channel
sqlite3 data/v2.db "SELECT id, channel_type, platform_id FROM messaging_groups;"

# Add the destination
node_modules/.bin/tsx src/cli/client.ts destinations add \
  --agent-group-id <ag-id> \
  --local-name <name>       \   # e.g. cli-local
  --target-type channel     \
  --target-id <mg-id>
```

Then update `CLAUDE.local.md` to tell the agent which destination to use for each
inbound channel:

```markdown
## Channel routing
- Inbound `senderId: cli:local` → reply to destination `cli-local`
- Inbound from Telegram → reply to destination `telegram-mg-XXXXX`
```

After updating CLAUDE.local.md, kill the running container so it respawns with the new
instructions:

```bash
docker kill nanoclaw-v2-<group>-<timestamp>
```

## Rule of thumb

**Every channel needs both a wiring AND a destination.** When you add a new chat
integration (WhatsApp, Zulip, etc.), run `destinations add` alongside `wirings create`
or replies will silently go to the wrong channel.

## Why destinations exist

Destinations are an explicit security boundary — an agent can only send to channels it
has been authorized to reach. This prevents a compromised agent from exfiltrating data to
arbitrary channels. The tradeoff is that every new channel must be explicitly configured
on both ends.
