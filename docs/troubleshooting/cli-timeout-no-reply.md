# Troubleshooting: CLI chat times out with "no reply in 120000ms"

## Symptom

```
$ pnpm run chat hi
timeout: no reply in 120000ms
```

Logs show the CLI client connected and disconnected cleanly, but no message was routed:
```
CLI client connected
CLI client disconnected
```

No `CLI Message routed` or delivered response appears in the logs.

## What's happening

NanoClaw routes messages via **wirings** — each wiring connects a messaging group
(a chat/channel) to an agent group (an agent). Without a wiring, messages arrive
at the messaging group but no agent is listening, so they're silently dropped and
the CLI client times out waiting for a reply.

The `cli/local` messaging group is created automatically during setup, but it is
**not wired to any agent group by default**. This means the CLI chat command will
always time out until you explicitly create a wiring.

### How to confirm

```bash
sqlite3 data/v2.db "
  SELECT mg.id, mg.channel_type, mg.platform_id, w.agent_group_id
  FROM messaging_groups mg
  LEFT JOIN messaging_group_agents w ON w.messaging_group_id = mg.id;
"
```

If the `cli` row has a NULL `agent_group_id`, the wiring is missing.

## Fix

Wire `cli/local` to the agent group you want to handle CLI messages. For the main
Nano agent:

```bash
ncl wirings create \
  --messaging-group-id <cli-messaging-group-id> \
  --agent-group-id <nano-agent-group-id> \
  --engage-mode pattern \
  --engage-pattern "." \
  --session-mode shared
```

Get the IDs:
```bash
ncl messaging-groups list   # find the cli/local group id
ncl groups list             # find the target agent group id
```

After the wiring is created, retry:
```bash
pnpm run chat hi
```

Logs should now show `CLI Message routed` and you'll get a reply.

## Why this isn't auto-wired

Wirings are an intentional design decision in NanoClaw — an agent only handles messages
from channels you explicitly wire to it. This prevents accidental cross-channel routing
and makes the security model explicit: each agent group has a defined set of inbound
channels. The CLI is just another channel; it needs the same opt-in wiring as Telegram,
WhatsApp, or any other messaging group.

## Related

- See `ncl wirings --help` for wiring options (engage modes: `pattern`, `mention`, `mention-sticky`)
- `session-mode shared` means one session per (agent, messaging group) — fine for CLI dev/testing
- If you want CLI messages to share session history with another channel, use `agent-shared`
