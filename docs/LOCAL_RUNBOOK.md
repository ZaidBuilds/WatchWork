# Local Runbook

## 1. Start API

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.main:app --reload --port 8000
```

Check `http://localhost:8000/api/health`.

## 2. Start Web

```powershell
cd apps/web
npm install
copy .env.example .env.local
npm run dev
```

Open `http://localhost:3000/dashboard`.

## 3. Load Extension

1. Go to `chrome://extensions`.
2. Turn on developer mode.
3. Load unpacked from `apps/extension`.
4. Open a YouTube video.
5. Click the extension popup or the `Action Engine` button injected near YouTube actions.

## 4. MVP Acceptance

- Captured video appears in dashboard.
- Processing generates a transcript preview or useful failure reason.
- Plan appears with summary, concepts, and tasks.
- Checking tasks updates completion.
- Gatekeeper mode blocks new captures when active plan progress is below threshold.
