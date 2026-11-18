"""Apply an 'Add plant' or 'Remove plant' issue form to data.json.

Reads the issue from GITHUB_EVENT_PATH, edits data.json in place and writes a
short human message to GITHUB_OUTPUT (key: message) and changed=true|false.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

CATS = {
    "fruit": ("fruit", "lemon", "#FBF3CF", "#7A5A0C"),
    "flowers": ("flowers", "flower", "#F9DDE8", "#A3336F"),
    "palms": ("palms", "palm", "#E3EDE0", "#3F6B4C"),
    "foliage": ("foliage", "bush", "#E1EEE6", "#2F6B44"),
    "succulents": ("succulents", "rosette", "#E9F0DD", "#4F7A36"),
    "herbs & veg": ("herbs", "veggie", "#EAF1DA", "#4A6B2A"),
}


def fields(body):
    out, key = {}, None
    for line in (body or "").splitlines():
        m = re.match(r"^###\s+(.*)$", line)
        if m:
            key = m.group(1).strip().lower()
            out[key] = ""
        elif key is not None:
            out[key] += line + "\n"
    return {k: ("" if v.strip() == "_No response_" else v.strip()) for k, v in out.items()}


def clean(text, limit):
    text = re.sub(r"[\x00-\x1f<>`]", "", text or "").strip()
    return text[:limit]


def slug(name, taken):
    base = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:40] or "plant"
    s, i = base, 2
    while s in taken:
        s, i = f"{base}-{i}", i + 1
    return s


def output(message, changed):
    with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
        f.write(f"message={message}\nchanged={'true' if changed else 'false'}\n")
    print(message)


def main():
    event = json.load(open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8"))
    issue = event["issue"]
    title = (issue.get("title") or "").lower()
    f = fields(issue.get("body"))
    data = json.load(open("data.json", encoding="utf-8"))
    plants = data.setdefault("plants", [])

    if title.startswith("add plant"):
        name = clean(f.get("plant name", ""), 40)
        cat = CATS.get(clean(f.get("category", ""), 20).lower())
        if not name or not cat:
            return output("Couldn't add it: the form needs a plant name and a category.", False)
        key, art, tint, deep = cat
        pid = slug(name, {p.get("id") for p in plants})
        plants.append({
            "id": pid, "name": name, "section": key, "art": art, "tint": tint, "deep": deep,
            "spot": clean(f.get("where is it?", ""), 50),
            "addedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        })
        msg = f"Added {name} to {clean(f.get('category', ''), 20)}. It shows on the site in a minute or two; care details arrive on Saturday."
    elif title.startswith("remove plant"):
        want = clean(f.get("plant name", ""), 40).lower()
        match = [p for p in plants if p.get("name", "").lower() == want or p.get("id") == want]
        if not match:
            return output(f"Couldn't find a plant called '{want}'. Check the spelling on the site and try again.", False)
        data["plants"] = [p for p in plants if p not in match]
        msg = f"Removed {match[0]['name']} from the site."
    else:
        return output("Not a garden form; nothing changed.", False)

    with open("data.json", "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    output(msg, True)


if __name__ == "__main__":
    sys.exit(main())
