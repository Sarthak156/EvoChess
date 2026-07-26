# Developer guide
## Local quality checks
```bash
PYTHONPATH=backend pytest tests -q
python -m compileall backend
cd frontend && npm run build
```

## Extension boundaries
- Put a new rules plugin in `backend/chess_engine/rules.py` (or split it into a module), register it in `RULES`, then add an incompatibility constraint and tests.
- Keep API handlers thin. Lifecycle/database work belongs in `services/game_service.py`.
- A state feature must be added to `FEATURE_NAMES`; this makes vector ordering explicit and reproducible.
- Database migrations should be introduced with Alembic for production PostgreSQL deployments.

## Deployment
Set `DATABASE_URL` to a PostgreSQL SQLAlchemy URL, set `CORS_ORIGINS` appropriately, serve the Vite build via a static host, and run Uvicorn/Gunicorn behind TLS. Persist `saved_models/` separately from ephemeral containers.
