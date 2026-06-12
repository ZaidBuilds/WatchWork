# Product Spec

## Problem

Saved educational content becomes a backlog instead of execution. Action Engine converts captured videos into task plans and creates friction against endless consumption.

## MVP Promise

No copy-paste links. Capture from the browser, generate a plan, and track execution.

## User Journey

1. User opens a YouTube learning video.
2. User clicks the extension button or injected page button.
3. Dashboard receives the capture.
4. User generates the action plan.
5. User checks off tasks.
6. Gatekeeper mode blocks new capture until enough execution is done.

## Level Up Concepts

- Browser extension architecture: MV3 permissions, popup scripts, content scripts.
- Structured AI output: JSON schema validation before storage.
- Background jobs: move processing into queues for reliability.
- Agent design: add critic review before tasks are persisted.
