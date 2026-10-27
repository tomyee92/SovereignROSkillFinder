#!/usr/bin/env python3
"""Rebuild data.json from the live SovereignRO Pokedex page.

Usage:  python scripts/update_data.py            (fetch the live page)
        python scripts/update_data.py page.html  (parse a saved copy)

The Pokedex page embeds its whole dataset as `var DATA = [...]`. Each entry has a
`moves` string like "Psychic (Psychic Wave Lv 5), Fire Blast (Meteor Storm Lv 4)":
the Pokemon move name, then the Ragnarok Online skill it maps to and its level.
"""
import json, re, sys, urllib.request, datetime, pathlib

URL = "https://sovereignro.com/?module=pokedex"
OUT = pathlib.Path(__file__).resolve().parent.parent / "data.json"
MOVE_RE = re.compile(r"\s*(.+?) \((.+?) Lv (\d+)\)\s*(?:,|$)")


def load_html(argv):
    if len(argv) > 1:
        return pathlib.Path(argv[1]).read_text(encoding="utf-8")
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (SkillFinder updater)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def parse_moves(text):
    moves, pos = [], 0
    for m in MOVE_RE.finditer(text):
        if m.start() != pos:
            break
        moves.append({"move": m.group(1).strip(), "skill": m.group(2).strip(), "lv": int(m.group(3))})
        pos = m.end()
    if pos != len(text):
        raise ValueError(f"could not parse moves: {text!r}")
    return moves


def main():
    html = load_html(sys.argv)
    i = html.index("var DATA = ") + len("var DATA = ")
    data, _ = json.JSONDecoder().raw_decode(html[i:])
    mons = []
    for p in data:
        mons.append({
            "dex": p["dex"], "name": p["name"], "type": p["type"], "ball": p["ball"],
            "region": p["region"], "how": p["how"], "from": p["from"], "into": p["into"],
            "moves": parse_moves(p["moves"]),
        })
    skills = {}
    for p in mons:
        for m in p["moves"]:
            skills.setdefault(m["skill"], set()).add(p["dex"])
    out = {
        "meta": {
            "source": URL,
            "updated": datetime.date.today().isoformat(),
            "pokemon": len(mons),
            "skills": len(skills),
        },
        "pokemon": mons,
    }
    blob = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
    OUT.write_text(blob, encoding="utf-8")
    # data.js lets the page work from file:// and a plain static host without fetch()/CORS
    OUT.with_suffix(".js").write_text("window.SKILLDATA=" + blob + ";\n", encoding="utf-8")
    print(f"wrote {OUT} + data.js: {len(mons)} pokemon, {len(skills)} distinct skills, {OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
