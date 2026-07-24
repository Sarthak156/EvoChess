# Adaptive Chess RL
A full-stack adaptive chess application: it learns **which pre-match rule modifications** create fair, varied and strategically interesting games, rather than trying to outplay the human.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=backend uvicorn app.main:app --reload
# another terminal
cd frontend && npm install && npm run dev
```
Open `http://localhost:5173`; Swagger API docs are at `http://localhost:8000/docs`.

## Commands
- `PYTHONPATH=backend pytest tests -q` — tests
- `PYTHONPATH=backend python scripts/train.py` — train a PPO contextual policy from completed games
- `cd frontend && npm run build` — production UI build

## Architecture
`frontend` is the React UI. FastAPI routes call the game service, which rehydrates an `AdaptiveGame` from persisted move logs. The rule engine exposes independent plugins and filters `python-chess` legal moves. Feature extraction persists player metrics at game end; policy episodes feed the Gymnasium/PPO training environment.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md), [`docs/RULE_ENGINE.md`](docs/RULE_ENGINE.md), and [`docs/TRAINING.md`](docs/TRAINING.md).

Additional references: [API](docs/API.md) · [Developer guide](docs/DEVELOPER_GUIDE.md)
