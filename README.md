# Sovereign RO Pokédex Skill Finder

Search the [Sovereign RO Pokédex](https://sovereignro.com/?module=pokedex) by the **Ragnarok Online skill** each Pokémon move uses (Psychic Wave, Earthquake, Spiral Pierce, …).

**Live site:** https://tomyee92.github.io/SovereignROSkillFinder/

## Features
- Pick one or more RO skills (autocomplete, or "Browse all skills" grouped by AOE / Single / Support).
- **Has all / Has any** when several skills are selected.
- Filter by **skill level** (min–max) or **top level only** per skill.
- Filter by name or Pokédex #, type and ball.
- Sort by Pokédex #, name, skill level, number of matching skills, or ball rarity; ascending/descending.
- **★ Rare** category: the game has a hidden Rare category that its website does not show, so the list is collected by players (`rare.js`). Tick **Rare only** to see them; each one also gets a ★ Rare badge.
- Matching skills are highlighted on each card. **Copy link** shares the exact search (state lives in the URL hash).

## How it works
Static site, no build step: `index.html` + `data.js` (a snapshot of the Pokédex data). Pictures are loaded directly from sovereignro.com.

## Adding Rare Pokémon
Open `rare.js`, add the exact Pokédex name on a new line (keep the comma), then commit and push. `update_data.py` never touches this file.

## Updating the data
When the server changes the Pokédex, rebuild the snapshot and push:

```bash
python scripts/update_data.py        # fetches the live page, rewrites data.json + data.js
git add data.json data.js && git commit -m "Update data" && git push
```

## Notes
- Unofficial fan tool, not affiliated with Sovereign RO.
- The AOE / Single / Support tags are approximate. Whether a skill hits an area follows the rAthena Renewal skill database; how hard it hits depends on the server and the Pokémon's own stats, which are not shown here.
