from __future__ import annotations
import random
from app.chess_engine.rules import RULES,INCOMPATIBLE
from app.features.extractor import vector
class RuleSelector:
 def select(self,metrics:dict,previous:list[int]|None=None)->tuple[list[int],str]:
  # Explainable baseline policy; PPO training can replace scoring without changing API.
  candidates=[]
  mapping=[('queen_usage',1),('queen_usage',5),('knight_usage',2),('pawn_aggression',4),('castling_preference',3),('bishop_usage',7),('capture_frequency',11),('center_control',14)]
  for feature,rid in mapping:
   if metrics.get(feature,0)>=.12 or (feature=='castling_preference' and metrics.get(feature,0)>0):candidates.append(rid)
  candidates=list(dict.fromkeys(candidates)) or [20,8]
  ids=candidates[:min(3,max(1,len(candidates)))];
  if any(x<=set(ids) for x in INCOMPATIBLE):ids=[x for x in ids if x!=16]
  behaviors=[]
  for feat,rid in mapping:
   if rid in ids:behaviors.append(f'{feat.replace("_"," ")} is elevated')
  names=', '.join(RULES[x].name for x in ids); reason='; '.join(behaviors[:3]) or 'your profile benefits from a balanced strategic adjustment'
  return ids,f'Active rules: {names}. Selected because {reason}; they encourage strategic variety while remaining fixed and visible for this match.'
