# AI Website Generator

Describe a website in plain English, and this app generates a complete,
live, downloadable webpage for you using Google's Gemini API — with an
instant preview and the full source code.

Inspired by the idea behind AI website builders, but built independently:
a simple split-pane workbench — describe what you want on the left,
watch it get built on the right.

## Architecture
- `index.html` — the frontend: prompt input, live preview, code view.
- `api/generate.py` — a Vercel Python serverless function that calls the
  Gemini API server-side, so the API key never reaches the browser.
- `vercel.json` — tells Vercel how to run the Python function.

## Deploy on Vercel
1. Push this folder to a GitHub repository.
2. On vercel.com, import the repository as a new project.
3. In the project's **Settings → Environment Variables**, add:
   - `GEMINI_API_KEY` = your free key from https://aistudio.google.com/apikey
4. Deploy. Vercel will host `index.html` as the site and `api/generate.py`
   as a serverless endpoint at `/api/generate`.

## Run it locally
```bash
npm install -g vercel
vercel dev
```

## Tech stack
- HTML/CSS/JavaScript (frontend)
- Python (Vercel serverless function)
- Google Gemini API

Built by Tripti Sharma.
