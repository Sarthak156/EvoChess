# Rule engine
Rules inherit `Rule` and may implement `legal(board, move, state)` and `after(board, move, state, captured)`. `RuleEngine` intersects standard python-chess legality with every active plugin, validates 1–3 rule selection, and rejects declared incompatible sets (Promotion Delay + Random Promotion).

Rule descriptions—including experimental rules whose visual/client interaction is required—are exposed at `GET /api/rules`. Add a rule by subclassing `Rule`, registering it in `RULES`, and adding focused engine tests.
