#!/usr/bin/env python3
"""Google One Storage Audit — Drive totals + Gmail large attachments."""

import json
import os
import subprocess
import sys
import urllib3

# Bootstrap requests
for _pkg in ["requests"]:
    try:
        __import__(_pkg)
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-q", _pkg],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

import requests

# OneCLI injects HTTPS_PROXY + a self-signed CA cert for mitm interception.
# SSL_CERT_FILE / REQUESTS_CA_BUNDLE point to that cert if set.
_ca = os.environ.get("REQUESTS_CA_BUNDLE") or os.environ.get("SSL_CERT_FILE")
_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy") or ""
PROXIES = {"https": _proxy, "http": _proxy} if _proxy else {}
SSL = _ca if _ca else False  # verify=False if no CA cert found — local dev only
if not SSL:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _get(url, params=None):
    r = requests.get(url, params=params, proxies=PROXIES, verify=SSL, timeout=30)
    if r.status_code in (401, 403):
        print(json.dumps({"error": r.status_code, "detail": r.json()}, indent=2))
        sys.exit(1)
    r.raise_for_status()
    return r.json()


def _gb(n):
    return f"{n / 1e9:.1f} GB"


def _mb(n):
    return f"{n / 1e6:.1f} MB"


# ── Section 1: Storage totals ────────────────────────────────────────────────
about = _get(
    "https://www.googleapis.com/drive/v3/about",
    params={"fields": "storageQuota,user"},
)
q = about["storageQuota"]
used = int(q.get("usage", 0))
limit = int(q.get("limit", 0))
used_drive = int(q.get("usageInDrive", 0))
used_trash = int(q.get("usageInDriveTrash", 0))
# Drive API has no separate Gmail/Photos fields; remainder is Photos + Gmail.
used_other = max(0, used - used_drive - used_trash)
pct = round(used / limit * 100) if limit else 0

storage = {
    "used_bytes": used,
    "limit_bytes": limit,
    "pct": pct,
    "used_display": _gb(used),
    "limit_display": _gb(limit),
    "used_drive_display": _mb(used_drive),
    "used_trash_display": _mb(used_trash),
    "used_photos_gmail_display": _gb(used_other),
}

# ── Section 2: Gmail large attachments ───────────────────────────────────────
msg_list = _get(
    "https://gmail.googleapis.com/gmail/v1/users/me/messages",
    params={"q": "has:attachment larger:5mb", "maxResults": 20},
)

gmail_messages = []
for item in msg_list.get("messages", []):
    msg = _get(
        f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{item['id']}",
        params={
            "format": "metadata",
            "metadataHeaders": ["Subject", "From", "Date"],
        },
    )
    hdrs = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
    gmail_messages.append(
        {
            "id": item["id"],
            "subject": hdrs.get("Subject", "(no subject)"),
            "from_": hdrs.get("From", ""),
            "date": hdrs.get("Date", "")[:25],
            "size_bytes": msg.get("sizeEstimate", 0),
            "size_display": _mb(msg.get("sizeEstimate", 0)),
        }
    )

gmail_messages.sort(key=lambda x: x["size_bytes"], reverse=True)

# ── Section 3: Drive large files ─────────────────────────────────────────────
files_resp = _get(
    "https://www.googleapis.com/drive/v3/files",
    params={
        "q": "'me' in owners",
        "orderBy": "quotaBytesUsed desc",
        "pageSize": 20,
        "fields": "files(name,size,mimeType,modifiedTime,webViewLink)",
    },
)
drive_files = []
for f in files_resp.get("files", []):
    size = int(f.get("size", 0))
    drive_files.append(
        {
            "name": f.get("name", ""),
            "size_bytes": size,
            "size_display": _mb(size),
            "mimeType": f.get("mimeType", ""),
            "modifiedTime": f.get("modifiedTime", "")[:10],
        }
    )

# ── Write full results + print summary ───────────────────────────────────────
results = {
    "storage": storage,
    "gmail_large_attachments": gmail_messages,
    "drive_large_files": drive_files,
}
out_dir = "/workspace/agent" if os.path.isdir("/workspace") else os.path.join(os.path.dirname(__file__), "audit_output")
os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir, "audit_results.json"), "w") as fh:
    json.dump(results, fh, indent=2)

summary = {
    "storage": {
        "used": storage["used_display"],
        "limit": storage["limit_display"],
        "pct": f"{pct}%",
        "drive": storage["used_drive_display"],
        "photos_and_gmail": storage["used_photos_gmail_display"],
    },
    "gmail_top_10": [
        {
            "subject": m["subject"][:60],
            "size": m["size_display"],
            "date": m["date"],
        }
        for m in gmail_messages[:10]
    ],
    "drive_top_10": [
        {"name": f["name"][:60], "size": f["size_display"]}
        for f in drive_files[:10]
    ],
}
print(json.dumps(summary, indent=2))
