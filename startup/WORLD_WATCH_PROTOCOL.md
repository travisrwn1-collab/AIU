# World Watch Protocol

When Trav says "world watch" or "update the stories":

## Steps

1. Read `world_watch/stories.json`
2. Search current news for each active story
3. Add new updates with date, summary, sources, spins
4. Note new connections between stories
5. Add pending questions
6. Write updated JSON back to `stories.json`
7. Regenerate `stories_readable.txt` from the JSON
8. Show Trav the readable file

## Adding a New Story

If significant news emerges not already tracked:
- Ask Trav before adding
- Use the same JSON structure
- Include: id, title, status, started date, first update

## Connections

Look for patterns across stories:
- Same actors (administrations, leaders, organizations)
- Same regions
- Economic threads (oil, contracts, investments)
- Timing patterns
- Who's present / who's absent

## Sources

Always note sources. Document multiple framings when they exist.

## Files

- `world_watch/stories.json` - machine data
- `world_watch/stories_readable.txt` - human readable

---

Started: January 23, 2026
