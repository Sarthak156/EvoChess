# Dependency compatibility policy
The project uses maintained, non-deprecated major versions and conservative upper bounds to prevent accidental breaking-major upgrades. Python uses Pydantic v2 (`SettingsConfigDict`, not the deprecated v1 `Config` class), SQLAlchemy 2.x, FastAPI with Pydantic 2, Gymnasium (not unmaintained `gym`), and Stable-Baselines3 2.x+.

## Verified installation procedure
Use a clean virtual environment and run these commands in CI and before releases:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip check
PYTHONPATH=backend pytest tests -q
```

For the UI, use Node as declared in `frontend/package.json` and a fresh install:
```bash
cd frontend
npm install
npm ls --all
npm run build
```
`npm install` produces `package-lock.json`; commit that lockfile for a release build. Dependabot/Renovate should update dependencies in isolated PRs that run the commands above.
