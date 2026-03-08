# Project Rules — Sharable

A shared workspace for brainstorming, architecture, solution design, knowledge exploration, and prototyping.

## Remote Repository

- Remote: `https://github.com/dsonerd/sharable.git`
- Credentials are stored in `.local/credentials.env` — source them to authenticate.
- When setting up remote, use: `git remote add origin https://<PAT>@github.com/dsonerd/sharable.git`

## Git Workflow

- **Always commit** after completing any task — do not leave work uncommitted.
- **Never push** unless the user explicitly asks to push.
- Write concise, meaningful commit messages describing *why*, not *what*.
- **Never mention Claude or AI** in commit messages — no `Co-Authored-By` tags, no AI references.
- Do not commit `.env`, `.local/`, or any file containing secrets.
- Do not force-push to `main`.

## Task Workflow

Before starting any task:
1. **Categorize** the task (brainstorming, architecture, solution, knowledge, prototype, etc.)
2. **Place output** in the appropriate folder based on category (see Project Structure)
3. Execute the task
4. Commit the result

## Project Structure

```
brainstorming/        # Ideas, mind maps, rough explorations
architecture/         # System design, diagrams, ADRs, component layouts
solutions/            # Solution designs, technical proposals, PoCs
knowledge/            # Research, references, learnings, how-tos
prototypes/           # Quick code experiments, spike solutions
assets/               # Shared images, diagrams, media files
.claude/              # Claude Code local settings
.local/               # Local credentials and secrets (gitignored)
```

## Conventions

- **Language**: Default to English for code, comments, and documentation.
- **Secrets**: Never commit credentials or secrets. Use `.local/credentials.env` for local secrets (gitignored via `.local/`).
- **File format**: Prefer Markdown (`.md`) for documents. Use subfolders within categories to group related items.
- **Naming**: Use kebab-case for folders and files (e.g., `payment-gateway-design.md`).

## Claude Code Guidelines

- Read files before editing them.
- Prefer editing existing files over creating new ones.
- Keep solutions simple — avoid over-engineering.
- Ask before taking destructive or irreversible actions.
