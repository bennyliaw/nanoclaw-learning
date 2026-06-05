# Google Photos Library API — March 2025 Restriction

## What changed

In March 2025, Google restricted the Photos Library API for unverified apps:

- `mediaItems.list` — previously returned all photos in the user's library, now returns
  **only items created by the app itself**
- `mediaItems.search` — same restriction
- `albums.list` — same restriction

The `photoslibrary` and `photoslibrary.readonly` OAuth scopes are still grantable, but
even with these scopes, unverified apps get 403 back from all list/search endpoints.

## What the error looks like

```json
{
  "error": {
    "code": 403,
    "message": "Request had insufficient authentication scopes.",
    "status": "PERMISSION_DENIED"
  }
}
```

This message is misleading — the scopes ARE present in the token. Google returns this
error to direct developers to apply for higher-level app verification.

## How we confirmed this (not proxy/auth issue)

Working setup (OneCLI connected, token has `photoslibrary` scope):
- Drive API (`www.googleapis.com/drive/...`) → ✅ returns real data
- Photos albums endpoint (`photoslibrary.googleapis.com/v1/albums`) → ❌ 403
- Photos mediaItems endpoint → ❌ 403

The OneCLI gateway IS injecting the Photos token (we get a Google error, not an OneCLI
"app not connected" error). The token has the correct scope. The rejection is Google's.

## Alternatives for auditing Google Photos storage

| Approach | Feasibility | Notes |
|----------|-------------|-------|
| `mediaItems.list` (old approach) | ❌ Blocked | Restricted for unverified apps |
| Google Picker API | ⚠️ Interactive only | User must manually select photos in browser — not automatable |
| Google Takeout | ⚠️ Manual | Request a metadata export; usable but one-shot, slow |
| Drive API `files.list` | ✅ Works | Only finds photos shared to Drive (rare post-2021) |
| Gmail API | ✅ Works | Finds large attachments contributing to storage quota |
| Google Photos app "Manage storage" | ✅ Works | Built-in tool at photos.google.com/storage — shows duplicates, screenshots, blurry photos. Manual but effective. |

## Recommended path for personal Google One audit

1. **Drive API** — get storage quota totals (done; only 570MB in Drive anyway)
2. **Gmail API** — enumerate large attachment emails
3. **Google Photos app** — use built-in "Manage storage" + "Free up space" suggestions
   for the bulk of the cleanup
4. **Phase B/C** — when Google eventually allows Takeout-based or Picker-based automation,
   wire that into NanoClaw for approval-gated deletion

## App verification (not practical for personal use)

To regain full `mediaItems.list` access, an app must complete Google's OAuth verification
process (weeks, requires public-facing privacy policy, security assessment). Not practical
for a personal self-hosted agent.
