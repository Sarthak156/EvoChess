"""Deterministic, rule-aware local opponent.

The opponent intentionally uses the same RuleEngine legal move list as the player. This
keeps custom-rule enforcement server authoritative and makes it replaceable by a UCI
engine or a learned policy later.
"""
from __future__ import annotations
import chess
from .engine import AdaptiveGame
PIECE_VALUE={chess.PAWN:100,chess.KNIGHT:320,chess.BISHOP:330,chess.ROOK:500,chess.QUEEN:900,chess.KING:20_000}
def choose_move(game:AdaptiveGame)->str|None:
 """Pick Black's strongest one-ply move, with deterministic UCI tie-breaking."""
 board=game.board
 legal=list(game.rules.legal_moves(board))
 if not legal:return None
 def score(move:chess.Move)->tuple[int,int,int,str]:
  victim=board.piece_at(move.to_square)
  attacker=board.piece_at(move.from_square)
  capture=PIECE_VALUE.get(victim.piece_type,0) if victim else 0
  # Prefer a favorable exchange, checking moves, then centralization.
  exchange=capture-PIECE_VALUE.get(attacker.piece_type,0)//10 if attacker else capture
  board.push(move);check=int(board.is_check());mate=int(board.is_checkmate());board.pop()
  center=int(move.to_square in (chess.D4,chess.E4,chess.D5,chess.E5))
  return (mate,check,exchange+center,move.uci())
 return max(legal,key=score).uci()
