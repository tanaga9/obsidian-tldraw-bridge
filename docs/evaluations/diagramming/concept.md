# Cache concept diagram

Create an editable tldraw concept diagram in the specified Obsidian vault to
explain caching to newly assigned developers. Use this simplified model:

- Client requests data from API.
- API optionally uses Cache. Without Cache, it can retrieve data from Origin.
- On a cache hit, API returns data from Cache to Client. Origin access is unnecessary.
- On a cache miss, API retrieves data from Origin, stores it in Cache, and returns it to Client.
- When Origin is updated, Invalidation invalidates the corresponding Cache entry.
- The next request after invalidation is a miss and retrieves the new data from Origin.

The central distinction is that a cache hit avoids Origin access, while a miss
still needs Origin. Make the processing paths and dependencies clear. Colors
are unrestricted. The viewing environment is a light background with a
1280 × 800 CSS-pixel drawing viewport. Readers can view the overview and then
read details at 100% canvas zoom. Complete creation, inspection, and saving of
the diagram.
