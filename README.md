# Custom AI Skills

Repo-managed custom skills, Open WebUI/Ollama model assets, and VPS deployment workflow for Panyakorn's AI automation stack.

## Structure

```text
ai/
├── modelfiles/
│   └── panyakorn-local-qwen.Modelfile
└── skills/
    ├── ai-console/
    │   ├── portfolio-2026/
    │   │   └── SKILL.md
    │   ├── vps-ai-services/
    │   │   └── SKILL.md
    │   └── youtube-highlight-automation/
    │       └── SKILL.md
    └── portfolio-site/
        ├── panyakorn-profile/
        │   └── SKILL.md
        └── portfolio-services/
            └── SKILL.md
.github/workflows/
└── deploy-ai-assets.yml
```

## Skill profiles

The backend loads different skill profile folders depending on the public surface:

- `ai-console`: used by `ai.panyakorn.com` through `/api/ai/chat` and `/api/ai/chat/stream`. This profile can include internal engineering, VPS, automation, and repo-operation skills.
- `portfolio-site`: used by `panyakorn.com` through `/api/portfolio/assistant/chat` and `/api/portfolio/assistant/chat/stream`. This profile must remain public-safe and focused on portfolio visitor questions.

Keep private deployment details, credentials, admin endpoints, and automation internals out of `portfolio-site` skills.

## Intended deployment

GitHub Actions syncs `ai/` to the VPS at `/opt/apps/ai`, then rebuilds the local Ollama custom model `panyakorn-local:latest` from the Modelfile. The Go backend reads skill profiles from `/opt/apps/ai/skills` mounted/readable inside the backend container as `/opt/ai/skills` or configured with `AISkillsDir`.

Expected VPS compose mounts:

```yaml
ollama:
  volumes:
    - ollama-data:/root/.ollama
    - ./ai:/opt/ai:ro

backend:
  volumes:
    - ./ai:/opt/ai:ro
  environment:
    AI_SKILLS_DIR: /opt/ai/skills
```

Open WebUI should connect to Ollama internally with:

```text
OLLAMA_BASE_URL=http://ollama:11434
```

Do not expose Ollama publicly. Expose only the frontend/backend routes that enforce rate limits and skill-profile boundaries.

## Secrets

Do not commit API keys, database URLs, VPS passwords, or private tokens. Use GitHub repository secrets and `/opt/apps/.env` on the VPS.

Required GitHub Actions secrets for deployment:

- `VPS_HOST`
- `VPS_USER`
- `VPS_SSH_KEY`
