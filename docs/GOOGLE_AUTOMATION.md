# Google-First Automation Opportunities

## Sheets as Operating Dashboard

Create a Google Sheet with tabs:

- `Captures`: content id, title, source, status, created date.
- `Plans`: plan id, content title, completion percent.
- `Tasks`: task title, priority, estimated minutes, done status.
- `Weekly Review`: tasks completed, unfinished commitments, next focus.

Later, add a backend job that appends rows through the Google Sheets API after every successful plan generation and task completion.

## Docs as SOP

Create one Google Doc SOP:

1. Pick only educational/actionable content.
2. Capture with the extension.
3. Generate plan.
4. Complete at least 70 percent before adding more.
5. Review unfinished tasks every Sunday.

## Gmail Notifications

Send an email when:

- A plan is ready.
- A plan is under 70 percent after 3 days.
- Weekly digest is ready.

This can start as an n8n workflow triggered by a webhook from FastAPI.
