"""Train PPO from stored episodes: PYTHONPATH=backend python scripts/train.py"""
from stable_baselines3 import PPO
from app.rl.environment import RuleSelectionEnv
from app.db.session import SessionLocal
from app.db.models import PolicyEpisode
from pathlib import Path
db=SessionLocal(); rows=db.query(PolicyEpisode).all();records=[{'state':r.state,'rules':r.rule_ids,'reward':r.reward} for r in rows] or [{'state':[0.]*17,'rules':[20],'reward':.1}]
model=PPO('MlpPolicy',RuleSelectionEnv(records),verbose=1,n_steps=32,batch_size=32);model.learn(10_000);Path('saved_models').mkdir(exist_ok=True);model.save('saved_models/ppo_rule_selector')
