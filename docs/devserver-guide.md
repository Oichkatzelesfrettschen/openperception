# Dev Server with Live Reload

Run a simple HTTP server from repo root with optional live reload:

- Start: `python3 tools/devserver.py --port 8000 --dir .`
- Add to your HTML: `<script src="/__livereload.js"></script>`
- Open: `http://localhost:8000/examples/simulator/` (or any page)

Notes:
- Watches common file types (*.html, *.css, *.js, *.json, *.md, *.py, *.tex, *.sty)
- Ignores typical dev folders (.git, __pycache__, node_modules)
- No external dependencies required

