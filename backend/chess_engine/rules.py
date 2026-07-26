"""Composable rule plugins. Hooks never mutate python-chess legality outside their scope."""
from __future__ import annotations
from dataclasses import dataclass,field
from abc import ABC
import chess, random
@dataclass
class RuleState:
 turn:int=0; last_piece:dict[bool,int]=field(default_factory=dict); consecutive:dict[tuple[bool,int],int]=field(default_factory=dict); cooldown:dict[tuple[bool,int],int]=field(default_factory=dict); immune:dict[int,int]=field(default_factory=dict); pending_promotion:dict[int,bool]=field(default_factory=dict); first_captured:dict[bool,tuple[int,chess.Piece]|None]=field(default_factory=lambda:{True:None,False:None}); capture_turn:dict[bool,int]=field(default_factory=dict)
class Rule(ABC):
 id:int; name:str; description:str; counters:str=''
 def legal(self,b:chess.Board,m:chess.Move,s:RuleState)->bool:return True
 def after(self,b:chess.Board,m:chess.Move,s:RuleState,captured:chess.Piece|None):pass
class RoyalTax(Rule):
 id=1;name='Royal Tax';description='Queen cannot capture until move 8.';counters='early queen attacks'
 def legal(self,b,m,s): return not (s.turn<14 and b.piece_at(m.from_square).piece_type==chess.QUEEN and b.is_capture(m))
class TiredKnights(Rule):
 id=2;name='Tired Knights';description='Knights cannot move on consecutive turns.';counters='knight-heavy play'
 def legal(self,b,m,s): return not(b.piece_at(m.from_square).piece_type==chess.KNIGHT and s.last_piece.get(b.turn)==chess.KNIGHT)
class DelayedCastling(Rule):
 id=3;name='Delayed Castling';description='Castling allowed only after move 10.';counters='early castling'
 def legal(self,b,m,s): return not(b.is_castling(m) and s.turn<18)
class HeavyPawns(Rule):
 id=4;name='Heavy Pawns';description='Pawns may only advance one square initially.';counters='fast pawn storms'
 def legal(self,b,m,s): return not(b.piece_at(m.from_square).piece_type==chess.PAWN and abs(m.to_square-m.from_square)==16)
class FragileQueen(Rule):
 id=5;name='Fragile Queen';description='Queen skips its next move after a capture.';counters='queen domination'
 def legal(self,b,m,s): return not(b.piece_at(m.from_square).piece_type==chess.QUEEN and s.cooldown.get((b.turn,chess.QUEEN),0)>0)
 def after(self,b,m,s,c):
  if c and b.piece_at(m.to_square).piece_type==chess.QUEEN:s.cooldown[(not b.turn,chess.QUEEN)]=1
class ExhaustedRook(Rule):
 id=6;name='Exhausted Rook';description='A rook cannot capture twice consecutively.';counters='rook sweeps'
 def legal(self,b,m,s): return not(b.piece_at(m.from_square).piece_type==chess.ROOK and b.is_capture(m) and s.cooldown.get((b.turn,chess.ROOK),0)>0)
 def after(self,b,m,s,c):
  if c and b.piece_at(m.to_square).piece_type==chess.ROOK:s.cooldown[(not b.turn,chess.ROOK)]=1
class SlowBishop(Rule):
 id=7;name='Slow Bishop';description='Bishop movement is capped at four squares.';counters='long diagonals'
 def legal(self,b,m,s): return not(b.piece_at(m.from_square).piece_type==chess.BISHOP and max(abs(chess.square_file(m.to_square)-chess.square_file(m.from_square)),abs(chess.square_rank(m.to_square)-chess.square_rank(m.from_square)))>4)
class SprintKing(Rule): id=8;name='Sprint King';description='King has one two-square defensive move.';counters='defensive flexibility'
class PromotionDelay(Rule): id=9;name='Promotion Delay';description='Promotion is delayed one turn.';counters='instant promotions'
class Fortress(Rule): id=10;name='Fortress';description='First captured piece may revive after five turns.';counters='short tactical games'
class FogTurn(Rule):
 id=11;name='Fog Turn';description='Every 10th turn permits no captures.';counters='capture rhythm'
 def legal(self,b,m,s):return not(s.turn>0 and s.turn%20==0 and b.is_capture(m))
class MomentumCapture(Rule): id=12;name='Momentum Capture';description='Capturing pieces continue direction where legal.';counters='repositioning'
class ShieldedPawns(Rule): id=13;name='Shielded Pawns';description='One selected pawn survives first capture.';counters='opening pressure'
class BridgeSquares(Rule):
 id=14;name='Bridge Squares';description='Central arrivals gain one-turn immunity.';counters='center avoidance'
 def legal(self,b,m,s): return not(b.is_capture(m) and m.to_square in s.immune and s.immune[m.to_square]>=s.turn)
 def after(self,b,m,s,c):
  if m.to_square in [chess.D4,chess.E4,chess.D5,chess.E5]:s.immune[m.to_square]=s.turn+1
class PieceFatigue(Rule):
 id=15;name='Piece Fatigue';description='Same piece three turns causes a skipped turn.';counters='single-piece overuse'
 def legal(self,b,m,s):return s.cooldown.get((b.turn,m.from_square),0)<=0
 def after(self,b,m,s,c):
  key=(not b.turn,m.to_square);s.consecutive[key]=s.consecutive.get(key,0)+1
  if s.consecutive[key]>=3:s.cooldown[(b.turn,m.to_square)]=1;s.consecutive[key]=0
class RandomPromotion(Rule):
 id=16;name='Random Promotion';description='Promotion is randomly selected.';counters='promotion certainty'
 def legal(self,b,m,s):return not(m.promotion and m.promotion!=random.choice([2,3,4,5]))
class SacrificeBonus(Rule): id=17;name='Sacrifice Bonus';description='A sacrifice can earn a power move.';counters='passive tactics'
class RotatingBoard(Rule): id=18;name='Rotating Board';description='Board rotates every 15 moves (visual orientation).';counters='spatial habits'
class MirrorMove(Rule): id=19;name='Mirror Move';description='One legal matching reply may be mirrored.';counters='predictable replies'
class AdaptiveHandicap(Rule): id=20;name='Adaptive Handicap';description='A style-aware temporary strategic bonus.';counters='style-specific habits'
RULES={r.id:r for r in [RoyalTax(),TiredKnights(),DelayedCastling(),HeavyPawns(),FragileQueen(),ExhaustedRook(),SlowBishop(),SprintKing(),PromotionDelay(),Fortress(),FogTurn(),MomentumCapture(),ShieldedPawns(),BridgeSquares(),PieceFatigue(),RandomPromotion(),SacrificeBonus(),RotatingBoard(),MirrorMove(),AdaptiveHandicap()]}
INCOMPATIBLE=[{9,16}]
