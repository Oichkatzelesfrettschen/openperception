# Development Server Guide

The dev server (`tools/devserver.py`) serves the repository over HTTP with optional
live-reload for rapid iteration on HTML/CSS examples.

---

## WHY

Browser examples (contrast checker, CVD simulator, Ishihara plates) require an HTTP
server because browsers block `file://` resource loads by default (CORS restrictions).

---

## Start the Server

```bash
# Default: port 8000, serves repository root
python3 tools/devserver.py

# Custom port and directory
python3 tools/devserver.py --port 9000 --dir examples/

# Or via Makefile (uses port 8000)
make serve
```

Open `http://localhost:8000/` in your browser.

---

## Live Reload

Add the live-reload script tag to any HTML file you want to auto-refresh on save:

```html
<script src="/__livereload.js"></script>
```

The server watches these file types for changes:
`*.html`, `*.css`, `*.js`, `*.json`, `*.md`, `*.py`, `*.tex`, `*.sty`

Ignored directories: `.git`, `__pycache__`, `node_modules`, `build`

---

## Useful URLs

| URL | Content |
|-----|---------|
| `http://localhost:8000/examples/simulator/` | SVG CVD simulator |
| `http://localhost:8000/examples/contrast/` | WCAG contrast checker |
| `http://localhost:8000/datasets/ishihara-plate-learning/` | Ishihara learning tool |

---

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | 8000 | TCP port to listen on |
| `--dir` | `.` | Directory to serve (repository root) |

---

## Troubleshooting

**Port already in use**
```bash
# Kill whatever is on port 8000
fuser -k 8000/tcp
make serve
```

**Live reload not working**
- Confirm `<script src="/__livereload.js"></script>` is in the HTML `<head>`.
- Check browser console for WebSocket connection errors.

**File not found (404)**
- The server serves relative to `--dir`. Verify the path from that root.
