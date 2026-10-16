# Repository Guidelines

## Project Structure & Module Organization

This is a small React/Vite storefront. `src/` contains the editable React source (`App.jsx`, `main.jsx`, and `styles.css`); `public/` contains runtime assets such as `logo.png` and `hero.png`; `dist/` is the static deployment output. Root-level PNGs are design references and source assets. `.openai/hosting.json` contains the Sites project configuration.

## Build, Test, and Development Commands

Install dependencies with `npm install`, start the Vite development server with `npm run dev`, create a production build with `npm run build`, and preview the built app with `npm run preview`. The static `dist/` output can also be opened directly for a quick check. A macOS image metadata check is:

```sh
sips -g pixelWidth -g pixelHeight "Sin título.png"
```

## Coding Style & Naming Conventions

Use JSX with two-space indentation, semicolons, descriptive `camelCase` variables/functions, and `PascalCase` React components. Keep customer-facing copy in Spanish and preserve the existing WhatsApp-only checkout scope. Use lowercase kebab-case for new directories/assets unless an external filename must be preserved. No formatter or linter is configured yet.

## Testing Guidelines

No testing framework or coverage threshold is configured. Before submitting UI changes, run `npm run build`, inspect the responsive layout, add a product to the cart, change quantity, remove it, and verify that the WhatsApp link contains the expected order text. Add tests under `tests/` when a framework is introduced.

## Commit & Pull Request Guidelines

Git history is not available in this directory, so no repository-specific commit convention can be inferred. Use concise imperative commit subjects, for example `Add homepage artwork`, and keep unrelated changes separate. Pull requests should explain the change, identify affected files, include validation steps, and attach before/after screenshots for visual or asset changes.

## Asset Handling

Preserve the existing PNG unless the task explicitly requests replacement. Check dimensions, transparency, and visual appearance after edits; avoid committing temporary exports, caches, or editor metadata.
