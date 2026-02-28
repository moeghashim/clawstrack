# Claws Track

Open-source AI assistant project comparison matrix. Side-by-side feature, license, and popularity data for the "claw" ecosystem — OpenClaw, NanoClaw, nanobot, PicoClaw, Pi, IronClaw, and ZeroClaw.

## Projects Compared

| Project | Repo | Language |
|---------|------|----------|
| OpenClaw | [openclaw/openclaw](https://github.com/openclaw/openclaw) | TypeScript |
| nanobot | [HKUDS/nanobot](https://github.com/HKUDS/nanobot) | Python |
| PicoClaw | [sipeed/picoclaw](https://github.com/sipeed/picoclaw) | Go |
| ZeroClaw | [zeroclaw-labs/zeroclaw](https://github.com/zeroclaw-labs/zeroclaw) | Rust |
| Pi | [badlogic/pi-mono](https://github.com/badlogic/pi-mono) | TypeScript |
| NanoClaw | [qwibitai/nanoclaw](https://github.com/qwibitai/nanoclaw) | TypeScript |
| IronClaw | [nearai/ironclaw](https://github.com/nearai/ironclaw) | Rust |

## Features Tracked

- **Multi-Channel Messaging** — WhatsApp, Telegram, Slack, Discord, etc.
- **Sandbox Isolation** — Container or WASM-based agent isolation
- **Persistent Memory** — Conversation and context storage
- **Scheduled Tasks** — Cron-style or recurring jobs
- **MCP Support** — Model Context Protocol
- **Web Search** — Built-in web search capability
- **Web UI** — Browser-based interface
- **Agent Swarms** — Multi-agent collaboration

GitHub star counts are fetched live client-side.

## Tech Stack

- [Astro](https://astro.build) v5 — static-first
- [Tailwind CSS](https://tailwindcss.com) v4
- TypeScript (strict mode)
- Content Collections (JSON data)

## Commands

| Command | Action |
|---------|--------|
| `npm install` | Install dependencies |
| `npm run dev` | Start dev server at `localhost:4321` |
| `npm run build` | Production build to `./dist/` |
| `npm run preview` | Preview production build locally |

## Adding a Project

1. Create `src/content/projects/<name>.json` matching the schema in `src/content/config.ts`
2. The table auto-expands — no template changes needed

## License

MIT
