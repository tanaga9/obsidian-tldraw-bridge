# Incident timeline

Create an editable tldraw diagram in the specified Obsidian vault to explain
the following fictional incident at a review meeting. The audience is the
service's engineers. Distinguish chronology from confirmed causal relationships.

| Time | Participant | Event |
| --- | --- | --- |
| 10:00 | API | Release v2 starts |
| 10:02 | Database | Increased connections from API v2 exhaust the connection pool |
| 10:03 | API | Connection pool exhaustion causes request timeouts |
| 10:04 | Client | Retries after timeouts increase pending requests |
| 10:05 | Metrics | The monitoring process restarts; a causal connection to the API incident is unconfirmed |
| 10:06 | Operator | Rollback of API v2 starts |
| 10:08 | API | Connection counts return to normal and new requests can be processed again |
| 10:12 | Client | Pending requests are cleared |

The confirmed causal links are "increased connections from API v2 → connection
pool exhaustion" and "connection pool exhaustion → API timeouts." Do not invent
additional causes. You may show the explicitly described client retry response.

The viewing environment is a light background with a 1280 × 800 CSS-pixel
drawing viewport. Readers can inspect the overall flow and then zoom into
details. Panning and zooming are available for long diagrams. If the layout
shows event order only, do not imply that spatial intervals represent elapsed
time. Complete creation, inspection, and saving of the diagram.
