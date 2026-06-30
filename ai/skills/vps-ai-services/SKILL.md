---
name: vps-ai-services
description: Use when deploying or troubleshooting Ollama, Open WebUI, model Modelfiles, AI assets, and internal-only AI APIs on the VPS Docker Compose stack.
version: 1.0.0
author: Panyakorn Boonyong
license: MIT
metadata:
  hermes:
    tags: [vps, ollama, open-webui, docker, ai-services]
    related_skills: [vps-docker-compose-deployment]
---

# VPS AI Services

## Overview

This skill defines the deployment pattern for AI services on the VPS. Open WebUI is the public UI, Ollama is the internal model backend, and repo-managed AI assets are synced to `/opt/apps/ai`.

Default posture: expose Open WebUI only through HTTPS and login; keep Ollama private inside Docker Compose.

## When to Use

Use this skill when:
- Adding or changing the `ollama` service.
- Adding or changing the `open-webui` service.
- Deploying Modelfiles from this repo to the VPS.
- Rebuilding custom Ollama models such as `panyakorn-local:latest`.
- Connecting backend or n8n workflows to Ollama.

## Compose Pattern

Ollama should stay internal:

```yaml
ollama:
  image: ollama/ollama:latest
  container_name: ollama
  restart: unless-stopped
  volumes:
    - ollama-data:/root/.ollama
    - ./ai:/opt/ai:ro
  expose:
    - "11434"
```

Open WebUI can be exposed through Caddy:

```yaml
open-webui:
  image: ghcr.io/open-webui/open-webui:main
  container_name: open-webui
  restart: unless-stopped
  depends_on:
    - ollama
  environment:
    OLLAMA_BASE_URL: http://ollama:11434
    WEBUI_URL: https://ai.panyakorn.com
    WEBUI_SECRET_KEY: ${OPEN_WEBUI_SECRET_KEY}
    ENABLE_SIGNUP: "false"
    DEFAULT_MODELS: panyakorn-local:latest
  volumes:
    - open-webui-data:/app/backend/data
  expose:
    - "8080"
```

Volumes:

```yaml
volumes:
  ollama-data:
  open-webui-data:
```

## Caddy Pattern

```caddyfile
ai.panyakorn.com {
  reverse_proxy open-webui:8080
}
```

Do not add a public route for Ollama unless authentication, IP allowlisting, and rate limiting are explicitly designed.

## Model Build Pattern

After AI assets are synced to `/opt/apps/ai`, rebuild the custom model:

```bash
cd /opt/apps
docker compose up -d ollama open-webui
docker exec ollama ollama create panyakorn-local:latest \
  -f /opt/ai/modelfiles/panyakorn-local-qwen.Modelfile
docker exec ollama ollama list
```

Test Ollama internally:

```bash
docker exec ollama curl -s http://127.0.0.1:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "panyakorn-local:latest",
    "messages": [
      {"role": "user", "content": "ตอบเป็นภาษาไทยสั้น ๆ ว่าพร้อมใช้งานไหม"}
    ],
    "stream": false
  }'
```

## Security Rules

1. Do not expose `11434` with `ports`.
   - Done when `docker compose config` shows Ollama uses `expose`, not host-published ports.
2. Do not commit `OPEN_WEBUI_SECRET_KEY` or Ollama credentials.
   - Done when secrets live in GitHub Secrets or `/opt/apps/.env` only.
3. Do not disable Open WebUI auth on a public domain.
   - Done when `WEBUI_AUTH=False` is absent for public deployment.
4. Keep repo-managed AI assets read-only inside containers.
   - Done when the mount uses `./ai:/opt/ai:ro`.

## Common Pitfalls

1. `OLLAMA_BASE_URL=http://localhost:11434` inside Open WebUI is wrong in Docker Compose; use `http://ollama:11434`.
2. Open WebUI `ConfigVar` settings may persist in its database and override later environment changes.
3. Floating image tags are convenient but less reproducible; pin versions when the stack becomes production-critical.
4. Local models such as `qwen2.5:3b` avoid Ollama Cloud subscription requirements but have lower reasoning quality than cloud models.
5. Recreating the Ollama container is safe if `ollama-data` is preserved; deleting the volume removes models/auth/cache.

## Verification Checklist

- [ ] `docker compose config` passes.
- [ ] `docker compose ps ollama open-webui caddy` shows running services.
- [ ] `docker exec ollama ollama list` shows `panyakorn-local:latest`.
- [ ] Internal Ollama API test returns a model response.
- [ ] `curl -I https://ai.panyakorn.com` responds.
- [ ] Ollama is not reachable publicly.
- [ ] Open WebUI signup/auth settings are safe for public use.
