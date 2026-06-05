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

This message is misleading — the scopes ARE correctly requested. Google returns this
specific error to signal that the *operation* requires a permission level only granted to
verified apps, even when the scope is present in the token.

## How we confirmed this — definitive proof

**Test:** OAuth 2.0 Playground with own client credentials (completely bypassing OneCLI
entirely). Fresh token obtained via Playground OAuth flow with `photoslibrary.readonly`
scope explicitly authorized. App in Testing mode, account owner as test user.

**Result:** Identical 403 `PERMISSION_DENIED / "insufficient authentication scopes"` on
`GET https://photoslibrary.googleapis.com/v1/mediaItems?pageSize=5`.

**What this rules out:**

| Hypothesis | Ruled out because |
|------------|-------------------|
| OneCLI injecting wrong/missing token | Playground used its own fresh token, no OneCLI involved |
| Token missing photoslibrary scope | Scope explicitly authorized in Playground OAuth flow |
| API not enabled in GCP | Console shows Photos Library API enabled; 7 requests logged, all 403 |
| Storage over-quota blocking reads | Over-quota only blocks writes; returns `storageQuotaExceeded`, not scope error |
| API rate limit | Fresh project, only 7 calls; rate limits return 429, not 403 |
| Testing mode exemption | App owner as test user still blocked — Testing mode does not exempt this scope |

**Conclusion:** Google blocks `mediaItems.list`, `mediaItems.search`, and `albums.list`
for unverified apps at the API level, regardless of OAuth scope or Testing mode status.
Restriction introduced March 2025.

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

## Official references

- [Updates to the Google Photos APIs](https://developers.google.com/photos/support/updates) — Google's official announcement of the March 31, 2025 scope deprecation
- [rclone issue #8567](https://github.com/rclone/rclone/issues/8567) — widely-used open-source tool hitting the exact same 403; confirms this affects all third-party apps

## App verification (not practical for personal use)

To regain full `mediaItems.list` access, an app must complete Google's OAuth verification
process (weeks, requires public-facing privacy policy, security assessment). Not practical
for a personal self-hosted agent.
