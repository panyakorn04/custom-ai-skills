---
name: portfolio-2026
description: Use when working on the panyakorn.com portfolio frontend, backend API integration, VPS Docker deployment, GitHub Actions release workflow, or bilingual Thai/English portfolio content.
version: 1.0.0
author: Panyakorn Boonyong
license: MIT
metadata:
  hermes:
    tags: [portfolio, nextjs, vps, docker, deployment]
    related_skills: [github-operations, vps-docker-compose-deployment]
---

# Portfolio 2026

## Overview

This skill captures the operating rules for the panyakorn.com portfolio system.

The frontend is a Next.js app deployed to a VPS through GitHub Actions. It consumes a separate backend API and must not receive database credentials or backend-only secrets.

## When to Use

Use this skill when:
- Editing the portfolio frontend repo.
- Updating deployment workflows.
- Debugging frontend/API integration.
- Changing Docker Compose or Caddy behavior for panyakorn.com.
- Adding bilingual Thai/English portfolio content.

## Architecture

- Frontend repo: `panyakorn04/portfolio-2026`
- Public site: `https://panyakorn.com`
- Public API: `https://api.panyakorn.com`
- Browser API URL: `NEXT_PUBLIC_API_URL=https://api.panyakorn.com`
- Server-side frontend API URL inside Compose: `FRONTEND_API_BASE_URL=http://backend:8888`
- Backend owns Postgres, Redis, Supabase, private credentials, admin tokens, and webhook secrets.

## Working Rules

1. Do not add `DATABASE_URL` to the frontend container.
   - Done when the frontend environment contains only public/site/API values and no backend-only credentials.
2. Do not expose backend secrets through `NEXT_PUBLIC_*`.
   - Done when every `NEXT_PUBLIC_*` value is safe for browsers.
3. Keep Thai copy professional, natural, and not overly resume-like.
   - Done when Thai copy sounds like a real portfolio, not a literal translation.
4. Prefer targeted patches and real verification.
   - Done when lint/build/deploy checks are run or blockers are reported directly.

## Verification Commands

Run before committing frontend changes:

```bash
pnpm lint
NEXT_PUBLIC_SITE_URL=https://panyakorn.com \
NEXT_PUBLIC_API_URL=https://api.panyakorn.com \
FRONTEND_API_BASE_URL=http://backend:8888 \
pnpm build
```

After push, watch GitHub Actions:

```bash
gh run list --limit 5
gh run watch <run-id> --exit-status
```

Verify production:

```bash
curl -I https://panyakorn.com
curl -I https://api.panyakorn.com
```

## Common Pitfalls

1. Frontend container accidentally receives backend `.env` values.
2. GitHub Actions SSH upload can intermittently timeout; rerun once before changing code if the VPS is reachable.
3. `localhost` inside Docker containers points to the container itself, not the VPS host or another service.
4. Caddy routes must preserve API routing behavior and not strip paths unexpectedly.
5. Public article data may come through the backend API/Supabase path, not a local frontend database.

## Verification Checklist

- [ ] `pnpm lint` passes.
- [ ] `pnpm build` passes with production-like API env.
- [ ] GitHub Actions CI passes after push.
- [ ] Deploy workflow passes after push.
- [ ] `https://panyakorn.com` responds.
- [ ] `https://api.panyakorn.com` responds.
- [ ] Frontend env does not include database or backend-only secrets.
