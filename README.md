# The Orchid

A phone-first garden-care site for our Auckland garden: fruit trees, roses, flowers, palms, foliage and succulents, with a weekly job list.

## Two versions

| | Where | What it does |
|---|---|---|
| **Main app** | Private claude.ai artifact | Add and remove plants, ticks shared across devices, new weekly list every Saturday 7:40am (Auckland) with a phone notification. |
| **Family view** | This repo, via GitHub Pages | Read-only snapshot of the plants and this week's list. Ticks are saved on each phone only. |

## Files

- `index.html`: the whole site in one file (no build step). Inside claude.ai it reads the artifact database. Anywhere else it loads `data.json` and switches to read-only mode.
- `data.json`: snapshot of the plants and the latest weekly list (`{ plants: [...], week: {...} }`).

## Updating the family view

Replace `data.json` with a fresh export of the `plants` collection and the latest `weeks` document from the claude.ai artifact, then commit.

## Data shape

- `plants/<id>`: name, short, latin, section (fruit, flowers, palms, foliage, succulents, herbs), art (drawing key), tint, deep, spot, sun, water, feed, care, season, seasonText, months (0 = Jan), about, watch, next, addedAt.
- `weeks/<YYYY-MM-DD>`: weekOf, generatedAt, weather, headline, tasks [{id, plantId, section, tag, text}], nextTitle, next [].
- `ticks/<week id>`: done {taskId: true}.

All plant drawings are original inline SVGs drawn for this site.
