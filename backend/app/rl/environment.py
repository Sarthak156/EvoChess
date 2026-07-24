import gymnasium as gym
from gymnasium import spaces
import numpy as np
from ..features.extractor import FEATURE_NAMES
class RuleSelectionEnv(gym.Env):
 """Offline contextual bandit: action encodes 20 choose 1..3 legal presets."""
 metadata={'render_modes':[]}
 def __init__(self,records=None):
  self.records=records or [];self.observation_space=spaces.Box(0,1,shape=(len(FEATURE_NAMES)+3,),dtype=np.float32);self.action_space=spaces.Discrete(20)
 def reset(self,seed=None,options=None):
  super().reset(seed=seed);self.record=self.records[self.np_random.integers(len(self.records))] if self.records else {'state':[0.]*17,'reward':0.};return np.array(self.record['state'],dtype=np.float32),{}
 def step(self,action):
  target=set(self.record.get('rules',[]));reward=float(self.record.get('reward',0))+(0.15 if action+1 in target else -0.05);return np.array(self.record['state'],dtype=np.float32),reward,True,False,{'selected_rule':int(action+1)}
