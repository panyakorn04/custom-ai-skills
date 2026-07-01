---
name: youtube-highlight-automation
description: Use when working on the YouTube Highlight to TikTok or multiplatform automation, including discovery, analysis, Google Sheet rows, n8n orchestration, worker endpoints, and Upload-Post publishing.
version: 1.0.0
author: Panyakorn Boonyong
license: MIT
metadata:
  hermes:
    tags: [youtube, tiktok, n8n, automation, upload-post]
    related_skills: [vps-ai-services]
---

# YouTube Highlight Automation

## Overview

This skill captures the workflow rules for the YouTube Highlight automation that discovers podcast clips, analyzes transcript/metadata, writes rows to Google Sheets, cuts vertical highlight videos, and posts through Upload-Post.

Use only content the user has rights to use. The workflow may automate execution, but rights and platform policy checks remain required.

## When to Use

Use this skill when:
- Updating the n8n YouTube Highlight workflow.
- Changing discovery prompts, hashtags, or topic selection.
- Writing Google Sheet rows for highlight jobs.
- Debugging VPS worker endpoints.
- Posting through Upload-Post to TikTok or other platforms.

## Core Flow

1. Discover candidate YouTube videos.
   - Done when selected videos match the allowed content categories and avoid excluded sources.
2. Analyze transcript and metadata.
   - Done when each candidate has `topic`, `start_time`, `duration`, title, caption, and hashtags.
3. Append Google Sheet rows.
   - Done when rows include `status=pending` for auto mode and enough fields for the cutter/poster workflow.
4. Cut vertical highlight video on the VPS worker.
   - Done when the worker returns a usable vertical video while preserving source audio where appropriate.
5. Publish via Upload-Post.
   - Done when Upload-Post returns a verifiable publish/upload result.

## Discovery Rules

Include both:
- Self-improvement podcasts and personal development content.
- Finance, personal finance, investing, and planning content.

Useful Thai hashtags and terms:
- `#พัฒนาตัวเอง`
- `#พอดแคสต์`
- `#podcast`
- `#การเงิน`
- `#ลงทุน`
- `#วางแผนการเงิน`

Excluded source:
- POSCASH should remain excluded unless the user explicitly changes this rule.

## Worker Endpoints

Expected VPS worker endpoints:

```text
/youtube-search
/youtube-analyze
/youtube-highlight
```

YouTube cookies may be needed at:

```text
/opt/n8n-ffmpeg-worker/youtube-cookies.txt
```

If video download suddenly fails, check whether the cookies file needs refreshing before rewriting the worker.

## Google Sheet Rows

For auto mode, append AI-selected rows with:

```text
status=pending
```

Do not use `pending_review` for the current auto-posting flow unless the user switches back to manual review.

Each row should carry enough data for the downstream workflow:
- source video URL or ID
- title/topic
- start time
- duration, <= 60 seconds
- caption
- hashtags
- platform target
- status
- rights/use note if applicable

## Upload-Post Rules

Known Upload-Post profile details:
- user field: `panyakorn`
- TikTok account: `KwanJai` / `@KwanJai`

Do not store or print API keys. Verify upload/posting with returned IDs, URLs, or API status where available.

## Common Pitfalls

1. Assuming a YouTube video is safe to reuse just because it is public.
2. Writing `pending_review` when the active workflow expects `pending`.
3. Letting highlight duration exceed 60 seconds.
4. Using AI-generated Thai audio when source audio should be preserved.
5. Treating missing downloads as a code bug before checking cookies.
6. Posting without a verifiable Upload-Post response.

## Verification Checklist

- [ ] Candidate sources match allowed categories and exclusions.
- [ ] Every highlight duration is <= 60 seconds.
- [ ] Sheet rows use `status=pending` for auto mode.
- [ ] Worker endpoint response is captured and checked.
- [ ] Output video exists and preserves intended audio.
- [ ] Upload-Post response includes a verifiable result.
- [ ] Report includes rights/use caution when relevant.
