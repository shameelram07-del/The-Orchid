# The Orchid

A phone-first garden-care site for our Auckland garden: fruit, flowers, palms, foliage, succulents, and herbs & veg. The front page ("Garden watch") shows critical items, current issues and risks; each plant has its own swipeable page with this week's jobs, care details and pet safety (3 cats, a Pomeranian, cockatiels).

**Live site:** https://shameelram07-del.github.io/The-Orchid/

## This repo is the source of truth

| File | What it is |
|---|---|
| `index.html` | The whole site, one file, no build step. |
| `data.json` | All plants and the current week: `{ plants: [...], week: {...} }`. |
| `history/` | Past weeks, one file per week (`YYYY-MM-DD.json`). |

### How it updates

- **Add / remove a plant:** only through the owner's Claude chat, which edits `data.json` and pushes. The site itself has no add or remove buttons.
- **Every Saturday 7:40am (Auckland):** a scheduled Claude session checks the forecast, fills in care details and pet safety for new plants, writes the new Garden watch and weekly jobs into `data.json`, archives last week into `history/`, and pushes. A phone notification summarises it.
- **Publishing:** GitHub Pages serves the `gh-pages` branch, which mirrors `main`. Every update pushes to both.

### Data shape

- `plants[]`: id, name, short, latin, section (fruit, flowers, palms, foliage, succulents, herbs), art (drawing key), tint, deep, spot, sun, water, feed, care, season, seasonText, months (0 = Jan), about, watch, next, pets {cat, dog, bird: safe | care | toxic}, petNote, addedAt.
- `week`: id, weekOf, generatedAt, weather, headline, alerts [{id, level: critical | issue | risk, plantId, art, title, text, action}], tasks [{id, plantId, section, tag, text}], nextTitle, next [].

Ticks and "Sorted" are saved on each phone (browser storage), not in the repo.

All plant drawings are original inline SVGs drawn for this site.
