import sys;sys.path.append('backend')
import chess
from app.chess_engine.engine import AdaptiveGame,GameError
from app.chess_engine.rules import RuleEngine
def test_heavy_pawn_blocks_double_push():
 g=AdaptiveGame([4])
 try:g.move('e2e4');assert False
 except GameError:assert True
def test_standard_single_pawn_move_works():
 g=AdaptiveGame([4]);g.move('e2e3');assert g.board.piece_at(chess.E3).piece_type==chess.PAWN
def test_incompatible_rules():
 try:RuleEngine([9,16]);assert False
 except GameError:assert True
