# Custom AI Skills

Repo-managed custom skills, Open WebUI/Ollama model assets, and VPS deployment workflow for Panyakorn's AI automation stack.

## Structure

```text
ai/
├── modelfiles/
│   └── panyakorn-local-qwen.Modelfile
└── skills/
    ├── portfolio-2026/
    │   └── SKILL.md
    ├── vps-ai-services/
    │   └── SKILL.md
    └── youtube-highlight-automation/
        └── SKILL.md
.github/workflows/
└── deploy-ai-assets.yml
```

## Intended deployment

GitHub Actions syncs `ai/` to the VPS at `/opt/apps/ai`, then rebuilds the local Ollama custom model `panyakorn-local:latest` from the Modelfile.

Expected VPS compose mounts:

```yaml
ollama:
  volumes:
    - ollama-data:/root/.ollama
    - ./ai:/opt/ai:ro
```

Open WebUI should connect to Ollama internally with:

```text
OLLAMA_BASE_URL=http://ollama:11434
```

Do not expose Ollama publicly. Expose only Open WebUI through HTTPS and login, for example `https://ai.panyakorn.com`.

## Secrets

Do not commit API keys, database URLs, VPS passwords, or private tokens. Use GitHub repository secrets and `/opt/apps/.env` on the VPS.

Required GitHub Actions secrets for deployment:

- `VPS_HOST`
- `VPS_USER`
- `VPS_SSH_KEY`
