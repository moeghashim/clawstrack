# Claws Track — Project Guide

## Overview

Claws Track is an open-source project comparison matrix built with Astro and Tailwind CSS v4. It displays side-by-side feature, security, and popularity data for OSS projects, with live GitHub star counts fetched client-side.

## Tech Stack

- **Framework:** Astro v5 (static-first, content-driven)
- **Styling:** Tailwind CSS v4 via `@tailwindcss/vite` plugin
- **Language:** TypeScript (strict mode via `astro/tsconfigs/strict`)
- **Content:** Astro Content Collections (JSON data files, Zod schemas)
- **Design:** Brutalist / utilitarian aesthetic (hard borders, monospace accents, black-and-white palette with `#FF3300` accent)

## Commands

- `npm run dev` — Start dev server (default: localhost:4321)
- `npm run build` — Production build to `dist/`
- `npm run preview` — Preview production build locally

## Folder Structure

```
clawstrack/
├── astro.config.mjs          # Astro + Tailwind vite plugin config
├── tsconfig.json              # Strict TypeScript config
├── package.json               # Dependencies and scripts
├── progress.txt               # Learnings log (append-only, see below)
├── CLAUDE.md                  # Project guide for Claude
├── public/                    # Static assets (favicons)
└── src/
    ├── components/            # Reusable .astro UI components
    │   ├── FeatureCell.astro  # Boolean feature indicator (● / ○)
    │   ├── SectionHeader.astro# Table section divider row
    │   └── StarsCell.astro    # Live GitHub stars cell with bar graph
    ├── content/
    │   ├── config.ts          # Zod schema for content collections
    │   └── projects/          # One JSON file per project being compared
    │       ├── astro.json
    │       └── nextjs.json
    ├── layouts/
    │   └── Layout.astro       # Base HTML layout (head, header, fonts)
    ├── pages/
    │   └── index.astro        # Main comparison table page
    ├── scripts/
    │   └── github-stars.ts    # Client-side GitHub API star fetcher
    └── styles/
        └── global.css         # Tailwind v4 @theme tokens
```

## Conventions

### Components

- One component per file in `src/components/`.
- Every component must define a typed `Props` interface in its frontmatter.
- Keep components focused — each renders a single table cell or row pattern.

### Content Collections

- Project data lives in `src/content/projects/` as individual JSON files.
- Schema is defined in `src/content/config.ts` using Zod.
- To add a new project: create a new `.json` file matching the schema — no code changes needed.
- Collection type is `data` (JSON/YAML), not `content` (Markdown).

### Styling

- Tailwind v4 with `@theme` block in `global.css` for design tokens.
- Custom tokens: `--color-accent`, `--color-surface`, `--shadow-brutal`, `--shadow-brutal-sm`.
- Fonts: Inter (sans), JetBrains Mono (mono) loaded via Google Fonts in Layout.
- No `tailwind.config.*` file — Tailwind v4 uses CSS-based configuration.
- Use Tailwind utility classes directly in templates. Avoid `@apply` unless extracting a repeated pattern.

### Pages

- Pages live in `src/pages/` following Astro file-based routing.
- Import and compose components rather than inlining large HTML blocks.
- Client-side scripts go in `src/scripts/` and are referenced via `<script src="...">`.

### TypeScript

- Strict mode enabled. All props must be typed.
- Use Astro's built-in types (`astro:content` for collections).

### Code Quality

- No redundant comments — only explain non-obvious intent or trade-offs.
- Prefer extracting reusable components over duplicating markup.
- Keep frontmatter (---) blocks lean: data fetching and imports only.

## Adding a New Compared Project

1. Create `src/content/projects/<name>.json` matching the schema in `config.ts`.
2. The table auto-expands — no template changes required.

## progress.txt — Learning Log

**Always append to `progress.txt`** at the project root after completing meaningful work. Each entry should include:
- Date
- What was done
- Key decisions or trade-offs made
- Anything learned or discovered about the codebase

This file is append-only. Never overwrite or reorganize existing entries. It serves as a running knowledge base across sessions.
