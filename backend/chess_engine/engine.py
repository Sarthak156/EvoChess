from __future__ import annotations
import chess
from .rules import Rule,RuleState,RULES,INCOMPATIBLE
class GameError(ValueError): pass
class RuleEngine:
 def __init__(self,rule_ids:list[int]):
  if not 1<=len(rule_ids)<=3 or any(i not in RULES for i in rule_ids):raise GameError('Select between one and three valid rules.')
  if any(x<=set(rule_ids) for x in INCOMPATIBLE):raise GameError('Selected rules are incompatible.')
  self.rules=[RULES[i] for i in rule_ids];self.state=RuleState()
 def legal_moves(self,b:chess.Board)->list[chess.Move]:return [m for m in b.legal_moves if all(r.legal(b,m,self.state) for r in self.rules)]
 def push(self,b:chess.Board,uci:str)->chess.Move:
  try:m=chess.Move.from_uci(uci)
  except ValueError:raise GameError('Move must be UCI notation, e.g. e2e4.')
  if m not in self.legal_moves(b):raise GameError('Move is illegal under chess or active-rule constraints.')
  piece=b.piece_at(m.from_square); captured=b.piece_at(m.to_square)
  # Random Promotion resolves server-side in a deterministic valid family.
  if any(r.id==16 for r in self.rules) and m.promotion: m=chess.Move(m.from_square,m.to_square,promotion=chess.QUEEN)
  b.push(m);self.state.turn+=1;self.state.last_piece[not b.turn]=piece.piece_type
  for r in self.rules:r.after(b,m,self.state,captured)
  # decrement only the side that has just recovered its next opportunity
  for k in list(self.state.cooldown):
   if k[0]==b.turn and self.state.cooldown[k]>0:self.state.cooldown[k]-=1
  return m
 def payload(self):return [{'id':r.id,'name':r.name,'description':r.description,'counters':r.counters} for r in self.rules]
class AdaptiveGame:
 def __init__(self,rule_ids:list[int],fen:str|None=None):self.board=chess.Board(fen) if fen else chess.Board();self.rules=RuleEngine(rule_ids);self.move_log=[]
 def move(self,uci:str,elapsed_ms:int=0):
  san=self.board.san(chess.Move.from_uci(uci));m=self.rules.push(self.board,uci);d={'uci':m.uci(),'san':san,'elapsed_ms':elapsed_ms,'ply':len(self.move_log)+1};self.move_log.append(d);return d
 def outcome(self):
  if self.board.is_checkmate():return '0-1' if self.board.turn else '1-0'
  if self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.can_claim_draw():return '1/2-1/2'
  return '*'
