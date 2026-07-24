# API guide
All routes return JSON. Interactive, generated OpenAPI documentation is available at `/docs`.

| Method | Route | Purpose |
|---|---|---|
| POST | `/api/players` | Create profile (`{"name":"..."}`) |
| GET | `/api/players` | List profiles |
| POST | `/api/matches` | Start game (`player_id`, optional `requested_rules`) |
| GET | `/api/matches/{id}` | Current canonical game state and filtered legal moves |
| POST | `/api/matches/{id}/moves` | Submit UCI move and optional `elapsed_ms` |
| GET | `/api/rules` | Rule catalogue |
| GET | `/api/players/{id}/analytics` | Profile and policy episode history |
| GET | `/api/dashboard` | Aggregate learning telemetry |

Move submission example: `{"uci":"e2e4","elapsed_ms":810}`. Rule constraints are enforced server-side; invalid moves return HTTP 400.
