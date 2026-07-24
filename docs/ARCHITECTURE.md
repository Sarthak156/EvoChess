# Architecture
## Layers
1. **UI** — Vite/React routes for play, rules and learning dashboard.
2. **API** — FastAPI contracts, validation, OpenAPI at `/docs`.
3. **Application** — `game_service` owns transactions and match lifecycle.
4. **Domain** — `AdaptiveGame` wraps python-chess; `RuleEngine` composes plugins.
5. **Data** — SQLAlchemy models: players, matches, metrics and policy episodes.
6. **ML** — feature vectors → Gymnasium contextual bandit → PPO.

The API is stateless: each request rebuilds board state from the persisted canonical UCI log, making it safe to scale behind a shared database.
